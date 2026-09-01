"""Regulatory compliance and financial risk auditing engine."""

from typing import TypedDict
from pydantic import BaseModel


class ComplianceAuditResult(BaseModel):
    verdict: str  # COMPLIANT, NON_COMPLIANT, ESCALATION_REQUIRED
    framework: str
    rules_evaluated: list[str]
    violations: list[str]
    risk_score: float  # 0.0 to 1.0
    recommended_action: str


class ComplianceRuleEngine:
    """Evaluates banking transactions and balance sheet metrics against regulatory frameworks."""

    @staticmethod
    def audit_basel_iii(
        cet1_capital: float,
        tier1_capital: float,
        total_capital: float,
        rwa: float,
    ) -> ComplianceAuditResult:
        """Audit bank capital adequacy against Basel III requirements."""
        cet1_ratio = (cet1_capital / rwa) * 100
        tier1_ratio = (tier1_capital / rwa) * 100
        total_ratio = (total_capital / rwa) * 100

        violations = []
        if cet1_ratio < 7.0:  # 4.5% min + 2.5% conservation buffer
            violations.append(f"CET1 ratio {cet1_ratio:.2f}% falls below 7.00% requirement (including buffer).")
        if tier1_ratio < 8.5:  # 6.0% min + 2.5% buffer
            violations.append(f"Tier 1 ratio {tier1_ratio:.2f}% falls below 8.50% requirement.")
        if total_ratio < 10.5:  # 8.0% min + 2.5% buffer
            violations.append(f"Total Capital ratio {total_ratio:.2f}% falls below 10.50% requirement.")

        if violations:
            verdict = "NON_COMPLIANT"
            risk_score = 0.85
            action = "Submit capital restoration plan to supervisory authority and curtail discretionary distributions."
        else:
            verdict = "COMPLIANT"
            risk_score = 0.10
            action = "Maintain standard capital monitoring and stress testing protocols."

        return ComplianceAuditResult(
            verdict=verdict,
            framework="Basel III Capital Framework (Pillar 1)",
            rules_evaluated=[
                "Common Equity Tier 1 (CET1) >= 7.00%",
                "Tier 1 Capital Ratio >= 8.50%",
                "Total Capital Adequacy Ratio >= 10.50%",
            ],
            violations=violations,
            risk_score=risk_score,
            recommended_action=action,
        )

    @staticmethod
    def audit_aml_structuring(deposit_amounts: list[float], days_span: int) -> ComplianceAuditResult:
        """Check for suspicious transaction structuring under the Bank Secrecy Act ($10k CTR limit)."""
        structuring_count = sum(1 for amt in deposit_amounts if 8500.0 <= amt < 10000.0)
        total_deposited = sum(deposit_amounts)

        violations = []
        if structuring_count >= 2 and days_span <= 5:
            violations.append(
                f"Detected {structuring_count} transactions just below $10,000 threshold within {days_span} days (Total: ${total_deposited:,.2f})."
            )

        if violations:
            return ComplianceAuditResult(
                verdict="ESCALATION_REQUIRED",
                framework="Bank Secrecy Act (BSA) / AML 31 CFR 1010.314",
                rules_evaluated=["Anti-Structuring Monitoring (Amounts between $8,500 and $9,999)"],
                violations=violations,
                risk_score=0.92,
                recommended_action="File FinCEN Form 111 (Suspicious Activity Report - SAR) and initiate enhanced AML investigation.",
            )

        return ComplianceAuditResult(
            verdict="COMPLIANT",
            framework="Bank Secrecy Act (BSA) / AML 31 CFR 1010.314",
            rules_evaluated=["Anti-Structuring Monitoring"],
            violations=[],
            risk_score=0.05,
            recommended_action="Standard transaction processing.",
        )
