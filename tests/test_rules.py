import pytest

from spidermon import Rule, CallableRule, PythonExpressionRule
from spidermon.exceptions import InvalidExpression, InvalidCallable

from .test_expressions import SYNTAXERROR_EXPRESSIONS, INVALID_EXPRESSIONS, VALID_EXPRESSIONS


STATS_01 = {
    'scraped_items': 100,
}

STATS_02 = {
    'scraped_items': 0,
}

STATS_EMPTY = {}


class DummyRule(Rule):
    def check(self, stats):
        return True


class SimpleRule(Rule):
    def check(self, stats):
        return stats.scraped_items == 100


def function_rule(stats):
    return stats.scraped_items == 100


lambda_rule = lambda stats: stats.scraped_items == 100
expression_rule = 'stats.scraped_items == 100'


def test_base_rule():
    rule = Rule()
    with pytest.raises(NotImplementedError):
        rule.run_check(STATS_EMPTY)


def test_dummy_rule():
    rule = DummyRule()
    assert rule.run_check(STATS_EMPTY) is True


def test_simple_rule():
    rule = SimpleRule()
    _test_rule_with_stats(rule)


def test_not_callable():
    with pytest.raises(InvalidCallable):
        CallableRule(None)


def test_function_rule():
    rule = CallableRule(function_rule)
    _test_rule_with_stats(rule)


def test_lambda_rule():
    rule = CallableRule(lambda_rule)
    _test_rule_with_stats(rule)


def _test_rule_with_stats(rule):
    assert rule.run_check(STATS_01) is True  # PASSED
    assert rule.run_check(STATS_02) is False  # FAILED
    with pytest.raises(AttributeError):  # ERROR
        rule.run_check(STATS_EMPTY)


def test_python_rule():
    with pytest.raises(SyntaxError):
        for exp in SYNTAXERROR_EXPRESSIONS:
            PythonExpressionRule(exp)
    with pytest.raises(InvalidExpression):
        for exp in INVALID_EXPRESSIONS:
            PythonExpressionRule(exp)
    for exp in VALID_EXPRESSIONS:
        PythonExpressionRule(exp)
    rule = PythonExpressionRule(expression_rule)
    _test_rule_with_stats(rule)
