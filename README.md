# Credix Assessment Project

This project consists of a backend built with **FastAPI** and a frontend built with **React** and **Vite**. Below are the instructions to set up and run the project locally.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Backend Setup](#backend-setup)
3. [Frontend Setup](#frontend-setup)
4. [Running the Project](#running-the-project)
5. [Task Commands (Backend)](#task-commands-backend)
6. [Project Structure](#project-structure)

---

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python >=3.12** (for the backend)
- **Node.js** (for the frontend)
- **Poetry** (Python dependency management)
- **Git** (optional, for cloning the repository)

---

**Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/rafaeldiasbh/credixAssessment.git
   ```

## Backend Setup
1. **Install dependencies using Poetry:**

```bash
cd credixAssessment/backend 
poetry install
```
Database:

Database is SQLite and its configured to be created and "migrated" automatically.
No extra configuration needed.

## Frontend Setup
Navigate to the frontend directory:

```bash
cd ../frontend
```

1. **Install dependencies using npm:**

```bash
npm install
```

## Running the Project

**Backend**
To run the backend, use the following command:

```bash
cd ../backend
poetry run task run
```
This will start the FastAPI server with hot-reloading enabled. The backend will be accessible at:

http://localhost:8000

**Frontend**
To run the frontend, use the following command:

```bash
cd ../frontend
npm run dev
```
or
```bash
cd ../frontend
vite
```
This will start the Vite development server. The frontend will be accessible at:

http://localhost:5173

## Task Commands (Backend)
The backend includes several predefined tasks for development and testing. These tasks are defined in the pyproject.toml file and can be run using Poetry.

**Available Tasks**
Run the backend server:
```bash
task run
```

Run automated tests:

```bash
task test
```

Generate test coverage report:

```bash
task post_test
```

Lint the code:

```bash
task lint
```

Format the code:

```bash
task format
```

## Project Structure

Backend follows the 3tier Achitecture 
1- presentation on the API folder
2- Business logic on the service folder
3- Data/Storage on the model folder

**Backend**

```bash
credixAssessment/backend/
├── src/
│   ├── main.py                # FastAPI application entry point
│   ├── api/v1/
│   │   ├── endpoints
│   │   │   ├── orders.py      # Order-related API endpoints
│   │   │   ├── hello.py       # Hello Word route to ensure backend is not broken
│   ├── core/
│   │   ├── db.py              # Database configuration
│   ├── models/                # ORM entities folder
│   │   ├── order.py           # Order model 
│   │   ├── product.py         # Product model
│   ├── schemas/
│   │   ├── hello.py           # Pydantic schema for hello
│   │   ├── order.py           # Pydantic schemas for orders
│   ├── services/
│   │   ├── hello_service.py   # Business logic for hello word
│   │   ├── order_service.py   # Business logic for orders
├── tests/                     # Automated tests folder
│   ├── test_hello.py          # Tests for helloWorld functionality
│   ├── test_orders.py         # Tests for order-related functionality
├── pyproject.toml             # Poetry configuration and dependencies
```

**Frontend**

Frontend uses the component based Architecture

```bash
credixAssessment/frontend/
├── src/
│   ├── main.tsx               # React application entry point
│   ├── components/            # React components
│   ├── pages/                 # React pages
├── public/                    # Static assets
├── package.json               # npm dependencies and scripts
```