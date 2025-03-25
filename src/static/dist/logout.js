"use strict";
function handleLogout() {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then((response) => {
        if (response.ok) {
            window.location.href = '/';
        }
    })
        .catch((error) => console.error('Error:', error));
}
