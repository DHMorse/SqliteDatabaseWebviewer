# SQLite Database Webviewer

[![Python](https://img.shields.io/badge/Python_3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![uv](https://img.shields.io/badge/uv-FFE873?style=flat&logo=python&logoColor=black)](https://github.com/astral-sh/uv)
[![Flask](https://img.shields.io/badge/Flask-3daabf?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Node.js](https://img.shields.io/badge/Node.js_DevDep-339933?style=flat&logo=node.js&logoColor=white)](https://nodejs.org/)
[![npm](https://img.shields.io/badge/npm_DevDep-CB3837?style=flat&logo=npm&logoColor=white)](https://www.npmjs.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript_DevDep-3178C6?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

A secure web-based SQLite database viewer that provides a user-friendly interface for exploring and managing SQLite databases with role-based access control.

## 🚀 Features

- **Secure Access Control**: Role-based user authentication with customizable permissions
- **Table Management**: View and explore database tables with a clean interface
- **User Management**: Configure user access levels and permissions per table
- **Auto Logout**: Automatic session timeout for enhanced security
- **Configurable Settings**: Easy configuration through `settings.json`

## 📋 Prerequisites

- Python 3.10 or higher
- SQLite3
- uv (recommended for faster dependency management)

## 🔧 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/404-5971/sqliteDatabaseWebviewer.git
   cd sqliteDatabaseWebviewer
   ```

2. Configure the `settings.json` file:
   ```json
   {
     "DATABASE_FILEPATH": "./data/your_database.db",
     "PASSWORD_PROTECTION": true,
     "LOG_OUT_USERS": true,
     "LOG_OUT_USERS_AFTER": 3600,
     "users": {
       "admin": {
         "password": "admin",
         "tables": ["*"],
         "permissions": ["*"]
       }
     },
     "HOST": "default",
     "PORT": "default",
     "DEBUG": false
   }
   ```

## 🖥️ Usage

1. Start the application:

   ```bash
   ./run.sh
   ```

   or

   ```batch
   .\run.bat
   ```

2. Open your browser and navigate to:

   ```
   http://localhost:5000
   ```

3. Log in with your configured credentials and start exploring your database.

## 📁 Project Structure

```
sqliteDatabaseWebviewer/
├── src/                   # Source code directory
│   ├── app.py            # Main Flask application
│   ├── helperFunctions.py # Helper functions and utilities
│   ├── static/           # Static assets
│   └── templates/        # HTML templates
├── data/                 # Database storage directory
├── .python-version       # Python version specification
├── pyproject.toml        # Project dependencies and metadata
├── uv.lock              # uv dependency lock file
├── run.sh               # Setup and run script
└── settings.json        # Application configuration
```

## ⚙️ Configuration

### User Management

Configure user access in `settings.json`:

```json
"users": {
    "username": {
        "password": "user_password",
        "tables": ["table1", "table2"],  // or "*" for all tables
        "permissions": ["*"]             // or specific permissions
    }
}
```

### Security Settings

- `PASSWORD_PROTECTION`: Enable/disable authentication
- `LOG_OUT_USERS`: Enable automatic logout
- `LOG_OUT_USERS_AFTER`: Set timeout in seconds

## 📄 License

Licensed under the [GNU General Public License v3.0](LICENSE).

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

---

Happy database exploring! 🚀

# Settings.json Configuration Guide

This document provides an explanation of all fields in the `settings.json` file.

## General Settings

- **`DATABASE_FILEPATH`** (string): Specifies the file path to the SQLite database file.
- **`PASSWORD_PROTECTION`** (boolean): Enables (`true`) or disables (`false`) password protection for the system.
- **`LOG_OUT_USERS`** (boolean): Determines whether users should be logged out after a set time of inactivity.
- **`LOG_OUT_USERS_AFTER`** (integer): Defines the logout timeout in seconds if `LOG_OUT_USERS` is set to `true`.

## User Settings

The `users` object contains configurations for individual users. Each user has the following properties:

- **`password`** (string): The user's password.
- **`tables`** (array): Lists the database tables the user has access to. A value of `"*"` grants access to all tables, while `null` means no access. You can also specify individual tables by name.
- **`permissions`** (array): Lists the SQL operations the user is allowed to perform. A value of `"*"` grants all permissions, while `null` means no permissions. You can also specify individual permissions by name. BUT THIS IS NOT IMPLEMENTED YET.

### Example Users

#### `admin`

- Password: `admin`
- Tables: All (`"*"`)
- Permissions: All (`"*"`)

#### `John Doe`

- Password: `user`
- Tables: None (`null`)
- Permissions: None (`null`)

## Server Configuration

- **`HOST`** (string): Defines the hostname or IP address for the server. The value `"default"` means it uses the default host configuration.
- **`PORT`** (string): Defines the port number for the server. The value `"default"` means it uses the default port.
- **`DEBUG`** (boolean): Enables (`true`) or disables (`false`) debug mode for the server.
