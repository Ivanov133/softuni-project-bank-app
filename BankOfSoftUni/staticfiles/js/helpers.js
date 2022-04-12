document.getElementById('open-account-btn').addEventListener('click', display_form)

function display_form(ev) {
    let form_style = document.getElementById('account-open').style.display
    console.log(typeof (form_style))
    if (form_style == 'none') {
        document.getElementById('account-open').style.display = 'block'
        ev.target.textContent = 'Cancel'
    } else {
        document.getElementById('account-open').style.display = 'none'
        ev.target.textContent = 'Open account'

    }
}
