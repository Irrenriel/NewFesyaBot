import traceback
from datetime import datetime, timedelta
from logging import info, error

from resources.tools.database import PostgreSQLDatabase
from src.content import WS_SHOPS_INSERT
from src.content.cashes.guru_cash import RawGuru, GuruShops


async def shops_formatter(shops_pool, db: PostgreSQLDatabase):
    now = datetime.now()
    pool_date = datetime.fromtimestamp(int(shops_pool.timestamp)/1000.0)
    if now - pool_date > timedelta(minutes=5):
        return

    info('Starting update shops!')

    try:
        # Date
        await db.execute('UPDATE settings_date SET date = $1 WHERE var = $2', [pool_date, 'ws_shops_upd'])
        GuruShops.update_callback_date(pool_date)

        # Cash-result to return with all gurus
        gurus = [RawGuru(**ws, date=pool_date) for ws in shops_pool.value]
        await db.execute(WS_SHOPS_INSERT, [guru.get_data() for guru in gurus], many=True)
        GuruShops.startup_update(shops_pool.value)

    except Exception:
        error('Happend error in shops updating!')
        error(traceback.format_exc())

    finally:
        info('Finishing update shops!')


# async def cw3_au_digest_formatter(lots_pool, db: PostgreSQLDatabase):
#     '''
#     Auction Functional
#     '''
#     now = datetime.now()
#     pool_date = datetime.fromtimestamp(int(lots_pool.timestamp)/1000.0)
#     if now - pool_date > timedelta(minutes=3):
#         return
#
#     #print(True)
#     lots_db = {i: [*i] for i in await db.fetch('SELECT * FROM auction')}
#     insert_req = '''INSERT OR REPLACE INTO auction VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'''
#
#     update_lots = []
#
#     for l in lots_pool.value:
#         # if l.get('sellerTag') != 'AT':
#         #     return
#
#         update_lots.append((
#             l.get('lotId'), l.get('status'),
#             l.get('sellerName'), l.get('sellerTag', ''), l.get('sellerCastle'),
#             l.get('startedAt'), l.get('endAt'), l.get('finishedAt'),
#             l.get('itemName'), l.get('condition', ''), l.get('stats', ''),
#             l.get('buyerCastle', ''), l.get('price', 0)
#         ))
#
#     db.querymany(insert_req, update_lots)
