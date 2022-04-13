//Customer details page ev listeners
document.getElementById('open-account-btn').addEventListener('click', display_form_account)
document.getElementById('show-accounts-btn').addEventListener('click', display_accounts_list)
document.getElementById('open-account-btn').addEventListener('click', display_form_account)
document.getElementById('open-account-btn').addEventListener('click', display_form_account)

$('label[for="id_id_card"]').hide()

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
        ev.target.textContent = 'Hide list'
        ev.target.style["background-color"] = 'red'

    } else {
        document.getElementById('accounts-list-table').style.display = 'none'
        ev.target.textContent = 'Show customer accounts'
        ev.target.style["background-color"] = 'darkorange'

    }
}
