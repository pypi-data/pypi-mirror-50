from copy import deepcopy

import numpy as np
import pytest

from lcs.agents.racs import Classifier, Configuration, Condition, Effect
from lcs.agents.racs.components.genetic_algorithm import mutate, crossover, \
    _flatten, _unflatten
from lcs.representations import UBR
from lcs.representations.RealValueEncoder import RealValueEncoder


class TestGeneticAlgorithm:

    @pytest.fixture
    def cfg(self):
        return Configuration(classifier_length=2,
                             number_of_possible_actions=2,
                             encoder=RealValueEncoder(4))

    @pytest.mark.parametrize("_cond, _effect", [
        ([UBR(2, 5), UBR(5, 10)], [UBR(2, 5), UBR(5, 10)]),
        ([UBR(5, 2), UBR(10, 5)], [UBR(5, 2), UBR(10, 5)]),
        ([UBR(2, 2), UBR(5, 5)], [UBR(2, 2), UBR(5, 5)]),
        ([UBR(0, 15), UBR(0, 15)], [UBR(0, 15), UBR(0, 15)]),
    ])
    def test_aggressive_mutation(self, _cond, _effect, cfg):
        # given
        condition = Condition(_cond, cfg)
        effect = Effect(_effect, cfg)

        cfg.encoder = RealValueEncoder(16)  # more precise encoder
        cfg.mutation_noise = 0.5  # strong noise mutation range
        mu = 1.0  # mutate every attribute

        cl = Classifier(
            condition=deepcopy(condition),
            effect=deepcopy(effect),
            cfg=cfg)

        # when
        mutate(cl, mu)

        # then
        range_min, range_max = cfg.encoder.range
        for idx, (c, e) in enumerate(zip(cl.condition, cl.effect)):
            # assert that we have new locus
            if condition[idx] != cfg.classifier_wildcard:
                assert condition[idx] != c

            if effect[idx] != cfg.classifier_wildcard:
                assert effect[idx] != e

            # assert if condition values are in ranges
            assert c.lower_bound >= range_min
            assert c.upper_bound <= range_max

            # assert if effect values are in ranges
            assert e.lower_bound >= range_min
            assert e.upper_bound <= range_max

    @pytest.mark.parametrize("_cond, _effect", [
        ([UBR(2, 5), UBR(5, 10)], [UBR(3, 6), UBR(1, 1)]),
    ])
    def test_disabled_mutation(self, _cond, _effect, cfg):
        # given
        condition = Condition(_cond, cfg)
        effect = Effect(_effect, cfg)
        cl = Classifier(
            condition=deepcopy(condition),
            effect=deepcopy(effect),
            cfg=cfg)
        mu = 0.0

        # when
        mutate(cl, mu)

        # then
        for idx, (c, e) in enumerate(zip(cl.condition, cl.effect)):
            assert c.lower_bound == condition[idx].lower_bound
            assert c.upper_bound == condition[idx].upper_bound
            assert e.lower_bound == effect[idx].lower_bound
            assert e.upper_bound == effect[idx].upper_bound

    def test_crossover(self, cfg):
        # given
        parent = Classifier(
            condition=Condition([UBR(1, 1), UBR(1, 1), UBR(1, 1)], cfg),
            effect=Effect([UBR(1, 1), UBR(1, 1), UBR(1, 1)], cfg),
            cfg=cfg)
        donor = Classifier(
            condition=Condition([UBR(2, 2), UBR(2, 2), UBR(2, 2)], cfg),
            effect=Effect([UBR(2, 2), UBR(2, 2), UBR(2, 2)], cfg),
            cfg=cfg)

        # when
        np.random.seed(12345)  # left: 3, right: 6
        crossover(parent, donor)

        # then
        assert parent.condition == \
            Condition([UBR(1, 1), UBR(1, 2), UBR(2, 2)], cfg)
        assert parent.effect == \
            Effect([UBR(1, 1), UBR(1, 2), UBR(2, 2)], cfg)
        assert donor.condition == \
            Condition([UBR(2, 2), UBR(2, 1), UBR(1, 1)], cfg)
        assert donor.effect == \
            Effect([UBR(2, 2), UBR(2, 1), UBR(1, 1)], cfg)

    @pytest.mark.parametrize("_cond, _result", [
        ([UBR(1, 3), UBR(2, 4)], [1, 3, 2, 4])
    ])
    def test_should_flatten_condition(self, _cond, _result, cfg):
        assert _flatten(Condition(_cond, cfg=cfg)) == _result

    @pytest.mark.parametrize("_effect, _result", [
        ([UBR(1, 3), UBR(2, 4)], [1, 3, 2, 4])
    ])
    def test_should_flatten_effect(self, _effect, _result, cfg):
        assert _flatten(Effect(_effect, cfg=cfg)) == _result

    @pytest.mark.parametrize("_flat, _result", [
        ([1, 3], [UBR(1, 3)]),
        ([1, 3, 2, 4], [UBR(1, 3), UBR(2, 4)])
    ])
    def test_should_unflatten(self, _flat, _result):
        assert _unflatten(_flat) == _result
