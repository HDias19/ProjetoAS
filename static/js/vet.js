const searchInput = document.querySelector('input[name="email_cliente"]');
const searchResults = document.getElementById('search-results');

searchResults.style.display = 'none';

searchInput.addEventListener('focus', () => {
    if (searchInput.value.trim().length != 0) {
        searchResults.style.display = 'block';
    }
});

searchInput.addEventListener('blur', () => {
    if (searchInput.value.trim().length === 0) {
        searchResults.style.display = 'none';
    }
});

searchInput.addEventListener('input', () => {
    if (searchInput.value.trim().length >= 0) {
        searchResults.style.display = 'block';
    } else {
        searchResults.style.display = 'none';
    }
});

const resultItems = searchResults.querySelectorAll('li');
resultItems.forEach((item) => {
    item.addEventListener('click', () => {
        const selectedEmail = item.getAttribute('data-email');
        searchInput.value = selectedEmail.trim();
        searchResults.style.display = 'none';
    });
});

function selectEmail(email) {
    const emailInput = document.getElementById('email_cliente');
    emailInput.value = email;
    searchResults.style.display = 'none';
}
