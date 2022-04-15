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
LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION_YEARS = {
    1: 0,
    5: 0,
    10: 0.1,
    20: 0.1,
}

# The monthly income of the client cannot exceed the monthly payment of
# the loan - this variable determines what percentage of the income can be used for
# loan payment

MAX_INCOME_SHARE_AS_MONTHLY_LOAN_PAYMENT = 0.60

MAX_LOAN_DURATION_YEARS = 30
MAX_LOAN_PRINCIPAL = 500000
MIN_LOAN_PRINCIPAL = 1000

CUSTOMER_MAX_LOAN_EXPOSITION = 500000
