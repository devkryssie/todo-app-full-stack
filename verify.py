import time
import requests

BASE_URL = "http://localhost:8081"
API_VERSION_URL = f"{BASE_URL}/api/v1"

def print_header(title):
    print(f"\n{'='*50}\n{title}\n{'='*50}")

def print_result(success, message):
    mark = "🟢 PASS" if success else "🔴 FAIL"
    print(f"{mark} - {message}")

def wait_for_backend():
    print("Waiting for backend to start up...")
    max_retries = 30
    for i in range(max_retries):
        try:
            r = requests.get(f"{BASE_URL}/")
            if r.status_code == 200:
                print("Backend is up and running!")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(2)
    print("Backend failed to start.")
    return False

def test_health():
    print_header("Testing Healthcheck & V1 docs existence")
    r = requests.get(f"{BASE_URL}/")
    print_result(r.status_code == 200, f"Root healthcheck: {r.status_code}")
    
    r = requests.get(f"{API_VERSION_URL}/openapi.json")
    print_result(r.status_code == 200, f"OpenAPI JSON schema existence: {r.status_code}")

def test_auth():
    print_header("Testing User Registration & Authentication")
    email_u1 = "user1@example.com"
    email_u2 = "user2@example.com"
    password = "password123"

    # 1. Clean up or register new users
    # User 1 Register
    register_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": email_u1,
        "password": password
    }
    r = requests.post(f"{API_VERSION_URL}/auth/register", json=register_data)
    if r.status_code == 409:
        print_result(True, "User 1 already registered (conflict handling works)")
    else:
        print_result(r.status_code == 201, f"User 1 Register: {r.status_code}")
        if r.status_code == 201:
            data = r.json()
            print_result("password" not in data, "User registration did NOT leak password field")

    # Double register User 1 (should fail)
    r = requests.post(f"{API_VERSION_URL}/auth/register", json=register_data)
    print_result(r.status_code == 409, f"Registering duplicate email returns 409 Conflict: {r.status_code}")

    # Register User 2
    register_data_2 = {
        "first_name": "Bob",
        "last_name": "Jones",
        "email": email_u2,
        "password": password
    }
    r = requests.post(f"{API_VERSION_URL}/auth/register", json=register_data_2)
    if r.status_code == 409:
        print_result(True, "User 2 already registered")
    else:
        print_result(r.status_code == 201, f"User 2 Register: {r.status_code}")

    # 2. Login User 1
    login_data = {
        "email": email_u1,
        "password": password
    }
    r = requests.post(f"{API_VERSION_URL}/auth/login", json=login_data)
    print_result(r.status_code == 200, f"User 1 Login: {r.status_code}")
    token_1 = None
    if r.status_code == 200:
        token_1 = r.json().get("access_token")
        print_result(token_1 is not None, "Login returns access token")

    # Login User 2
    login_data_2 = {
        "email": email_u2,
        "password": password
    }
    r = requests.post(f"{API_VERSION_URL}/auth/login", json=login_data_2)
    token_2 = None
    if r.status_code == 200:
        token_2 = r.json().get("access_token")

    # Login with invalid password
    bad_login = {
        "email": email_u1,
        "password": "wrongpassword"
    }
    r = requests.post(f"{API_VERSION_URL}/auth/login", json=bad_login)
    print_result(r.status_code == 401, f"Login with wrong password returns 401: {r.status_code}")

    return token_1, token_2

def test_todos(token_1, token_2):
    print_header("Testing Protected Private Todos")
    headers_1 = {"Authorization": f"Bearer {token_1}"}
    headers_2 = {"Authorization": f"Bearer {token_2}"}

    # 1. Create a todo for User 1
    todo_data = {
        "title": "Buy groceries",
        "body": "Milk, eggs, and bread"
    }
    r = requests.post(f"{API_VERSION_URL}/todos", json=todo_data, headers=headers_1)
    print_result(r.status_code == 201, f"User 1 create todo: {r.status_code}")
    todo_id = None
    if r.status_code == 201:
        res_data = r.json()
        todo_id = res_data.get("id")
        print_result(res_data.get("status") == "PENDING", "Todo default status is PENDING")
        print_result(res_data.get("title") == "Buy groceries", "Todo title is correct")

    # 2. Get User 1's todos
    r = requests.get(f"{API_VERSION_URL}/todos", headers=headers_1)
    print_result(r.status_code == 200, f"User 1 get todos: {r.status_code}")
    if r.status_code == 200:
        todos = r.json()
        print_result(len(todos) > 0, f"User 1 received {len(todos)} todos")
        print_result(all(t.get("user_id") is not None for t in todos), "Todos have valid user_id associated")

    # 3. Security Boundary: User 2 tries to GET User 1's todo by updating or modifying
    # User 2 tries to update User 1's todo (should return 403 Forbidden)
    update_data = {
        "title": "Hack todo",
        "status": "COMPLETED"
    }
    r = requests.put(f"{API_VERSION_URL}/todos/{todo_id}", json=update_data, headers=headers_2)
    print_result(r.status_code == 403, f"User 2 trying to update User 1's todo returns 403: {r.status_code}")

    # User 2 tries to delete User 1's todo (should return 403 Forbidden)
    r = requests.delete(f"{API_VERSION_URL}/todos/{todo_id}", headers=headers_2)
    print_result(r.status_code == 403, f"User 2 trying to delete User 1's todo returns 403: {r.status_code}")

    # User 2 gets their own todos (should be empty, and never show User 1's todo)
    r = requests.get(f"{API_VERSION_URL}/todos", headers=headers_2)
    if r.status_code == 200:
        todos_2 = r.json()
        contains_u1_todo = any(t.get("id") == todo_id for t in todos_2)
        print_result(not contains_u1_todo, "User 2 cannot see User 1's private todo in GET list")

    # 4. Update todo for User 1
    update_data = {
        "status": "COMPLETED"
    }
    r = requests.put(f"{API_VERSION_URL}/todos/{todo_id}", json=update_data, headers=headers_1)
    print_result(r.status_code == 200, f"User 1 updates own todo to COMPLETED: {r.status_code}")
    if r.status_code == 200:
        updated = r.json()
        print_result(updated.get("status") == "COMPLETED", "Todo status is successfully updated")
        print_result(updated.get("updated_at") is not None, "updated_at timestamp is populated")

    # 5. Delete todo for User 1
    r = requests.delete(f"{API_VERSION_URL}/todos/{todo_id}", headers=headers_1)
    print_result(r.status_code == 200, f"User 1 deletes own todo: {r.status_code}")

    # Verify todo is deleted
    r = requests.put(f"{API_VERSION_URL}/todos/{todo_id}", json=update_data, headers=headers_1)
    print_result(r.status_code == 404, f"Accessing deleted todo returns 404: {r.status_code}")

def test_guest_todos():
    print_header("Testing Public Guest Todos")
    
    # 1. Create a guest todo (no auth headers)
    guest_data = {
        "title": "Guest public idea",
        "body": "Should look clean and nice"
    }
    r = requests.post(f"{API_VERSION_URL}/guest/todos", json=guest_data)
    print_result(r.status_code == 201, f"Create guest todo: {r.status_code}")
    
    # 2. Read all guest todos
    r = requests.get(f"{API_VERSION_URL}/guest/todos")
    print_result(r.status_code == 200, f"Get all guest todos: {r.status_code}")
    if r.status_code == 200:
        guest_list = r.json()
        print_result(len(guest_list) > 0, f"Received {len(guest_list)} public guest todos")
        print_result(all("user_id" not in gt for gt in guest_list), "Public guest todos have no user association field")

if __name__ == "__main__":
    if wait_for_backend():
        test_health()
        t1, t2 = test_auth()
        if t1 and t2:
            test_todos(t1, t2)
        test_guest_todos()
