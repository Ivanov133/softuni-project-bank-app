document.getElementById('show_target_list').addEventListener('click', display_target_list)

function display_target_list(ev) {
    let form_style = document.getElementById('target_list').style.display
    if (form_style == 'none') {
        document.getElementById('target_list').style.display = 'block'
        ev.target.textContent = 'Hide'
    } else {
        document.getElementById('target_list').style.display = 'none'
        ev.target.textContent = 'Show target completion'
    }
}
