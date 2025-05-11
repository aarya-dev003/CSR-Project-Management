# CSR Project Management System

## Overview
The CSR Project Management System is a web application built with Streamlit for managing Corporate Social Responsibility (CSR) projects. It allows users to create, view, update, delete, and approve projects, with features for managing project details, agency details, financial details, location/beneficiary information, and generating reports. The app includes user authentication, role-based access (e.g., approvers), and a dashboard for project management.

## Prerequisites
Ensure the following are installed before running the project:

- **Python 3.8+**: Required to run the application.
- **pip**: Python package manager for installing dependencies.
- **Virtual Environment (Recommended)**: To isolate project dependencies.
- **PostgreSQL**: Used as the database. Install PostgreSQL on your system.
- **Git**: For cloning the repository if hosted on a version control system.

## Installation

### 1. Clone the Repository (Optional)
If the project is hosted on a Git repository, clone it:

```bash
git clone https://github.com/aarya-dev003/CSR-Project-Management
cd CSR-Project-Management
```

If you already have the project files, navigate to the project directory:

```bash
cd path/to/CSR-Project-Management
```

### 2. Set Up PostgreSQL
1. **Install PostgreSQL**:
   - Download and install PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/).
   - During installation, set a password for the `postgres` user (you’ll need this later).
   - Ensure the PostgreSQL server is running.

2. **Create the Database**:
   - Open a terminal or PostgreSQL client (e.g., `psql` or pgAdmin).
   - Log in as the `postgres` user:
     ```bash
     psql -U postgres
     ```
   - Create a database named `csr_projects`:
     ```sql
     CREATE DATABASE csr_projects;
     ```
   - Exit the `psql` shell:
     ```sql
     \q
     ```

3. **Configure Database Access**:
   - The project uses a `.env` file to store database credentials. Create a `.env` file in the project directory with the following content:
     ```
     DB_HOST=localhost
     DB_NAME=csr_projects
     DB_USER=postgres
     DB_PASSWORD=your_postgres_password
     DB_PORT=5432
     ```
   - Replace `your_postgres_password` with the password you set for the `postgres` user.

### 3. Set Up a Virtual Environment (Recommended)
Create and activate a virtual environment:

#### On Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
The project requires several Python libraries (see "Python Libraries" section below). If a `requirements.txt` file exists, install dependencies with:

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn’t exist, create it with the following content:

```
streamlit==1.38.0
python-dotenv==1.0.1
psycopg2-binary==2.9.9
pandas==2.2.3
```

Then run:

```bash
pip install -r requirements.txt
```

Alternatively, install the packages manually:

```bash
pip install streamlit python-dotenv psycopg2-binary pandas
```

### 5. Verify Project Files
Ensure the following files are in the project directory:

- `app.py`: Main application file.
- `project_details.py`: Manages the Project Details tab.
- `agency_details.py`: Manages the Agency Details tab.
- `financial_details.py`: Manages the Financial Details tab.
- `location_beneficiary.py`: Manages the Location/Beneficiary tab.
- `other_information.py`: Manages the Other Information tab.
- `db_helper.py`: Handles database operations (PostgreSQL).
- `.env`: Configuration file for database credentials.

## Running the Project

### 1. Start the Streamlit Server
From the project directory, with the virtual environment activated, run:

```bash
streamlit run app.py
```

### 2. Access the Application
- Streamlit will launch a local server and open the app in your default browser at `http://localhost:8501`.
- If the browser doesn’t open, navigate to `http://localhost:8501` manually.

### 3. Log In
Use the default credentials to log in:
- **CSR Manager**:
  - Username: `user1`
  - Password: `user123`
- **Approver**:
  - Username: `approver1`
  - Password: `approve123`

**Note**: These credentials are stored in the PostgreSQL database. The database tables are created automatically on first run if they don’t exist.

## Usage

### Dashboard
After logging in, the dashboard provides the following options:
- **Create New Project**: Add a new CSR project.
- **View Projects**: List all projects in a table.
- **Update Project**: Edit an existing project (only for the project owner).
- **Delete Project**: Remove a project (only for the project owner).
- **Approve Project**: Approve a project (only for approver roles).
- **View Report**: Generate a detailed report of all projects.

### Creating a Project
1. Click "Create New Project" on the dashboard.
2. Fill in the required fields across the tabs (e.g., Project Details, Financial Details).
3. Click "Save Project" in the sidebar to save.

### Updating a Project
1. Click "Update Project" on the dashboard.
2. Select a project and click "Edit".
3. Modify the fields and click "Update Project".

### Approving a Project
1. Log in as an approver (e.g., `approver1`).
2. Click "Approve Project" on the dashboard.
3. Select a project with "Saved" status and click "Approve".


## Python Libraries
The project uses the following Python libraries:

- **`streamlit`**: Framework for building the web application (version 1.38.0).
- **`python-dotenv`**: Loads environment variables from a `.env` file for database configuration (version 1.0.1).
- **`psycopg2-binary`**: PostgreSQL adapter for Python to interact with the database (version 2.9.9).
- **`pandas`**: Used for data manipulation and reporting (version 2.2.3).
