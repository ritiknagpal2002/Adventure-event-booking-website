function showPopup(ev) {
    // Get the popup element by its ID
    var event = ev
    const popup = document.getElementById("popup");
    // const event_id = document.getElementById("event_id")
    const event_name = document.getElementById("event_name")
    const event_desc = document.getElementById("event_name")
    const event_img = document.getElementById("event_img")
    const book_form = document.getElementById("book_form")

    book_form.action = `http://127.0.0.1:8000/myapp/bookingevent/${event.eventID}/`

    event_name.textContent = event.name
    event_desc.textContent = event.desc

    console.log("Event is: ", event)

    // Display the popup
    popup.style.display = "block";
}

function hidePaymentPopup() {
    history.go(-1)
}
function searchButtonClick() {
    const search_button = document.getElementById("search-button");

    // create a new input element
    search_button.classList.remove('search-btn-expanded');
    void search_button.offsetWidth;
    search_button.classList.add('search-btn-expanded');
    search_button.style.transform = "-30em";

}



window.onload = () => {
    document.getElementById("search_results").scrollIntoView({behavior:"smooth"})
}