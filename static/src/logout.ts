function handleLogout(): void {
    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then((response: Response) => {
        if (response.ok) {
            window.location.href = '/';
        }
    })
    .catch((error: Error) => console.error('Error:', error));
}
