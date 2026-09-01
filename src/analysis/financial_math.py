"""Quantitative financial math engine for DCF, WACC, DuPont analysis, and corporate ratios."""

from src.core.schemas import MathComputationResult


class FinancialCalculator:
    """Computes verified quantitative corporate finance metrics with step-by-step reasoning."""

    @staticmethod
    def calculate_wacc(
        cost_of_equity: float,
        cost_of_debt: float,
        equity_value: float,
        debt_value: float,
        tax_rate: float = 0.21,
    ) -> MathComputationResult:
        """Compute Weighted Average Cost of Capital (WACC)."""
        total_val = equity_value + debt_value
        we = equity_value / total_val
        wd = debt_value / total_val
        after_tax_rd = cost_of_debt * (1 - tax_rate)
        wacc = (we * cost_of_equity) + (wd * after_tax_rd)

        steps = [
            f"1. Total Capital (V) = Equity (${equity_value:,.2f}) + Debt (${debt_value:,.2f}) = ${total_val:,.2f}",
            f"2. Equity Weight (We) = {we:.4f} ({we*100:.2f}%), Debt Weight (Wd) = {wd:.4f} ({wd*100:.2f}%)",
            f"3. After-tax Cost of Debt = {cost_of_debt:.4f} * (1 - {tax_rate}) = {after_tax_rd:.4f} ({after_tax_rd*100:.2f}%)",
            f"4. WACC = ({we:.4f} * {cost_of_equity:.4f}) + ({wd:.4f} * {after_tax_rd:.4f}) = {wacc:.4f} ({wacc*100:.2f}%)",
        ]

        return MathComputationResult(
            metric_name="Weighted Average Cost of Capital (WACC)",
            formula="WACC = (E/V * Re) + (D/V * Rd * (1 - T))",
            steps=steps,
            inputs={
                "cost_of_equity": cost_of_equity,
                "cost_of_debt": cost_of_debt,
                "equity_value": equity_value,
                "debt_value": debt_value,
                "tax_rate": tax_rate,
            },
            result=round(wacc * 100, 2),
            interpretation=f"The firm's hurdle rate / cost of capital is {wacc*100:.2f}%. Any new capital project must yield a return exceeding this hurdle.",
        )

    @staticmethod
    def calculate_dupont_roe(
        net_income: float,
        sales: float,
        total_assets: float,
        shareholders_equity: float,
    ) -> MathComputationResult:
        """Compute 3-Stage DuPont ROE Decomposition: Net Profit Margin * Asset Turnover * Financial Leverage."""
        npm = net_income / sales
        asset_turnover = sales / total_assets
        leverage = total_assets / shareholders_equity
        roe = npm * asset_turnover * leverage

        steps = [
            f"1. Net Profit Margin = Net Income (${net_income:,.2f}) / Sales (${sales:,.2f}) = {npm:.4f} ({npm*100:.2f}%)",
            f"2. Asset Turnover = Sales (${sales:,.2f}) / Total Assets (${total_assets:,.2f}) = {asset_turnover:.4f}x",
            f"3. Equity Multiplier (Financial Leverage) = Total Assets (${total_assets:,.2f}) / Equity (${shareholders_equity:,.2f}) = {leverage:.4f}x",
            f"4. DuPont ROE = {npm:.4f} * {asset_turnover:.4f} * {leverage:.4f} = {roe:.4f} ({roe*100:.2f}%)",
        ]

        return MathComputationResult(
            metric_name="DuPont 3-Stage Return on Equity (ROE)",
            formula="ROE = Net Profit Margin * Asset Turnover * Equity Multiplier",
            steps=steps,
            inputs={
                "net_income": net_income,
                "sales": sales,
                "total_assets": total_assets,
                "shareholders_equity": shareholders_equity,
            },
            result=round(roe * 100, 2),
            interpretation=f"The company generates an ROE of {roe*100:.2f}%, driven by profit efficiency ({npm*100:.2f}%), asset productivity ({asset_turnover:.2f}x), and capital leverage ({leverage:.2f}x).",
        )

    @staticmethod
    def calculate_cagr(
        beginning_value: float,
        ending_value: float,
        years: int,
    ) -> MathComputationResult:
        """Compute Compound Annual Growth Rate (CAGR)."""
        cagr = ((ending_value / beginning_value) ** (1 / years)) - 1.0

        steps = [
            f"1. Growth Multiple = Ending Value (${ending_value:,.2f}) / Beginning Value (${beginning_value:,.2f}) = {ending_value/beginning_value:.4f}",
            f"2. Annualized Exponent = 1 / {years} = {1/years:.4f}",
            f"3. CAGR = ({ending_value/beginning_value:.4f}) ^ ({1/years:.4f}) - 1 = {cagr:.4f} ({cagr*100:.2f}%)",
        ]

        return MathComputationResult(
            metric_name="Compound Annual Growth Rate (CAGR)",
            formula="CAGR = (Ending Value / Beginning Value) ^ (1 / n) - 1",
            steps=steps,
            inputs={
                "beginning_value": beginning_value,
                "ending_value": ending_value,
                "years": float(years),
            },
            result=round(cagr * 100, 2),
            interpretation=f"Annualized geometric growth rate over {years} periods is {cagr*100:.2f}%.",
        )
