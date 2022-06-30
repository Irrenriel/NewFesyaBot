import traceback
from datetime import datetime, timedelta
from logging import info, error

from resources.tools.database import PostgreSQLDatabase
from src.content import WS_SHOPS_INSERT
from src.content.cashes.guru_cash import RawGuru


async def shops_formatter(shops_pool, db: PostgreSQLDatabase):
    now = datetime.now()
    pool_date = datetime.fromtimestamp(int(shops_pool.timestamp)/1000.0)
    if now - pool_date > timedelta(minutes=5):
        return

    info('Starting update shops!')

    try:
        # Date
        await db.execute('UPDATE settings_date SET date = $1 WHERE var = $2', [pool_date, 'ws_shops_upd'])

        # Cash-result to return with all gurus
        gurus = []

        for ws in shops_pool.value:
            # if ws.get('link') == 'MYdnt':
            #     print(ws)

            gurus.append(RawGuru(**ws, date=pool_date))

        await db.execute(WS_SHOPS_INSERT, [guru.get_data() for guru in gurus], many=True)

    except Exception:
        error('Happend error in shops updating!')
        error(traceback.format_exc())

    finally:
        info('Finishing update shops!')


# Old functional
# def shops_formatter(shops_pool):
#     now = datetime.datetime.now()
#     pool_date = datetime.datetime.fromtimestamp(int(shops_pool.timestamp)/1000.0)
#     if now - pool_date > datetime.timedelta(minutes=5):
#         return
#     # print('Started')
#
#     # print(True)
#     # Date
#     GS.reset_date_info(pool_date.strftime('%Y-%m-%d %H:%M:%S'))
#
#     # Cash-result to return with all gurus
#     spec_cash = {'boots': [], 'armor': [], 'coat': [], 'gloves': [], 'helmet': [], 'shield': [], 'weapon': []}
#     db_cash = []
#     db_req = '''INSERT INTO ws_shops (
#     link, name, ownerTag, ownerName, ownerCastle, mana, offers, qualityCraftLevel, qualityCraftSpec, qualityCraftPerc
#     ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
#
#     for ws in shops_pool.value:
#         # if ws.get('link') == 'S820X':
#         #     print(ws)
#         # Quality Craft and Checking
#         qc_lvl = ws.get('qualityCraftLevel')
#
#         s_specs = ws.get('specializations')
#         if ws.get('specialization') is None or qc_lvl == 0 or 'quality_craft' not in s_specs.keys():
#             continue
#
#         # Player Info
#         mana = ws.get('mana')
#         if mana == 0:
#             continue
#         link, name = ws.get('link'), ws.get('ownerName')
#         castle, tag = ws.get('ownerCastle'), ws.get('ownerTag')
#         offers, ws_name = json.dumps(ws.get('offers')), ws.get('name')
#
#         # Dict of Guru Spec
#         specs_dict = s_specs.get('quality_craft').get('Values')
#         for spec in specs_dict.items():
#             if spec[1] != 100:
#                 continue
#             spec_cash.get(spec[0]).append(Guru(link, castle, tag, name, qc_lvl, spec[0], spec[1], mana))
#             db_cash.append((link, ws_name, tag, name, castle, mana, offers, qc_lvl, spec[0], spec[1]))
#
#     db.query('DELETE FROM ws_shops')
#     db.querymany(db_req, db_cash)
#     GS.reset_shops_info(spec_cash)


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
