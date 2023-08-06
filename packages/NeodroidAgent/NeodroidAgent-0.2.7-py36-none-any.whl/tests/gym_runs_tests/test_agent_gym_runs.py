#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from agent.agents.model_free.hybrid.ddpg_agent import ddpg_test
from agent.agents.model_free.q_learning.dqn_agent import dqn_test
from agent.agents.model_free.policy_optimisation.pg_agent import pg_test

__author__ = 'cnheider'
__doc__ = ''


@pytest.mark.slow
def test_pg_agent():
  pg_test(1)


@pytest.mark.slow
def test_dqn_agent():
  dqn_test(1)


@pytest.mark.slow
def test_ppo_agent():
  pass
  # ppo_test(1)


@pytest.mark.slow
def test_ddpg_agent():
  ddpg_test(1)


if __name__ == '__main__':
  test_ddpg_agent()
  test_ppo_agent()
