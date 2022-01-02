from .banned_cash import BannedUsersCash
from .temp_cash import TempCash, TempAllianceCash
from .users_cash import UsersCash, UserData
from .adv_users_cash import AdvUsersCash, AdvUserData

# Cashes
users = UsersCash()
adv_users = AdvUsersCash()

# Temp Cashes
temp_cash = TempCash()
temp_alliance_cash = TempAllianceCash()

# Banned Cash
banned_users = BannedUsersCash()