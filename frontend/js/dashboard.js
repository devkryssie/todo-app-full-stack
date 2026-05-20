document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = '/index.html';
        return;
    }

    fetchUserTodos();

    const createForm = document.getElementById('todo-form');
    if (createForm) {
        createForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            clearDashboardAlerts();

            const title = document.getElementById('todo-title').value.trim();
            const body = document.getElementById('todo-body').value.trim();

            if (!title) {
                showDashboardError('Title is required.');
                return;
            }

            try {
                const response = await apiFetch('/todos', {
                    method: 'POST',
                    body: JSON.stringify({
                        title: title,
                        body: body || null
                    })
                });

                if (response.status === 201) {
                    createForm.reset();
                    showDashboardSuccess('Todo created successfully!');
                    fetchUserTodos();
                } else {
                    const data = await response.json();
                    showDashboardError(data.detail || 'Failed to create todo.');
                }
            } catch (err) {
                showDashboardError('Network error. Please try again.');
            }
        });
    }
});

async function fetchUserTodos() {
    const listContainer = document.getElementById('todo-list');
    if (!listContainer) return;

    try {
        const response = await apiFetch('/todos');
        if (response.status === 200) {
            const todos = await response.json();
            renderUserTodos(todos);
        } else {
            listContainer.innerHTML = `<p class="text-red-500 text-sm">Failed to retrieve your todos.</p>`;
        }
    } catch (err) {
        listContainer.innerHTML = `<p class="text-red-500 text-sm">Error connecting to server.</p>`;
    }
}

function renderUserTodos(todos) {
    const listContainer = document.getElementById('todo-list');
    if (!listContainer) return;

    if (todos.length === 0) {
        listContainer.innerHTML = `
            <div class="text-center py-10 text-gray-500 bg-gray-50 rounded-xl border border-dashed border-gray-200">
                You have no private todos yet. Add a new task above!
            </div>
        `;
        return;
    }

    listContainer.innerHTML = todos.map(todo => {
        const statusBadgeColor = todo.status === 'COMPLETED' 
            ? 'bg-green-50 text-green-700 border-green-200' 
            : 'bg-yellow-50 text-yellow-700 border-yellow-200';
            
        return `
            <div id="todo-card-${todo.id}" class="bg-white p-5 rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition duration-200">
                <!-- Static View -->
                <div id="todo-view-${todo.id}" class="flex flex-col justify-between h-full space-y-4">
                    <div>
                        <div class="flex items-start justify-between space-x-2">
                            <h3 class="font-semibold text-gray-800 text-lg break-words">${escapeHtml(todo.title)}</h3>
                            <span class="px-2.5 py-0.5 rounded-full text-xs font-medium border ${statusBadgeColor}">
                                ${todo.status}
                            </span>
                        </div>
                        <p class="text-gray-600 text-sm mt-2 whitespace-pre-wrap break-words">${todo.body ? escapeHtml(todo.body) : '<span class="text-gray-400 italic">No description</span>'}</p>
                    </div>
                    <div class="pt-3 border-t border-gray-50 flex items-center justify-between text-xs text-gray-400">
                        <span>Updated: ${new Date(todo.updated_at).toLocaleString()}</span>
                        <div class="flex items-center space-x-3">
                            <button onclick="startEditTodo(${todo.id}, '${escapeJsString(todo.title)}', '${escapeJsString(todo.body || "")}', '${todo.status}')" class="text-indigo-600 hover:text-indigo-800 font-medium transition">Edit</button>
                            <button onclick="deleteTodo(${todo.id})" class="text-red-600 hover:text-red-800 font-medium transition">Delete</button>
                        </div>
                    </div>
                </div>

                <!-- Inline Edit View (Hidden by default) -->
                <div id="todo-edit-${todo.id}" class="hidden space-y-3">
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Title</label>
                        <input type="text" id="edit-title-${todo.id}" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Body</label>
                        <textarea id="edit-body-${todo.id}" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"></textarea>
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Status</label>
                        <select id="edit-status-${todo.id}" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white">
                            <option value="PENDING">PENDING</option>
                            <option value="COMPLETED">COMPLETED</option>
                        </select>
                    </div>
                    <div class="flex items-center justify-end space-x-3 pt-2">
                        <button onclick="cancelEditTodo(${todo.id})" class="px-3 py-1.5 text-xs font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition">Cancel</button>
                        <button onclick="saveEditTodo(${todo.id})" class="px-3 py-1.5 text-xs font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition">Save Changes</button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

// Inline editing functions
function startEditTodo(id, title, body, status) {
    document.getElementById(`todo-view-${id}`).classList.add('hidden');
    
    const editContainer = document.getElementById(`todo-edit-${id}`);
    editContainer.classList.remove('hidden');

    document.getElementById(`edit-title-${id}`).value = title;
    document.getElementById(`edit-body-${id}`).value = body;
    document.getElementById(`edit-status-${id}`).value = status;
}

function cancelEditTodo(id) {
    document.getElementById(`todo-edit-${id}`).classList.add('hidden');
    document.getElementById(`todo-view-${id}`).classList.remove('hidden');
}

async function saveEditTodo(id) {
    const title = document.getElementById(`edit-title-${id}`).value.trim();
    const body = document.getElementById(`edit-body-${id}`).value.trim();
    const status = document.getElementById(`edit-status-${id}`).value;

    if (!title) {
        showDashboardError('Todo title cannot be empty.');
        return;
    }

    try {
        const response = await apiFetch(`/todos/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                title: title,
                body: body || null,
                status: status
            })
        });

        if (response.status === 200) {
            showDashboardSuccess('Todo updated successfully!');
            fetchUserTodos();
        } else {
            const data = await response.json();
            showDashboardError(data.detail || 'Failed to update todo.');
        }
    } catch (err) {
        showDashboardError('Network error. Failed to save changes.');
    }
}

async function deleteTodo(id) {
    if (!confirm('Are you sure you want to delete this todo?')) return;

    try {
        const response = await apiFetch(`/todos/${id}`, {
            method: 'DELETE'
        });

        if (response.status === 200) {
            showDashboardSuccess('Todo deleted successfully.');
            fetchUserTodos();
        } else {
            const data = await response.json();
            showDashboardError(data.detail || 'Failed to delete todo.');
        }
    } catch (err) {
        showDashboardError('Network error. Failed to delete todo.');
    }
}

// Helpers for Alerts
function showDashboardError(message) {
    const alert = document.getElementById('dashboard-alert-error');
    if (alert) {
        alert.textContent = message;
        alert.classList.remove('hidden');
    }
}

function showDashboardSuccess(message) {
    const alert = document.getElementById('dashboard-alert-success');
    if (alert) {
        alert.textContent = message;
        alert.classList.remove('hidden');
        setTimeout(() => alert.classList.add('hidden'), 4000);
    }
}

function clearDashboardAlerts() {
    const errorAlert = document.getElementById('dashboard-alert-error');
    const successAlert = document.getElementById('dashboard-alert-success');
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

function escapeJsString(str) {
    return str
        .replace(/\\/g, '\\\\')
        .replace(/'/g, "\\'")
        .replace(/"/g, '\\"')
        .replace(/\n/g, '\\n')
        .replace(/\r/g, '\\r');
}
