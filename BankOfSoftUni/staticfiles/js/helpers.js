//Customer details page ev listeners
document.getElementById('open-account-btn').addEventListener('click', display_form_account)
document.getElementById('show-accounts-btn').addEventListener('click', display_accounts_list)
document.getElementById('show-loans-btn').addEventListener('click', display_loans_list)
document.getElementById('show-customer-details').addEventListener('click', display_customer_details)

function display_form_account(ev) {
    let form_style = document.getElementById('account-open').style.display
    if (form_style == 'none') {
        document.getElementById('account-open').style.display = 'block'
        ev.target.textContent = 'Cancel'
    } else {
        document.getElementById('account-open').style.display = 'none'
        ev.target.textContent = 'Open account'
    }
}


function display_accounts_list(ev) {
    let form_style = document.getElementById('accounts-list-table').style.display
    if (form_style == 'none') {
        document.getElementById('accounts-list-table').style.display = 'block'
        ev.target.textContent = 'Hide account list'
        ev.target.style["background-color"] = 'red'

    } else {
        document.getElementById('accounts-list-table').style.display = 'none'
        ev.target.textContent = 'Show customer accounts'
        ev.target.style["background-color"] = 'darkorange'

    }
}

function display_loans_list(ev) {
    let form_style = document.getElementById('loan-list-table').style.display
    if (form_style == 'none') {
        document.getElementById('loan-list-table').style.display = 'block'
        ev.target.textContent = 'Hide loan list'
        ev.target.style["background-color"] = 'red'

    } else {
        document.getElementById('loan-list-table').style.display = 'none'
        ev.target.textContent = 'Show loans'
        ev.target.style["background-color"] = 'darkorange'

    }
}

function display_customer_details(ev) {
    let form_style = document.getElementById('customer-details').style.display
    if (form_style == 'none') {
        document.getElementById('customer-details').style.display = 'block'
        ev.target.textContent = 'Hide details'
    } else {
        document.getElementById('customer-details').style.display = 'none'
        ev.target.textContent = 'Show customer details'
    }
}
