"""Regulatory compliance auditing scaffold.

💡 Learning Concepts & References:
1. Basel III Framework:
   - International regulatory accord for banks established after the 2008 financial crisis.
   - Mandates minimum Common Equity Tier 1 (CET1) capital ratio of 4.5% + 2.5% conservation buffer = 7.00%.
   - 📖 Investopedia: https://www.investopedia.com/terms/b/basell-iii.asp
   - 📖 Bank for International Settlements: https://www.bis.org/bcbs/basel3.htm

2. Bank Secrecy Act (BSA) & Anti-Money Laundering (AML):
   - Mandates reporting of cash transactions exceeding $10,000 via Currency Transaction Reports (CTR).
   - "Structuring" (breaking deposits into $9,500 chunks to evade CTR limits) is illegal under 31 CFR 1010.314.
   - 📖 FinCEN BSA Overview: https://www.fincen.gov/resources/statutes-regulations
"""


class ComplianceChecker:
    """Evaluates regulatory rules such as Basel III capital ratios and AML transaction limits."""

    @staticmethod
    def check_basel_iii(cet1_ratio: float) -> bool:
        """Verify if Common Equity Tier 1 (CET1) satisfies the 7.00% minimum threshold with conservation buffer."""
        return cet1_ratio >= 7.0

    @staticmethod
    def check_aml_structuring(deposit_amounts: list[float], days: int) -> bool:
        """Flag suspicious structuring if multiple deposits are between $8,500 and $9,999 in <= 5 days."""
        flagged = sum(1 for a in deposit_amounts if 8500.0 <= a < 10000.0)
        return flagged >= 2 and days <= 5
