# TO DO - get currency rates daily
from BankOfSoftUni.helpers.parametrizations import ALLOWED_CURRENCIES, \
    LOAN_INTEREST_RATES_BASED_ON_PRINCIPAL_MIN_THRESHOLD_BGN, LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION


def calc_foreign_currency_to_BGN(value, currency):
    return value * ALLOWED_CURRENCIES[currency]


def calc_loan_interest_rate(principal, period):
    interest_rate = 0
    # Calculate interest based on principal
    for threshold, i_rate in LOAN_INTEREST_RATES_BASED_ON_PRINCIPAL_MIN_THRESHOLD_BGN.items():
        if principal <= threshold:
            interest_rate = LOAN_INTEREST_RATES_BASED_ON_PRINCIPAL_MIN_THRESHOLD_BGN[threshold]
    # Further deductions based on duration of the loan
    for threshold, i_rate in LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION.items():
        if principal <= threshold:
            interest_rate -= LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION[threshold]

    return interest_rate


def loan_approve(anual_income, principal, period):
    interest_rate = calc_loan_interest_rate(principal, period)

