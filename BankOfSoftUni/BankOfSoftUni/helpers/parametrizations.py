ALLOWED_CURRENCIES = {
    'BGN': 1,
    'USD': 1.7891,
    'CHF': 1.9324,
    'GBP': 2.3541,
    'JPY': 0.0143,
}

LOAN_INTEREST_RATES_BASED_ON_PRINCIPAL_MIN_THRESHOLD_BGN = {
    10000: 3.50,
    100000: 3.25,
    250000: 3.00,
    350000: 2.75,
    450000: 2.50,
}

# Deduct from interest rate if duration is greater than the key
LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION = {
    12: 0,
    60: 0,
    120: 0.1,
    240: 0.1,
}