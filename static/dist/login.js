"use strict";
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const usernameInput = document.getElementById('username');
            const passwordInput = document.getElementById('password');
            const data = {
                username: usernameInput.value,
                password: passwordInput.value
            };
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then((data) => {
                if (data.success) {
                    window.location.href = '/';
                }
                else {
                    alert(data.message || 'Login failed. Please try again.');
                }
            })
                .catch((error) => {
                console.error('Error:', error);
            });
        });
    }
});
