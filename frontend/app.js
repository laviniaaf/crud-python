const API_BASE = '/api';  
let editingUserId = null;

const userForm = document.getElementById('userForm');
const usersList = document.getElementById('usersList');
const formTitle = document.getElementById('form-title');
const submitBtn = document.getElementById('submitBtn');
const cancelBtn = document.getElementById('cancelBtn');
const refreshBtn = document.getElementById('refreshBtn');
const loading = document.getElementById('loading');
const message = document.getElementById('message');

document.addEventListener('DOMContentLoaded', loadUsers);

userForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(userForm);
    const userData = {
        name: formData.get('name'),
        email: formData.get('email'),
        age: parseInt(formData.get('age'))
    };

    if (editingUserId) {
        await updateUser(editingUserId, userData);
    } else {
        await createUser(userData);
    }
});

cancelBtn.addEventListener('click', resetForm);
refreshBtn.addEventListener('click', loadUsers);

// API Functions
async function loadUsers() {
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE}/users`);
        const users = await response.json();
        displayUsers(users);
        hideMessage();
    } catch (error) {
        showMessage('Error loading users', 'error');
        console.error('Load users error:', error);
    } finally {
        showLoading(false);
    }
}

async function createUser(userData) {
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            showMessage('User created successfully!', 'success');
            userForm.reset();
            await loadUsers();
        } else {
            const error = await response.json();
            showMessage(error.error || 'Error creating user', 'error');
        }
    } catch (error) {
        showMessage('Error creating user', 'error');
        console.error('Create user error:', error);
    } finally {
        showLoading(false);
    }
}

async function updateUser(id, userData) {
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE}/users/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            showMessage('User updated successfully!', 'success');
            resetForm();
            await loadUsers();
        } else {
            const error = await response.json();
            showMessage(error.error || 'Error updating user', 'error');
        }
    } catch (error) {
        showMessage('Error updating user', 'error');
        console.error('Update user error:', error);
    } finally {
        showLoading(false);
    }
}

async function deleteUser(id) {
    if (!confirm('Are you sure you want to delete this user?')) return;
    
    showLoading(true);
    try {
        const response = await fetch(`${API_BASE}/users/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showMessage('User deleted successfully!', 'success');
            await loadUsers();
        } else {
            const error = await response.json();
            showMessage(error.error || 'Error deleting user', 'error');
        }
    } catch (error) {
        showMessage('Error deleting user', 'error');
        console.error('Delete user error:', error);
    } finally {
        showLoading(false);
    }
}

// UI Functions
function displayUsers(users) {
    if (users.length === 0) {
        usersList.innerHTML = '<div class="no-users">No users found. Create your first user!</div>';
        return;
    }

    usersList.innerHTML = users.map(user => `
        <div class="user-card">
            <div class="user-info">
                <h3><i class="fas fa-user"></i> ${user.name}</h3>
                <p><i class="fas fa-envelope"></i> ${user.email}</p>
                <p><i class="fas fa-birthday-cake"></i> ${user.age} years old</p>
            </div>
            <div class="user-actions">
                <button class="btn btn-edit" onclick="editUser(${user.id}, '${user.name}', '${user.email}', ${user.age})">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button class="btn btn-delete" onclick="deleteUser(${user.id})">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </div>
        </div>
    `).join('');
}

function editUser(id, name, email, age) {
    editingUserId = id;
    document.getElementById('name').value = name;
    document.getElementById('email').value = email;
    document.getElementById('age').value = age;
    
    formTitle.innerHTML = '<i class="fas fa-user-edit"></i> Edit User';
    submitBtn.innerHTML = '<i class="fas fa-save"></i> Update User';
    cancelBtn.style.display = 'inline-block';
    
    document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth' });
}

function resetForm() {
    editingUserId = null;
    userForm.reset();
    formTitle.innerHTML = '<i class="fas fa-user-plus"></i> Add New User';
    submitBtn.innerHTML = '<i class="fas fa-save"></i> Save User';
    cancelBtn.style.display = 'none';
}

function showLoading(show) {
    loading.style.display = show ? 'flex' : 'none';
}

function showMessage(text, type) {
    message.textContent = text;
    message.className = `message ${type} show`;
    setTimeout(() => {
        message.classList.remove('show');
    }, 3000);
}

function hideMessage() {
    message.classList.remove('show');
}