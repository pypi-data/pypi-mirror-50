#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Iterable
from itertools import count
from typing import Type

import gym

import draugr
from neodroidagent import PROJECT_APP_PATH, utilities as U
from neodroidagent.interfaces.agent import Agent
from neodroidagent.interfaces.specifications import TrainingSession
from neodroidagent.training.procedures import train_episodically
from draugr.stopping.stopping_key import add_early_stopping_key_combination
from neodroid.environments import VectorEnvironment
from neodroid.wrappers import NeodroidGymWrapper
from trolls.wrappers.vector_environments import VectorWrap

__author__ = 'cnheider'
__doc__ = ''


class linear_training(TrainingSession):

  def __call__(self,
               agent_type: Type[Agent],
               *,
               environment=None,
               save=False,
               has_x_server=False,
               **kwargs):

    kwargs = NOD(**kwargs)

    if not kwargs.connect_to_running:
      if not environment:
        if '-v' in kwargs.environment_name:
          environment = VectorWrap(NeodroidGymWrapper(gym.make(kwargs.environment_name)))
        else:
          environment = VectorEnvironment(name=kwargs.environment_name,
                                          connect_to_running=kwargs.connect_to_running)
    else:
      environment = VectorEnvironment(name=kwargs.environment_name,
                                      connect_to_running=kwargs.connect_to_running)

    agent_class_name = agent_type.__name__
    model_directory = (PROJECT_APP_PATH.user_data / kwargs.environment_name /
                       agent_class_name / kwargs.load_time / 'models')
    config_directory = (PROJECT_APP_PATH.user_data / kwargs.environment_name /
                        agent_class_name / kwargs.load_time / 'configs')
    log_directory = (PROJECT_APP_PATH.user_log / kwargs.environment_name /
                     agent_class_name / kwargs.load_time)

    kwargs.log_directory = log_directory
    kwargs.config_directory = config_directory
    kwargs.model_directory = model_directory

    U.set_seeds(kwargs['SEED'])
    environment.seed(kwargs['SEED'])

    agent = agent_type(**kwargs)
    agent.build(environment)

    listener = add_early_stopping_key_combination(agent.stop_training, has_x_server=save)

    if listener:
      listener.start()
    try:
      training_resume = self._training_procedure(agent,
                                                 environment,
                                                 render=kwargs.render_environment,
                                                 **kwargs)
    finally:
      if listener:
        listener.stop()

    if save:
      identifier = count()
      if isinstance(training_resume.models, Iterable):
        for model in training_resume.models:
          U.save_model(model, name=f'{agent.__name__}-{identifier.__next__()}', **kwargs)
      else:
        U.save_model(training_resume.models,
                     name=f'{agent.__name__}-{identifier.__next__()}', **kwargs)

      if training_resume.stats:
        training_resume.stats.save(project_name=kwargs.project,
                                   config_name=kwargs.config_name,
                                   directory=kwargs.log_directory)

    environment.close()


if __name__ == '__main__':
  import neodroidagent.configs.agent_test_configs.pg_test_config as C
  from neodroidagent.agents.model_free.policy_optimisation.pg_agent import PGAgent

  env = VectorEnvironment(name=C.ENVIRONMENT_NAME,
                          connect_to_running=C.CONNECT_TO_RUNNING)
  env.seed(C.SEED)

  linear_training(training_procedure=train_episodically)(agent_type=PGAgent, config=C, environment=env)
