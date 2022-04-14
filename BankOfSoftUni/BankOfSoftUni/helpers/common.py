import datetime
from dateutil.relativedelta import relativedelta

from BankOfSoftUni.helpers.parametrizations import ALLOWED_CURRENCIES, \
    LOAN_INTEREST_RATES_BASED_ON_PRINCIPAL_MIN_THRESHOLD_BGN, LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION_YEARS, \
    MAX_INCOME_SHARE_AS_MONTHLY_LOAN_PAYMENT

import numpy_financial as npf


def get_next_month_date():
    date_today = datetime.date.today()
    next_month_date = date_today + relativedelta(months=1)
    return next_month_date


def calc_foreign_currency_to_BGN(value, currency):
    return value * ALLOWED_CURRENCIES[currency]


def calc_loan_interest_rate(principal, period):
    interest_rate = 0
    # Calculate interest based on principal
    for threshold, i_rate in LOAN_INTEREST_RATES_BASED_ON_PRINCIPAL_MIN_THRESHOLD_BGN.items():
        if principal <= threshold and interest_rate < i_rate:
            interest_rate = i_rate
    # Further deductions based on duration of the loan
    for threshold, i_rate in LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION_YEARS.items():
        if period <= threshold:
            interest_rate -= LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION_YEARS[threshold]

    return interest_rate


def loan_approve(annual_income, principal, period):
    interest_rate_percentage = calc_loan_interest_rate(principal, period) / 100
    monthly_payment = npf.pmt(interest_rate_percentage / 12, period * 12, principal) * -1
    loan_approval = annual_income / 12 * MAX_INCOME_SHARE_AS_MONTHLY_LOAN_PAYMENT >= monthly_payment
    total_loan_costs = monthly_payment * period * 12
    total_interest_costs = total_loan_costs - principal
    loan_first_payment = get_next_month_date()

    return {
        'monthly_payment': f"{monthly_payment:.2f}",
        'interest_rate': f'{interest_rate_percentage * 100:.2f}',
        'loan_approval': loan_approval,
        'total_loan_cost': f"{total_loan_costs:.2f}",
        'total_interest_costs': f'{total_interest_costs:.2f}',
        'loan_first_payment': loan_first_payment,
    }
