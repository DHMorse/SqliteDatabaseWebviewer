import os
import time
import json
from flask import request


def isClientLoggedIn() -> bool:
    """Function to check if the client is logged in based off their current IP address."""

    global loggedInUsers
    clientIp = request.remote_addr
    return any(clientIp == user[0] for user in loggedInUsers)

def hasPermission(user: dict, table: str) -> bool:
    """
    Function to check if the user has permission to access the table.
    Args:
        USER: dict - A dictionary containing the user data.
        table: str - The table name to check if the user has permission to access.
    Returns:
        bool - A boolean value to determine if the user has permission to access the table.
    """
    
    if '*' in user['tables']:
        return True
    elif table in user['tables']:
        return True
    else:
        return False

def handleSettingsFile(settingsFilepath: str) -> tuple[str, bool, bool, int, dict[str, dict[str, str] | list[str | None]], str, int, bool]:
    """
    Function to handle the settings file. This function will read the settings file and return the necessary data to run the application.
    Args:
        settingsFilepath: str - The file path to the settings file.
    Returns:
        DATABASE: str - The file path to the database file.
        PASSWORD_PROTECTION: bool - A boolean value to determine if password protection is enabled.
        USERS: dict - A dictionary containing the users and their permissions.
        HOST: str - The host IP address to run the application on.
        PORT: int - The port number to run the application on.
        DEBUG_MODE: bool - A boolean value to determine if debug mode is enabled.
    Raises:
        FileNotFoundError: If the settings file is not found at the file location.
        json.JSONDecodeError: If there is an error decoding the JSON file.
        ValueError: If there is no password found for the admin user or any other user with admin permissions.
        ValueError: If there is no password KEY found for a user.
        ValueError: If there is no tables KEY found for a user.
        ValueError: If there is no permissions KEY found for a user.
    """

    if not os.path.exists(settingsFilepath):
        raise FileNotFoundError(f"Settings file not found at file location: {settingsFilepath}")

    with open(settingsFilepath) as file:
        try:
            settings: dict = json.load(file)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error decoding JSON file: {e} at file location: {settingsFilepath}", e.doc, e.pos)



    DATABASE: str = settings['DATABASE_FILEPATH']
    if not os.path.exists(DATABASE):
        raise FileNotFoundError(f"Database file not found at file location: {DATABASE}")



    PASSWORD_PROTECTION: bool = settings['PASSWORD_PROTECTION']
    if PASSWORD_PROTECTION:
        if not settings['users']['admin']['password']:
            for user in settings['users']:
                if not 'admin' in settings['users'][user]['permissions']:
                    continue
                if settings['users'][user]['password']:
                    PASSWORD: str = settings['users'][user]['password']
                    break
            if not PASSWORD:
                raise ValueError("No password found for admin user or any other user with admin permissions.")
    else:
        PASSWORD = None



    LOG_OUT_USERS: bool = settings['LOG_OUT_USERS']
    if type(LOG_OUT_USERS) != bool:
        raise ValueError(f"LOG_OUT_USERS must be a boolean value, not {type(LOG_OUT_USERS)}.")



    LOG_OUT_USERS_AFTER: int = settings['LOG_OUT_USERS_AFTER']
    if type(LOG_OUT_USERS_AFTER) != int:
        raise ValueError(f"LOG_OUT_USERS_AFTER must be an integer value of seconds, not {type(LOG_OUT_USERS_AFTER)}.")
    if LOG_OUT_USERS_AFTER <= 0:
        raise ValueError("LOG_OUT_USERS_AFTER must be greater than 0.")



    USERS: dict = settings['users']
    for user in USERS:
        if not 'password' in USERS[user]:
            raise ValueError(f"No password KEY found for user: {user}")

        if not 'tables' in USERS[user]:
            raise ValueError(f"No tables KEY found for user: {user}")
        
        if not USERS[user]['permissions']:
            raise ValueError(f"No permissions KEY found for user: {user}")



    if settings['HOST'] == 'default':
        HOST = '0.0.0.0'
    else:
        HOST: str = settings['HOST']
        # add some sort of checking here for valid IP address



    if settings['PORT'] == 'default':
        PORT = 5000
    else:    
        PORT = settings['PORT']
        # add some sort of checking here for valid port number



    if settings['DEBUG']:
        DEBUG_MODE = True
    else:
        DEBUG_MODE = False

    return DATABASE, PASSWORD_PROTECTION, LOG_OUT_USERS, LOG_OUT_USERS_AFTER, USERS, HOST, PORT, DEBUG_MODE

def clearLoggedInUsers(lotOutAfter: int) -> None:
    """
    Function to clear the logged in users list after a certain amount of time.
    Args:
        lotOutAfter: int - The amount of time in seconds to clear the logged in users list.
    """
    global loggedInUsers
    while True:
        loggedInUsers = []
        time.sleep(lotOutAfter)  # Sleep for 1 hour