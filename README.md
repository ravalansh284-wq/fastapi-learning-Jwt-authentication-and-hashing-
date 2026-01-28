# 🚀 FastAPI Authentication System

A professional-grade backend API built from scratch using **FastAPI**. This project demonstrates a complete Authentication and Authorization flow, following modern security best practices.

## 🌟 Key Features (Completed up to Day 7)

* **Secure User Registration:** Passwords are never stored in plain text. Used **Bcrypt** hashing to secure credentials.
* **JWT Authentication:** Implemented JSON Web Tokens (JWT) for stateless, secure user sessions.
* **Dependency Injection:** Clean architecture using FastAPI's `Depends` system to manage database sessions and current user validation.
* **Protected Routes:** Created "VIP" endpoints that only allow access to users with valid, non-expired tokens.
* **Database Management:** Integrated **SQLAlchemy** with **SQLite** for persistent data storage.
* **Data Validation:** Strict input/output validation using **Pydantic** schemas.

## 🛠️ Tech Stack

* **Framework:** FastAPI
* **Language:** Python 3.10+
* **Database:** SQLite / SQLAlchemy ORM
* **Security:** Passlib (Bcrypt), Python-Jose (JWT), OAuth2
* **Server:** Uvicorn

## ⚡ How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/fastapi-learning.git](https://github.com/YOUR_USERNAME/fastapi-learning.git)
    cd fastapi-learning
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt] python-jose[cryptography] python-multipart
    ```

4.  **Run the server:**
    ```bash
    python -m uvicorn main:app --reload
    ```

5.  **Open Swagger UI:**
    Visit `http://127.0.0.1:8000/docs` to test the API interactively.

## 🛣️ API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/signup` | Register a new user (Hashes password) | ❌ No |
| `POST` | `/login` | Login and receive a JWT Bearer Token | ❌ No |
| `GET` | `/users/me` | Get profile details of the logged-in user | 🔒 Yes |

---