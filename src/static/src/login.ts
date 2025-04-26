document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm') as HTMLFormElement;
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e: Event) {
            e.preventDefault();
            
            const usernameInput = document.getElementById('username') as HTMLInputElement;
            const passwordInput = document.getElementById('password') as HTMLInputElement;
            
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
            .then((data: { success: boolean; message?: string }) => {
                if (data.success) {
                    window.location.href = '/';
                } else {
                    alert(data.message || 'Login failed. Please try again.');
                }
            })
            .catch((error: Error) => {
                console.error('Error:', error);
            });
        });
    }
});