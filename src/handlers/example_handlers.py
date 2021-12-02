# Firstly, import Dispatcher
from resources.models import dp_1, dp_2

# Secondly, import filters, states and functions
from resources.tools.cfilters import Command, IsUser
from resources.tools.states import ExampleState
from src.functions import test


'''<<<-----   EXAMPLE FUNCs   ----->>>'''
# You should code handlers in such format
dp_1.register_message_handler(
    test,  # Function in the first row
    Command('test'), IsUser(is_admin=False),  # Filters in the next rows
    state=None  # The last 2 rows is optional, adding state filter and comments
    # State: None -> ExampleState.First (by if)
)

dp_1.register_message_handler(
    test,  # Function in the first row
    Command('test'), IsUser(is_admin=False),  # Filters in the next rows
    state=ExampleState.First  # The last 2 rows is optional, adding state filter and comments
    # State: ExampleState.First -> None (by if)
)

dp_2.register_message_handler(
    test,  # Function in the first row
    Command('test'), IsUser(is_admin=False),  # Filters in the next rows
    state=None  # The last 2 rows is optional, adding state filter and comments
    # State: None -> ExampleState.First (by if)
)

dp_2.register_message_handler(
    test,  # Function in the first row
    Command('test'), IsUser(is_admin=False),  # Filters in the next rows
    state=ExampleState.First  # The last 2 rows is optional, adding state filter and comments
    # State: ExampleState.First -> None (by if)
)

# That`s all what you need to know about handlers!