document.addEventListener('DOMContentLoaded', () => {
    const guestForm = document.getElementById('guest-form');
    
    fetchGuestTodos();

    if (guestForm) {
        guestForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            clearGuestAlerts();

            const title = document.getElementById('guest-title').value.trim();
            const body = document.getElementById('guest-body').value.trim();

            if (!title) {
                showGuestError('Title is required.');
                return;
            }

            try {
                const response = await apiFetch('/guest/todos', {
                    method: 'POST',
                    body: JSON.stringify({
                        title: title,
                        body: body || null
                    })
                });

                if (response.status === 201) {
                    guestForm.reset();
                    showGuestSuccess('Guest Todo created successfully!');
                    fetchGuestTodos();
                } else {
                    const data = await response.json();
                    showGuestError(data.detail || 'Failed to create guest todo.');
                }
            } catch (err) {
                showGuestError('Network error. Please try again.');
            }
        });
    }
});

async function fetchGuestTodos() {
    const listContainer = document.getElementById('guest-todo-list');
    if (!listContainer) return;

    try {
        const response = await apiFetch('/guest/todos');
        if (response.status === 200) {
            const todos = await response.json();
            renderGuestTodos(todos);
        } else {
            listContainer.innerHTML = `<p class="text-red-500 text-sm">Failed to retrieve guest todos.</p>`;
        }
    } catch (err) {
        listContainer.innerHTML = `<p class="text-red-500 text-sm">Error connecting to server.</p>`;
    }
}

function renderGuestTodos(todos) {
    const listContainer = document.getElementById('guest-todo-list');
    if (!listContainer) return;

    if (todos.length === 0) {
        listContainer.innerHTML = `
            <div class="text-center py-8 text-gray-500 bg-gray-50 rounded-xl border border-dashed border-gray-200">
                No guest/public todos yet. Be the first to create one!
            </div>
        `;
        return;
    }

    listContainer.innerHTML = todos.map(todo => {
        const date = new Date(todo.created_at).toLocaleString();
        return `
            <div class="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition duration-200 flex flex-col justify-between">
                <div>
                    <h3 class="font-semibold text-gray-800 text-lg mb-1 break-words">${escapeHtml(todo.title)}</h3>
                    <p class="text-gray-600 text-sm mb-4 whitespace-pre-wrap break-words">${todo.body ? escapeHtml(todo.body) : '<span class="text-gray-400 italic">No description</span>'}</p>
                </div>
                <div class="text-xs text-gray-400 pt-3 border-t border-gray-50 flex justify-between items-center">
                    <span>Public Guest Todo</span>
                    <span>${date}</span>
                </div>
            </div>
        `;
    }).join('');
}

function showGuestError(message) {
    const alert = document.getElementById('guest-alert-error');
    if (alert) {
        alert.textContent = message;
        alert.classList.remove('hidden');
    }
}

function showGuestSuccess(message) {
    const alert = document.getElementById('guest-alert-success');
    if (alert) {
        alert.textContent = message;
        alert.classList.remove('hidden');
        setTimeout(() => alert.classList.add('hidden'), 4000);
    }
}

function clearGuestAlerts() {
    const errorAlert = document.getElementById('guest-alert-error');
    const successAlert = document.getElementById('guest-alert-success');
    if (errorAlert) errorAlert.classList.add('hidden');
    if (successAlert) successAlert.classList.add('hidden');
}

function escapeHtml(str) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
