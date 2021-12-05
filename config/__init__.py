# Development:
# Switch develop instances by this vars
TestMode: bool = True
LoggingMode: bool = False

# Variables to connect:
# Aiogram Bot
# BOT_TOKEN: str = 'bot_token'
BOT_TOKEN: str = 'bot_token'
PARSE_MODE: str = 'HTML'

# Databases
# !!! Please keep your database files in the config/ folder !!!
# You can create multiple paths and instantiate with them
DB_PATH_1: str = 'config/ExampleDataBase.db'

# Other variables:
# Roles
ADMINS_ID: list[int] = []

# Global constants:
# To import it anywhere or use it to instantiate it into resources / models