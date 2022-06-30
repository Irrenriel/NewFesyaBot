import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler


class MyScheduler:
    def __init__(self, loop):
        self.loop = loop
        self.scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        self.scheduler.start()

    def afs(self, func, params: dict, call=None):
        def result(res):
            if call:
                call(res.result())
        asyncio.ensure_future(func(**params), loop=self.loop).add_done_callback(result)

    def add_job(self, kwargs: dict, args: list, id: str):
        self.scheduler.add_job(self.afs, **kwargs, args=args, id=str(id))

    def remove_job(self, id):
        self.scheduler.remove_job(str(id))

    def get_job(self, id):
        return self.scheduler.get_job(str(id))
