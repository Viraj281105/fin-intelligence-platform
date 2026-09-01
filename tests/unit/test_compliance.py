"""Unit tests for compliance and regulatory auditing engine."""

from src.analysis.compliance import ComplianceRuleEngine


def test_basel_iii_compliant():
    res = ComplianceRuleEngine.audit_basel_iii(
        cet1_capital=100.0,
        tier1_capital=120.0,
        total_capital=150.0,
        rwa=1000.0,
    )
    assert res.verdict == "COMPLIANT"
    assert len(res.violations) == 0
    assert res.risk_score <= 0.2


def test_basel_iii_non_compliant():
    res = ComplianceRuleEngine.audit_basel_iii(
        cet1_capital=50.0,  # 5% < 7% buffer threshold
        tier1_capital=60.0,
        total_capital=70.0,
        rwa=1000.0,
    )
    assert res.verdict == "NON_COMPLIANT"
    assert len(res.violations) >= 1
    assert res.risk_score >= 0.7


def test_aml_structuring_alert():
    deposits = [9800.0, 9900.0, 9850.0]
    res = ComplianceRuleEngine.audit_aml_structuring(deposits, days_span=3)
    assert res.verdict == "ESCALATION_REQUIRED"
    assert res.risk_score > 0.8
