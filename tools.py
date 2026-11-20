"""Financial calculation tools exposed for multi-agent financial advisory."""

import os
import sys

# Temporarily unregister any shadowing to import installed OpenAI Agents SDK
_our_mod = sys.modules.get("agents")
if "agents" in sys.modules:
    del sys.modules["agents"]

_cur_dir = os.path.abspath(os.path.dirname(__file__))
_saved_paths = [p for p in sys.path if os.path.abspath(p) == _cur_dir or p == ""]
for p in _saved_paths:
    sys.path.remove(p)

import agents as _sdk_agents

for p in reversed(_saved_paths):
    sys.path.insert(0, p)

if _our_mod:
    sys.modules["agents"] = _our_mod

function_tool = _sdk_agents.function_tool

# Mock exchange rates for currency pairs
MOCK_EXCHANGE_RATES = {
    "USD/INR": 86.50,
    "EUR/INR": 90.20,
    "GBP/INR": 108.40,
}


def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    """Calculate the Equated Monthly Installment (EMI) for a loan using the standard formula.

    Formula: EMI = [P * r * (1 + r)^n] / [(1 + r)^n - 1]
    where P = principal, r = monthly interest rate, n = tenure in months.

    Args:
        principal: Total loan principal amount.
        annual_rate: Annual interest rate as a percentage (e.g., 9.5 for 9.5%).
        tenure_months: Total loan tenure duration in months.

    Returns:
        The calculated monthly EMI rounded to 2 decimal places.
    """
    if principal <= 0 or tenure_months <= 0:
        return 0.0
    if annual_rate <= 0:
        return round(principal / tenure_months, 2)

    monthly_rate = (annual_rate / 12.0) / 100.0
    growth_factor = (1.0 + monthly_rate) ** tenure_months
    emi = (principal * monthly_rate * growth_factor) / (growth_factor - 1.0)
    return round(emi, 2)


def calculate_returns(amount: float, annual_rate: float, years: float) -> float:
    """Calculate compound interest returns and return the final investment value.

    Formula: A = P * (1 + r / 100)^t
    where P = amount, r = annual interest rate, t = time in years.

    Args:
        amount: Initial investment principal amount.
        annual_rate: Annual expected return rate as a percentage (e.g., 12.0 for 12%).
        years: Number of years the amount is invested.

    Returns:
        The final investment value rounded to 2 decimal places.
    """
    if amount <= 0 or years <= 0:
        return float(amount)

    rate_factor = annual_rate / 100.0
    final_value = amount * ((1.0 + rate_factor) ** years)
    return round(final_value, 2)


def get_exchange_rate(pair: str) -> str:
    """Look up currency exchange rate from the mock exchange rate database.

    Args:
        pair: Currency pair string (e.g., 'USD/INR', 'EUR/INR', 'GBP/INR').

    Returns:
        A string describing the exchange rate or available pairs if not found.
    """
    clean_pair = pair.strip().upper()
    rate = MOCK_EXCHANGE_RATES.get(clean_pair)
    if rate is not None:
        return f"1 {clean_pair.split('/')[0]} = {rate} {clean_pair.split('/')[1]}"
    return f"Exchange rate for '{pair}' not found. Available pairs: {list(MOCK_EXCHANGE_RATES.keys())}"


# Exposed as tools for agent use
calculate_emi_tool = function_tool(calculate_emi)
calculate_returns_tool = function_tool(calculate_returns)
get_exchange_rate_tool = function_tool(get_exchange_rate)
