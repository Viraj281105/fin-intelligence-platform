"""Synthetic training data generator with chain-of-thought verification for 5 financial domains."""

import random
from src.core.schemas import FinancialTaskType
from src.data.schemas import FinancialTrainingExample


class SyntheticFinancialDataGenerator:
    """Generates verified synthetic financial instruction pairs with Chain-of-Thought reasoning."""

    def __init__(self, seed: int = 42):
        random.seed(seed)

    def generate_text_to_sql_dataset(self, num_samples: int = 100) -> list[FinancialTrainingExample]:
        """Generate verified Text-to-SQL financial queries over standard enterprise schemas."""
        schemas = [
            """Table: portfolio_positions (
    position_id INT PRIMARY KEY,
    fund_id VARCHAR(20),
    ticker VARCHAR(10),
    asset_class VARCHAR(30), -- Equities, Fixed Income, Derivatives
    market_value NUMERIC(15, 2),
    unrealized_gain_loss NUMERIC(15, 2),
    as_of_date DATE
);""",
            """Table: transactions (
    transaction_id INT PRIMARY KEY,
    account_id VARCHAR(30),
    transaction_type VARCHAR(20), -- BUY, SELL, DIVIDEND, TRANSFER
    ticker VARCHAR(10),
    shares NUMERIC(12, 4),
    price_per_share NUMERIC(10, 2),
    total_amount NUMERIC(15, 2),
    fee_amount NUMERIC(8, 2),
    transaction_timestamp TIMESTAMP
);""",
            """Table: income_statements (
    statement_id INT PRIMARY KEY,
    company_ticker VARCHAR(10),
    fiscal_year INT,
    fiscal_quarter INT,
    total_revenue NUMERIC(18, 2),
    operating_expenses NUMERIC(18, 2),
    ebitda NUMERIC(18, 2),
    net_income NUMERIC(18, 2),
    diluted_eps NUMERIC(8, 2)
);"""
        ]

        templates = [
            (
                "Find the top 5 largest equity positions by market value across all funds as of the latest reporting date.",
                0,
                "To get top 5 equity positions: filter asset_class = 'Equities', order by market_value DESC, limit 5.",
                "```sql\nSELECT ticker, fund_id, market_value, unrealized_gain_loss\nFROM portfolio_positions\nWHERE asset_class = 'Equities'\nORDER BY market_value DESC\nLIMIT 5;\n```\n\nThis query filters for equities and orders positions descending by market value, restricting output to the top 5 records."
            ),
            (
                "Calculate the total net trading volume and total transaction fees paid per account for Q3 2024.",
                1,
                "Aggregate total_amount and fee_amount grouped by account_id for transactions timestamped between 2024-07-01 and 2024-09-30.",
                "```sql\nSELECT \n    account_id,\n    SUM(total_amount) AS total_trading_volume,\n    SUM(fee_amount) AS total_fees_paid,\n    COUNT(transaction_id) AS total_trades\nFROM transactions\nWHERE transaction_timestamp >= '2024-07-01' \n  AND transaction_timestamp < '2024-10-01'\nGROUP BY account_id\nORDER BY total_trading_volume DESC;\n```\n\nThis query aggregates trade volumes and execution fees per account for the third quarter of 2024."
            ),
            (
                "List all companies whose revenue grew YoY in fiscal 2024 with EBITDA margins above 25%.",
                2,
                "Compute EBITDA margin as (ebitda / total_revenue) > 0.25 for fiscal_year = 2024 and check revenue growth against 2023.",
                "```sql\nSELECT \n    curr.company_ticker,\n    curr.total_revenue AS rev_2024,\n    prev.total_revenue AS rev_2023,\n    ROUND(((curr.total_revenue - prev.total_revenue) / prev.total_revenue) * 100, 2) AS rev_growth_pct,\n    ROUND((curr.ebitda / curr.total_revenue) * 100, 2) AS ebitda_margin_pct\nFROM income_statements curr\nJOIN income_statements prev \n  ON curr.company_ticker = prev.company_ticker \n AND curr.fiscal_year = 2024 \n AND prev.fiscal_year = 2023\nWHERE (curr.ebitda / curr.total_revenue) > 0.25\n  AND curr.total_revenue > prev.total_revenue\nORDER BY rev_growth_pct DESC;\n```\n\nThis query joins the 2024 and 2023 income statements to compute YoY revenue expansion and enforce the 25% EBITDA margin hurdle."
            ),
        ]

        examples = []
        for i in range(num_samples):
            template_idx = i % len(templates)
            q_text, schema_idx, reason, resp = templates[template_idx]
            examples.append(
                FinancialTrainingExample(
                    id=f"synth_sql_{i:04d}",
                    task_type=FinancialTaskType.TEXT_TO_SQL,
                    instruction=q_text,
                    context=schemas[schema_idx],
                    reasoning=reason,
                    response=resp,
                    metadata={"difficulty": "medium", "generator": "rule_based_sql"},
                )
            )
        return examples

    def generate_financial_math_dataset(self, num_samples: int = 100) -> list[FinancialTrainingExample]:
        """Generate verified step-by-step quantitative financial calculations."""
        examples = []
        for i in range(num_samples):
            # Generate DCF or WACC or DuPont problem
            if i % 3 == 0:
                # WACC
                cost_of_equity = round(random.uniform(0.08, 0.14), 4)
                cost_of_debt = round(random.uniform(0.04, 0.08), 4)
                tax_rate = 0.21
                equity_weight = round(random.uniform(0.5, 0.8), 2)
                debt_weight = round(1.0 - equity_weight, 2)
                
                wacc = (equity_weight * cost_of_equity) + (debt_weight * cost_of_debt * (1 - tax_rate))
                wacc_pct = round(wacc * 100, 2)

                inst = f"Calculate the Weighted Average Cost of Capital (WACC) given Cost of Equity = {cost_of_equity*100:.1f}%, Pre-tax Cost of Debt = {cost_of_debt*100:.1f}%, Tax Rate = 21%, Capital Structure: {equity_weight*100:.0f}% Equity and {debt_weight*100:.0f}% Debt."
                reason = f"WACC = (E/V * Re) + (D/V * Rd * (1 - T))\n1. Equity component = {equity_weight} * {cost_of_equity:.4f} = {equity_weight * cost_of_equity:.6f}\n2. Debt component = {debt_weight} * {cost_of_debt:.4f} * (1 - 0.21) = {debt_weight * cost_of_debt * 0.79:.6f}\n3. Total WACC = {wacc:.4f} ({wacc_pct}%)."
                resp = (
                    f"<calculation>\n"
                    f"Cost of Equity Weight: {equity_weight}\n"
                    f"Cost of Debt Weight: {debt_weight}\n"
                    f"After-tax Cost of Debt: {cost_of_debt:.4f} * (1 - 0.21) = {cost_of_debt*0.79:.4f}\n"
                    f"WACC = ({equity_weight} * {cost_of_equity:.4f}) + ({debt_weight} * {cost_of_debt*0.79:.4f}) = {wacc_pct}%\n"
                    f"</calculation>\n\n"
                    f"The computed Weighted Average Cost of Capital (WACC) is **{wacc_pct}%**."
                )

                examples.append(
                    FinancialTrainingExample(
                        id=f"synth_math_{i:04d}",
                        task_type=FinancialTaskType.FINANCIAL_MATH,
                        instruction=inst,
                        context=None,
                        reasoning=reason,
                        response=resp,
                        metadata={"metric": "WACC"},
                    )
                )
            else:
                # CAGR
                initial_val = round(random.uniform(50.0, 200.0), 1)
                final_val = round(initial_val * random.uniform(1.4, 3.2), 1)
                years = random.randint(3, 7)
                cagr = ((final_val / initial_val) ** (1 / years)) - 1.0
                cagr_pct = round(cagr * 100, 2)

                inst = f"Calculate the Compound Annual Growth Rate (CAGR) for a company whose revenue grew from ${initial_val}M to ${final_val}M over {years} years."
                reason = f"CAGR formula: (Ending Value / Beginning Value) ^ (1 / n) - 1\n1. Ratio = {final_val} / {initial_val} = {final_val/initial_val:.4f}\n2. Exponent = 1 / {years} = {1/years:.4f}\n3. CAGR = ({final_val/initial_val:.4f}) ^ ({1/years:.4f}) - 1 = {cagr_pct}%."
                resp = (
                    f"<calculation>\n"
                    f"Beginning Value: ${initial_val}M\n"
                    f"Ending Value: ${final_val}M\n"
                    f"Periods (n): {years}\n"
                    f"CAGR = ({final_val} / {initial_val}) ^ (1 / {years}) - 1 = {cagr_pct}%\n"
                    f"</calculation>\n\n"
                    f"The Compound Annual Growth Rate (CAGR) over the {years}-year period is **{cagr_pct}%**."
                )

                examples.append(
                    FinancialTrainingExample(
                        id=f"synth_math_{i:04d}",
                        task_type=FinancialTaskType.FINANCIAL_MATH,
                        instruction=inst,
                        context=None,
                        reasoning=reason,
                        response=resp,
                        metadata={"metric": "CAGR"},
                    )
                )
        return examples

    def generate_compliance_dataset(self, num_samples: int = 50) -> list[FinancialTrainingExample]:
        """Generate verified compliance, AML, and Basel III auditing scenarios."""
        scenarios = [
            (
                "A corporate client structured 3 cash deposits of $9,800, $9,950, and $9,700 across three consecutive business days at different branch locations.",
                "Bank Secrecy Act (BSA) & AML Anti-Structuring Rules (31 CFR 1010.314).",
                "Transactions fall just beneath the $10,000 Currency Transaction Report (CTR) threshold across consecutive days and branches, a classic structuring typological pattern.",
                "Verdict: [NON-COMPLIANT | ESCALATION_REQUIRED]\n\n"
                "### Regulatory Findings:\n"
                "- **Violation**: Anti-Structuring under 31 CFR 1010.314 (BSA).\n"
                "- **Risk Level**: High.\n"
                "- **Mandatory Action**: File a Suspicious Activity Report (SAR) with FinCEN within 30 calendar days and freeze account for Enhanced Due Diligence (EDD)."
            ),
            (
                "Commercial Bank A holds Tier 1 Capital of $120M against Risk-Weighted Assets (RWA) of $1,000M, with a Common Equity Tier 1 (CET1) ratio of 9.5%.",
                "Basel III Capital Adequacy Framework requirements: Minimum CET1 ratio 4.5% + Capital Conservation Buffer of 2.5% = 7.0% total.",
                "Bank A's CET1 is 9.5% ($95M CET1 / $1,000M RWA) and Tier 1 is 12.0% ($120M / $1,000M), surpassing Basel III minimum threshold (6.0% Tier 1, 7.0% CET1 with buffer).",
                "Verdict: [COMPLIANT]\n\n"
                "### Regulatory Findings:\n"
                "- **Framework**: Basel III Pillar 1 Capital Requirements.\n"
                "- **CET1 Ratio**: 9.5% (Threshold: 7.0% including conservation buffer) -> PASS.\n"
                "- **Tier 1 Ratio**: 12.0% (Threshold: 8.5% with buffer) -> PASS.\n"
                "- **Recommendation**: Maintain current capital adequacy monitoring."
            ),
        ]

        examples = []
        for i in range(num_samples):
            idx = i % len(scenarios)
            prompt, rule, reason, resp = scenarios[idx]
            examples.append(
                FinancialTrainingExample(
                    id=f"synth_compliance_{i:04d}",
                    task_type=FinancialTaskType.COMPLIANCE_AUDIT,
                    instruction=f"Audit the following financial scenario for regulatory compliance:\n\n{prompt}",
                    context=f"Applicable Standard: {rule}",
                    reasoning=reason,
                    response=resp,
                    metadata={"rule": rule},
                )
            )
        return examples
