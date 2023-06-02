window.onload = function () {
    var popup = document.querySelector('.popup');
    var closeButton = document.querySelector('.popup-button');

    // Calculate the center position
    var centerX = window.innerWidth / 2;
    var centerY = window.innerHeight / 2;

    // Calculate the left and top positions for centering the popup
    var popupWidth = popup.offsetWidth;
    var popupHeight = popup.offsetHeight;
    var leftPosition = centerX - popupWidth / 2;
    var topPosition = centerY - popupHeight / 2;

    // Set the popup position
    popup.style.left = leftPosition + 'px';
    popup.style.top = topPosition + 'px';

    // Show the popup
    popup.style.display = 'block';

    // Close the popup when the "OK" button is clicked
    closeButton.addEventListener('click', function () {
        popup.style.display = 'none';
    });
};