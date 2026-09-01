"""Financial mathematics calculator scaffold.

💡 Learning Concepts & References:
1. CAGR (Compound Annual Growth Rate):
   - The smoothed annual growth rate of an investment over multiple years.
   - Formula: CAGR = (Ending Value / Beginning Value) ^ (1 / n) - 1
   - 📖 Investopedia: https://www.investopedia.com/terms/c/cagr.asp

2. WACC (Weighted Average Cost of Capital):
   - The average rate of return a company must earn on its existing asset base to satisfy debt & equity holders.
   - Formula: WACC = (E/V * Re) + (D/V * Rd * (1 - TaxRate))
   - 📖 Investopedia: https://www.investopedia.com/terms/w/wacc.asp

3. DuPont Analysis (3-Stage ROE):
   - Breaks down Return on Equity into 3 components: Profit Margin * Asset Turnover * Leverage Multiplier.
   - 📖 Investopedia: https://www.investopedia.com/terms/d/dupontanalysis.asp
"""

class FinancialMath:
    """Calculates corporate finance ratios and valuation metrics."""

    @staticmethod
    def calculate_cagr(start_val: float, end_val: float, years: int) -> float:
        """Compute Compound Annual Growth Rate (CAGR)."""
        if start_val <= 0 or years <= 0:
            raise ValueError("Start value and years must be greater than zero.")
        return ((end_val / start_val) ** (1 / years)) - 1.0

    @staticmethod
    def calculate_wacc(
        equity_val: float,
        debt_val: float,
        cost_of_equity: float,
        cost_of_debt: float,
        tax_rate: float = 0.21,
    ) -> float:
        """Compute Weighted Average Cost of Capital (WACC)."""
        total = equity_val + debt_val
        if total <= 0:
            raise ValueError("Total firm value (Equity + Debt) must be positive.")
        we = equity_val / total
        wd = debt_val / total
        after_tax_rd = cost_of_debt * (1 - tax_rate)
        return (we * cost_of_equity) + (wd * after_tax_rd)
