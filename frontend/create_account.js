const form = document.getElementById('loginForm');
const footerText = document.getElementById('footerText');

form.addEventListener('submit', async (e) => {
    e.preventDefault(); // prevent page reload

    const username = form.username.value;
    const password = form.password.value;
    const confirmPassword = form.confirmPassword.value;

    if (password !== confirmPassword) {
    footerText.textContent = "Passwords do not match.";
    footerText.style.color = "#ff4d4d"; // red for error
    return;
    }

    try {
    const response = await fetch('http://127.0.0.1:5000//register', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
        footerText.textContent = data.message;
        footerText.style.color = "#00ff99"; // green for success
    } else {
        footerText.textContent = data.message;
        footerText.style.color = "#ff4d4d"; // red for error
    }
    } catch (error) {
    console.error('Error:', error);
    footerText.textContent = "Network error. Try again later.";
    footerText.style.color = "#ff4d4d"; // red for network error
    }
});