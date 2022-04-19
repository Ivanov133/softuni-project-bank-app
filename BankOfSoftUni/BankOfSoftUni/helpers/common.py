import datetime
from dateutil.relativedelta import relativedelta

from BankOfSoftUni.helpers.parametrizations import ALLOWED_CURRENCIES, \
    LOAN_INTEREST_RATES_BASED_ON_PRINCIPAL_MIN_THRESHOLD_BGN, LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION_MONTHS, \
    MAX_INCOME_SHARE_AS_MONTHLY_LOAN_PAYMENT

import numpy_financial as npf

from BankOfSoftUni.tasks_app.models import UserAnnualTargets


# Functions cover:
#   Loan model data - needed for creation/update and model property
#   Session storage data
#   TargetList model update


# Loan data based functions
def get_next_month_date():
    date_today = datetime.date.today()
    next_month_date = date_today + relativedelta(months=1)
    return next_month_date


def get_loan_end_date(start_date, months):
    end_date = start_date + relativedelta(months=months)
    return end_date


def calc_local_currency_to_foreign(bgn_value, currency):
    return bgn_value / ALLOWED_CURRENCIES[currency]


def calc_foreign_currency_to_BGN(value, currency):
    return value * ALLOWED_CURRENCIES[currency]


# Based on parametrization
def calc_loan_interest_rate(principal, period):
    interest_rate = 0
    # Calculate interest based on principal
    for threshold, i_rate in LOAN_INTEREST_RATES_BASED_ON_PRINCIPAL_MIN_THRESHOLD_BGN.items():
        if principal <= threshold and interest_rate < i_rate:
            interest_rate = i_rate
    # Further deductions based on duration of the loan
    for threshold, i_rate in LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION_MONTHS.items():
        if period <= threshold:
            interest_rate -= LOAN_INTEREST_RATES_DEDUCTIONS_BASED_ON_DURATION_MONTHS[threshold]

    return interest_rate


# Get all loan fields
def loan_approve(annual_income, principal, period):
    interest_rate_percentage = calc_loan_interest_rate(principal, period) / 100
    monthly_payment = npf.pmt(interest_rate_percentage / 12, period, principal) * -1
    loan_approval = annual_income / 12 * MAX_INCOME_SHARE_AS_MONTHLY_LOAN_PAYMENT >= monthly_payment
    total_loan_costs = monthly_payment * period
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


def get_loan_monthly_payment_interest_and_principal(i_rate, period_months, principal):
    interest_payment = npf.ipmt(i_rate / 12, 1, period_months, -principal)
    principal_payment = npf.ppmt(i_rate / 12, 1, period_months, -principal)

    return {
        'interest_payment': interest_payment,
        'principal_payment': principal_payment,
    }


def get_loan_table_of_payments():
    pass


# Target list model update related functions
def update_target_list_customer(user_id):
    target_list = UserAnnualTargets.objects.get(pk=user_id)
    target_list.registered_clients_actual += 1
    target_list.save()


def update_target_list_accounts(user_id):
    target_list = UserAnnualTargets.objects.get(pk=user_id)
    target_list.opened_accounts_actual += 1
    target_list.save()


def update_target_list_loans(user_id, principal):
    target_list = UserAnnualTargets.objects.get(pk=user_id)
    target_list.opened_loans_actual += 1
    target_list.total_loans_size_actual += float(principal)
    target_list.save()


# Session related functions
def set_request_session_loan_params(request, loan_data, principal, period, customer_id):
    request.session['monthly_payment'] = loan_data['monthly_payment']
    request.session['interest_rate'] = loan_data['interest_rate']
    request.session['total_loan_cost'] = loan_data['total_loan_cost']
    request.session['total_interest_costs'] = loan_data['total_interest_costs']
    request.session['principal'] = principal
    request.session['period'] = period
    request.session['customer_id'] = customer_id
    request.session.modified = True


def clear_request_session_loan_params(request):
    if "monthly_payment" in request.session.keys():
        del request.session["monthly_payment"]
    if "interest_rate" in request.session.keys():
        del request.session["interest_rate"]
    if "total_loan_cost" in request.session.keys():
        del request.session["total_loan_cost"]
    if "total_interest_costs" in request.session.keys():
        del request.session["total_interest_costs"]
    if "principal" in request.session.keys():
        del request.session["principal"]
    if "period" in request.session.keys():
        del request.session["period"]
    if "customer_id" in request.session.keys():
        del request.session["customer_id"]


def clear_session_error(request):
    if request.session.get('error', None):
        del request.session['error']


def set_session_error(request, message):
    request.session['error'] = message