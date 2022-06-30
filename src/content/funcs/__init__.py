from logging import info

from resources.tools.database import PostgreSQLDatabase


async def installing_schedulers(db: PostgreSQLDatabase, scheduler, cw3_api):
    await update_l_check_status(db)

    scheduler.add_job(
        {'trigger': 'cron', 'hour': 1, 'minute': 30},
        args=[update_l_check_status, {'db': db}],
        id='l_check_upd_1_30'
    )

    scheduler.add_job(
        {'trigger': 'cron', 'hour': 9, 'minute': 30},
        args=[update_l_check_status, {'db': db}],
        id='l_check_upd_9_30'
    )

    scheduler.add_job(
        {'trigger': 'cron', 'hour': 17, 'minute': 30},
        args=[update_l_check_status, {'db': db}],
        id='l_check_upd_17_30'
    )

    scheduler.add_job(
        {'trigger': 'interval', 'seconds': 3},
        args=[run_cw3_api, {'scheduler': scheduler, 'cw3_api': cw3_api}],
        id='run_cw3_api'
    )


async def update_l_check_status(db: PostgreSQLDatabase):
    await db.execute('UPDATE settings SET data_bool = True WHERE var = $1', ['l_check_upd'])
    info('▻ Updated "l_check_upd" var! /l_check is available now!')


async def run_cw3_api(scheduler, cw3_api):
    scheduler.remove_job('run_cw3_api')

    await cw3_api.start()
