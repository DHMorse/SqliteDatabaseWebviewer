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

