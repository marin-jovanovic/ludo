def get_config():
    return {
        "nonExistingUsername": "username 1",
        "nonExistingPassword": "@,<>12#*mdAmf-",
        "incorrectUsername": "1",
        "incorrectPassword": "1",
        "apiURL": "http://localhost:8000",


        "levelIdPrefix": "game ",
        # max number of users per level
        "levelMaxCapacity": 4,
        # how many users will be generated
        "levelUsersGenerated": 4,
        "levelPlayers": {
            "usernamePrefix": "u ",
            "passwordPrefix": "@,<>12#*mdAmf- "
        },
        "levelPath": "level",
        "levelLogPath": "log",

        "boardPath": "board",

    }
