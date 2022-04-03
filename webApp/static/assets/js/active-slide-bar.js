const id_home_page                  = document.getElementById("id_home_page")
const id_contact_us_page            = document.getElementById("id_contact_us_page")
const id_notification_page          = document.getElementById("id_notification_page")
const id_equipment_list_page        = document.getElementById("id_equipment_list_page")
const id_borrowing_history_page     = document.getElementById("id_borrowing_history_page")
const id_borrowing_information_page = document.getElementById("id_borrowing_information_page")

window.onload = (event) => {
    switch(String(name_page)) {
        case id_home_page.name:
            id_home_page.className = "nav-link text-white active bg-gradient-primary"
            break;
        case id_contact_us_page.name:
            id_contact_us_page.className = "nav-link text-white active bg-gradient-primary"
            break;
        case id_notification_page.name:
            id_notification_page.className = "nav-link text-white active bg-gradient-primary"
            break;
        case id_equipment_list_page.name:
            id_equipment_list_page.className = "nav-link text-white active bg-gradient-primary"
            break;
        case id_borrowing_history_page.name:
            id_borrowing_history_page.className = "nav-link text-white active bg-gradient-primary"
            break;
        case id_borrowing_information_page.name:
            id_borrowing_information_page.className = "nav-link text-white active bg-gradient-primary"
            break;
        default:
            break;
        }
}