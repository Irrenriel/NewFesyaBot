from aiogram.dispatcher.filters.state import StatesGroup, State


class StateOn(StatesGroup):
    # Main
    Registration = State()

    # Alliance
    AllianceGetCode = State()
    AllianceGetMenu = State()
    AllianceGetRoster = State()

    # Workbench
    WorkBenchActive = State()

    # AdvGuild
    AdvStart = State()
