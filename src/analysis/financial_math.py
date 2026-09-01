"""Financial mathematics calculator scaffold."""

class FinancialMath:
    """Calculates corporate finance ratios and valuation metrics."""

    @staticmethod
    def calculate_cagr(start_val: float, end_val: float, years: int) -> float:
        """Compute Compound Annual Growth Rate (CAGR)."""
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
        we = equity_val / total
        wd = debt_val / total
        after_tax_rd = cost_of_debt * (1 - tax_rate)
        return (we * cost_of_equity) + (wd * after_tax_rd)
