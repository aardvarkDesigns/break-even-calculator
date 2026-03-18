"""Break-even purchase price estimator — Streamlit app."""
from __future__ import annotations
import streamlit as st


def calculate_payment(
    purchase_price: float,
    renovation_cost: float,
    down_payment_pct: float,
    loan_term_yrs: float,
    interest_rate_pct: float,
) -> int:
    """Estimate the monthly mortgage payment."""
    total_project_cost = purchase_price + renovation_cost
    principal = total_project_cost * (1 - down_payment_pct / 100.0)
    monthly_interest = interest_rate_pct / 12.0 / 100.0
    months = loan_term_yrs * 12.0
    if months <= 0:
        raise ValueError("loan_term_yrs must be greater than 0")
    if monthly_interest == 0:
        return int(principal / months)
    payment = principal * (
        monthly_interest / (1 - (1 + monthly_interest) ** (-months))
    )
    return int(payment)


def break_even_price(
    income_mo: float,
    fees_mo: float,
    profit_pct: float,
    renovation_cost: float,
    down_payment_pct: float,
    loan_term_yrs: float,
    interest_rate_pct: float,
    real_estate_tax_pct: float,
    insurance_yr: float,
    management_pct: float,
    error_max: float = 5.0,
) -> int:
    """Return the estimated purchase price that breaks even."""
    purchase_price = 100_000.0
    income_yr = income_mo * 12.0
    fees_yr = fees_mo * 12.0
    profit_yr = profit_pct / 100.0 * income_yr
    management_yr = management_pct / 100.0 * income_yr
    error = float("inf")
    iterations = 0
    while abs(error) >= error_max:
        payment_mo = calculate_payment(
            purchase_price,
            renovation_cost,
            down_payment_pct,
            loan_term_yrs,
            interest_rate_pct,
        )
        payment_yr = payment_mo * 12.0
        total_project_cost = purchase_price + renovation_cost
        real_estate_tax_yr = real_estate_tax_pct / 100.0 * total_project_cost
        cost_sum = (
            payment_yr
            + fees_yr
            + profit_yr
            + management_yr
            + real_estate_tax_yr
            + insurance_yr
        )
        error = income_yr - cost_sum
        purchase_price = purchase_price + error / 2.0
        iterations += 1
        if purchase_price <= 0:
            raise ValueError("Inputs do not produce a positive purchase price.")
        if iterations > 10_000:
            raise RuntimeError("Break-even calculation did not converge.")
    return round(purchase_price)


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Break-Even Price Estimator | KW VIP", page_icon="🏠")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Montserrat', sans-serif;
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* Force white background on all Streamlit containers */
.stApp, .main, section[data-testid="stSidebar"],
div[data-testid="stAppViewContainer"],
div[data-testid="stHeader"] {
    background-color: #FFFFFF !important;
}

/* Input fields */
input[type="number"], .stNumberInput input {
    background-color: #f8f9ff !important;
    color: #000000 !important;
    border: 1px solid #dde3ff !important;
    font-weight: 600 !important;
}

/* Input labels */
label, .stNumberInput label, div[data-testid="stWidgetLabel"] p {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* Expander */
div[data-testid="stExpander"] {
    background-color: #f8f9ff !important;
    border: 1px solid #dde3ff !important;
    border-radius: 6px;
}

/* Breakdown rows on white background */
.kw-breakdown-label { color: #000000 !important; }

/* Header bar */
.kw-header {
    background-color: #2557FF;
    padding: 18px 28px;
    border-radius: 8px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.kw-header-title {
    color: #FFFFFF !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    margin: 0;
    line-height: 1.2;
}
.kw-header-sub {
    color: rgba(255,255,255,0.75);
    font-size: 11px;
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 0;
}

/* Section labels */
h2, h3 {
    font-family: 'Montserrat', sans-serif !important;
    color: #2557FF !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px;
}

/* Divider accent */
hr {
    border-color: #2557FF !important;
    opacity: 0.2;
}

/* Result box */
.kw-result {
    background-color: #2557FF;
    color: #FFFFFF;
    padding: 24px 32px;
    border-radius: 8px;
    text-align: center;
    margin-top: 8px;
}
.kw-result-label {
    font-size: 13px;
    font-weight: 300;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.85;
    margin-bottom: 6px;
}
.kw-result-price {
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -1px;
    margin-bottom: 4px;
}
.kw-result-sub {
    font-size: 14px;
    font-weight: 400;
    opacity: 0.80;
    margin-top: 6px;
    letter-spacing: 0.5px;
}

/* Breakdown rows */
.kw-breakdown-row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f0;
    font-size: 14px;
}
.kw-breakdown-row:last-child { border-bottom: none; }
.kw-breakdown-label { color: #000000; font-weight: 500; }
.kw-breakdown-value { color: #2557FF; font-weight: 600; }

/* Primary button override */
div.stButton > button[kind="primary"] {
    background-color: #2557FF !important;
    border-color: #2557FF !important;
    color: #FFFFFF !important;
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
    border-radius: 6px;
    padding: 10px 0;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #1a44e0 !important;
    border-color: #1a44e0 !important;
}
</style>

<div class="kw-header">
  <div>
    <p class="kw-header-title">Break-Even Purchase Price Estimator</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("Enter your property details below to estimate the maximum purchase price at which the investment breaks even.")

# ── Inputs ───────────────────────────────────────────────────────────────────
st.subheader("Income & Expenses")
col1, col2 = st.columns(2)
with col1:
    income_mo = st.number_input("Monthly Rental Income ($)", min_value=0.0, value=2_000.0, step=50.0)
    fees_mo = st.number_input("Monthly Fees (HOA, etc.) ($)", min_value=0.0, value=0.0, step=10.0)
    profit_pct = st.number_input("Annual Rent Profit Percentage", min_value=0.0, max_value=100.0, value=5.0, step=0.5)
with col2:
    management_pct = st.number_input("Property Management (% of annual income)", min_value=0.0, max_value=100.0, value=8.0, step=0.5)
    insurance_yr = st.number_input("Annual Insurance ($)", min_value=0.0, value=1_200.0, step=100.0)
    renovation_cost = st.number_input("Renovation Cost ($)", min_value=0.0, value=15_000.0, step=1_000.0)

st.subheader("Loan Parameters")
col3, col4 = st.columns(2)
with col3:
    down_payment_pct = st.number_input("Down Payment (%)", min_value=0.0, max_value=100.0, value=25.0, step=1.0)
    loan_term_yrs = st.number_input("Loan Term (years)", min_value=1.0, max_value=40.0, value=30.0, step=1.0)
with col4:
    interest_rate_pct = st.number_input("Annual Interest Rate (%)", min_value=0.0, max_value=30.0, value=6.0, step=0.125)
    real_estate_tax_pct = st.number_input("Real Estate Tax (% of total project cost)", min_value=0.0, max_value=10.0, value=0.5, step=0.05)

# ── Calculate ─────────────────────────────────────────────────────────────────
st.divider()
if st.button("Calculate Break-Even Price", type="primary", use_container_width=True):
    try:
        result = break_even_price(
            income_mo=income_mo,
            fees_mo=fees_mo,
            profit_pct=profit_pct,
            renovation_cost=renovation_cost,
            down_payment_pct=down_payment_pct,
            loan_term_yrs=loan_term_yrs,
            interest_rate_pct=interest_rate_pct,
            real_estate_tax_pct=real_estate_tax_pct,
            insurance_yr=insurance_yr,
            management_pct=management_pct,
        )
        payment_mo = calculate_payment(
            result, renovation_cost, down_payment_pct, loan_term_yrs, interest_rate_pct
        )
        st.markdown(f"""
<div class="kw-result">
  <p class="kw-result-label">Break-Even Purchase Price</p>
  <p class="kw-result-price">${result:,.0f}</p>
  <p class="kw-result-sub">Monthly Debt Service: ${payment_mo:,}</p>
</div>
""", unsafe_allow_html=True)

        # ── Cost breakdown ────────────────────────────────────────────────────
        with st.expander("See annual cost breakdown"):
            income_yr = income_mo * 12
            total_project_cost = result + renovation_cost
            rows = {
                "Gross Annual Income": income_yr,
                "Monthly Debt Service": payment_mo,
                "Annual Debt Service": payment_mo * 12,
                "Annual Fees": fees_mo * 12,
                "Target Profit": profit_pct / 100 * income_yr,
                "Property Management": management_pct / 100 * income_yr,
                "Real Estate Tax": real_estate_tax_pct / 100 * total_project_cost,
                "Insurance": insurance_yr,
            }
            breakdown_html = "".join(
                f'<div class="kw-breakdown-row">'
                f'<span class="kw-breakdown-label">{label}</span>'
                f'<span class="kw-breakdown-value">${value:,.0f}</span>'
                f'</div>'
                for label, value in rows.items()
            )
            st.markdown(breakdown_html, unsafe_allow_html=True)

    except (ValueError, RuntimeError) as exc:
        st.error(str(exc))

st.markdown("""
<div style="margin-top: 48px; padding-top: 16px; border-top: 1px solid #dde3ff;
            text-align: center; font-size: 12px; color: #444; font-weight: 400;">
    <p style="margin-bottom: 8px;">
        <a href="https://www.lasvegasrealestateinvestmentgroup.com/limitationOfLiability.html"
           target="_blank" style="color: #2557FF; text-decoration: underline;">
            License and Disclaimer: By choosing to use this tool and or information, you are agreeing to the terms on the license page.
        </a>
    </p>
    &copy; 2005 to 2026 Cleo Li and Eric Fernwood, all rights reserved.
</div>
""", unsafe_allow_html=True)
