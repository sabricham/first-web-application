//home-album photo filter by name using a searchbar input
const home_search_input = document.getElementById("home-search-photo");
const home_album_elements = document.querySelectorAll(".home-photo-view");

//event to read any input changes in the input research section
home_search_input.addEventListener("keyup", function(event) {

    //input event transformed to a lower case and also the text content to avoid any error in case sensitivity
    const input = event.target.value.toLowerCase();

    home_album_elements.forEach((photo) => {
        photo.querySelector(".photo-view-title").textContent.toLowerCase().startsWith(input) 
        ? (photo.style.display = '') //visibile
        : (photo.style.display = 'none');
    });
});

//personal-album photo filter by name using a searchbar input
const personal_search_input = document.getElementById("personal-search-photo");
const personal_album_photos = document.querySelectorAll(".personal-photo-view");

//event to read any input changes in the input research section
personal_search_input.addEventListener("keyup", function(event) {

    //input event transformed to a lower case and also the text content to avoid any error in case sensitivity
    const input = event.target.value.toLowerCase();

    personal_album_photos.forEach((photo) => {
        photo.querySelector(".photo-view-title").textContent.toLowerCase().startsWith(input) 
            ? (photo.style.display = '') //visibile
            : (photo.style.display = 'none');
    });
});