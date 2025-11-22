// Login Logic
async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('api_token', data.token);
            window.location.href = '/dashboard.html';
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Dashboard Logic
async function loadDashboard() {
    const token = localStorage.getItem('api_token');
    if (!token) {
        window.location.href = '/';
        return;
    }

    try {
        const response = await fetch('/api/dashboard-data', {
            headers: { 'Authorization': token }
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('user-name').textContent = data.username;
            document.getElementById('user-role').textContent = data.role;
            document.getElementById('user-email').value = data.email;
            document.getElementById('dashboard-image').src = data.dashboard_image;
        } else {
            localStorage.removeItem('api_token');
            window.location.href = '/';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function updateProfile(event) {
    event.preventDefault();
    const token = localStorage.getItem('api_token');
    const email = document.getElementById('user-email').value;

    try {
        const response = await fetch('/api/profile/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token
            },
            body: JSON.stringify({ email })
        });

        const data = await response.json();
        alert(data.message);
        if (response.ok) {
            location.reload();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
