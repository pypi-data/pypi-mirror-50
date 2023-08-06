#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import copy
from abc import abstractmethod
from itertools import count
from typing import Any

import numpy as np
import torch
from tqdm import tqdm

import draugr
from agent import utilities as U
from agent.architectures import MLP
from agent.architectures.experimental.merged import MergedInputMLP
from agent.exploration import OrnsteinUhlenbeckProcess
from agent.interfaces.specifications import GDCS
from agent.interfaces.torch_agent import TorchAgent
from agent.memory import TransitionBuffer
from draugr.writers.writer import Writer
from neodroid.environments.environment import Environment
from neodroid.interfaces.specifications import EnvironmentSnapshot

__author__ = 'cnheider'


class ActorCriticAgent(TorchAgent):
  '''
All value iteration agents should inherit from this class
'''

  # region Private

  def __init__(self, *args, **kwargs):
    self._actor_arch_spec: GDCS = None
    self._critic_arch_spec: GDCS = None

    self._target_update_tau = 3e-3
    self._signal_clipping = False
    self._action_clipping = False

    self._memory_buffer = TransitionBuffer()

    self._actor_optimiser_spec: GDCS = GDCS(constructor=torch.optim.Adam,
                                            kwargs={'lr':3e-4}
                                            )

    self._critic_optimiser_spec: GDCS = GDCS(constructor=torch.optim.Adam,
                                             kwargs={'lr':          3e-3,
                                                     'weight_decay':3e-2
                                                     }
                                             )

    self._actor_arch_spec = GDCS(MLP,
                                 kwargs=draugr.NOD({'input_shape':      None,  # Obtain from environment
                                                    'hidden_layers':    None,
                                                    'output_activation':torch.relu,
                                                    'output_shape':     None,  # Obtain from environment
                                                    }))

    self._critic_arch_spec = GDCS(MergedInputMLP,
                                  kwargs=draugr.NOD({'input_shape':      None,  # Obtain from environment
                                                     'hidden_layers':    None,
                                                     'output_activation':torch.relu,
                                                     'output_shape':     None,  # Obtain from environment
                                                     }))

    self._random_process_spec = GDCS(constructor=OrnsteinUhlenbeckProcess, kwargs=dict(theta=0.15,
                                                                                       sigma=0.2
                                                                                       ))

    super().__init__(*args, **kwargs)

  def _build(self, env, stat_writer:Writer=None, **kwargs) -> None:
    # Construct actor and critic
    self._actor = self._actor_arch_spec.constructor(**self._actor_arch_spec.kwargs).to(self._device)
    self._target_actor = self._actor_arch_spec.constructor(**self._actor_arch_spec.kwargs).to(
        self._device).eval()

    self._critic = self._critic_arch_spec.constructor(**self._critic_arch_spec.kwargs).to(self._device)
    self._target_critic = self._critic_arch_spec.constructor(**self._critic_arch_spec.kwargs).to(
        self._device).eval()

    self._random_process = self._random_process_spec.constructor(**self._random_process_spec.kwargs)

    # Construct the optimizers for actor and critic
    self._actor_optimiser = self._actor_optimiser_spec.constructor(self._actor.parameters(),
                                                                   **self._actor_optimiser_spec.kwargs
                                                                   )
    self._critic_optimiser = self._critic_optimiser_spec.constructor(self._critic.parameters(),
                                                                     **self._critic_optimiser_spec.kwargs
                                                                     )

    if stat_writer:
      dummy_in = torch.rand(1, *self.input_shape)

      model = copy.deepcopy(self._critic)
      model.to('cpu')
      if isinstance(stat_writer, draugr.TensorBoardXWriter):
        stat_writer._graph(model, dummy_in)

      model = copy.deepcopy(self._actor)
      model.to('cpu')
      if isinstance(stat_writer, draugr.TensorBoardXWriter):
        stat_writer._graph(model, dummy_in)

    actor_num_params = sum(param.numel() for param in self._actor.parameters())
    critic_num_params = sum(param.numel() for param in self._critic.parameters())

    actor_num_trainable_params = sum(
        p.numel() for p in self._actor.parameters() if p.requires_grad)

    critic_num_trainable_params = sum(
        p.numel() for p in self._critic.parameters() if p.requires_grad)

    draugr.sprint(f'trainable/actor_num_params: {actor_num_trainable_params}/{actor_num_params}\n',
                  highlight=True, color='cyan')
    draugr.sprint(f'trainable/critic_num_params: {critic_num_trainable_params}/{critic_num_params}\n',
                  highlight=True, color='magenta')

  def _post_io_inference(self, env):

    if ('input_shape' not in self._actor_arch_spec.kwargs or
        not self._actor_arch_spec.kwargs['input_shape']):
      self._actor_arch_spec.kwargs['input_shape'] = self._input_shape

    if ('output_shape' not in self._actor_arch_spec.kwargs or
        not self._actor_arch_spec.kwargs['output_shape']):
      self._actor_arch_spec.kwargs['output_shape'] = self._output_shape

    if ('input_shape' not in self._critic_arch_spec.kwargs or
        not self._critic_arch_spec.kwargs['input_shape']):
      self._input_shape = (*self._input_shape, *self._output_shape)
      self._critic_arch_spec.kwargs['input_shape'] = self._input_shape

    if ('output_shape' not in self._critic_arch_spec.kwargs or
        not self._critic_arch_spec.kwargs['output_shape']):
      self._critic_arch_spec.kwargs['output_shape'] = 1

  # endregion

  # region Public

  def save(self, C):
    U.save_model(self._actor, name='actor', **C)
    U.save_model(self._critic, name='policy', **C)

  def load(self,
           model_path,
           evaluation=False,
           **kwargs):
    print('loading latest model: ' + model_path)

    self._build(None, **kwargs)

    self._actor.load_state_dict(torch.load(f'actor-{model_path}'))
    self._critic.load_state_dict(torch.load(f'critic-{model_path}'))

    self._update_target(target_model=self._target_critic,
                        source_model=self._critic,
                        target_update_tau=self._target_update_tau)

    self._update_target(target_model=self._target_actor,
                        source_model=self._actor,
                        target_update_tau=self._target_update_tau)

    if evaluation:
      self._actor = self._actor.eval()
      self._actor.train(False)
      self._critic = self._actor.eval()
      self._critic.train(False)

    self._actor = self._actor.to(self._device)
    self._target_actor = self._target_actor.to(self._device)
    self._critic = self._critic.to(self._device)
    self._target_critic = self._target_critic.to(self._device)

  @property
  def models(self):
    return self._actor, self._critic

  def sample(self, state, **kwargs):
    return self._sample_model(state, **kwargs)

  def rollout(self,
              initial_state: EnvironmentSnapshot,
              environment: Environment,
              *,
              render: bool = False,
              train: bool = True,
              **kwargs):
    self._update_i += 1

    state = initial_state.observables
    episode_signal = []
    episode_length = 0

    T = tqdm(count(1), f'Rollout #{self._update_i}', leave=False, disable=not render)
    for t in T:
      self._step_i += 1

      action = self.sample(state, disallow_random_sample=not train)
      snapshot = environment.react(action)

      successor_state, signal, terminated = snapshot.observables, snapshot.signal, snapshot.terminated

      if render:
        environment.render()

      # successor_state = None
      # if not terminated:  # If environment terminated then there is no successor state

      if self._signal_clipping:
        signal = np.clip(signal, -1.0, 1.0)

      if train:
        self._memory_buffer.add_transition(state,
                                           action,
                                           signal,
                                           successor_state,
                                           terminated
                                           )
      state = successor_state

      if train:
        self.update()
      episode_signal.append(signal)

      if terminated.all():
        episode_length = t
        break

    es = np.array(episode_signal).mean()
    el = episode_length
    return es, el

  # endregion

  # region Protected

  @abstractmethod
  def _sample_model(self, state, **kwargs) -> Any:
    raise NotImplementedError

  # endregion
