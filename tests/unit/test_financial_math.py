"""Unit tests for quantitative financial math operations."""

from src.analysis.financial_math import FinancialCalculator


def test_wacc_calculation():
    res = FinancialCalculator.calculate_wacc(
        cost_of_equity=0.10,
        cost_of_debt=0.05,
        equity_value=600000.0,
        debt_value=400000.0,
        tax_rate=0.20,
    )
    # Total = 1,000,000. We = 0.60, Wd = 0.40.
    # After tax debt = 0.05 * 0.80 = 0.04.
    # WACC = (0.60 * 0.10) + (0.40 * 0.04) = 0.06 + 0.016 = 0.076 = 7.6%
    assert res.result == 7.6
    assert len(res.steps) == 4
    assert res.inputs["tax_rate"] == 0.20


def test_cagr_calculation():
    res = FinancialCalculator.calculate_cagr(
        beginning_value=100.0,
        ending_value=200.0,
        years=3,
    )
    # 2 ^ (1/3) - 1 = 1.25992 - 1 = 25.99%
    assert res.result == 25.99


def test_dupont_roe():
    res = FinancialCalculator.calculate_dupont_roe(
        net_income=15000.0,
        sales=100000.0,
        total_assets=200000.0,
        shareholders_equity=50000.0,
    )
    # NPM = 15/100 = 15%, Asset Turnover = 100/200 = 0.5x, Leverage = 200/50 = 4.0x
    # ROE = 0.15 * 0.5 * 4.0 = 0.30 = 30.0%
    assert res.result == 30.0
