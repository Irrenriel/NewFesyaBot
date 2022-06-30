import asyncio
import json

from aiokafka import AIOKafkaConsumer

from resources.tools.database import PostgreSQLDatabase


class AIOCW3_API:
    kafka_active = True
    keys = {
        "createAuthCode",
        "grantToken",
        "requestProfile",
        "guildInfo",
        "requestGearInfo",
        "authAdditionalOperation",
        "grantAdditionalOperation",
        "requestStock",
        'cw3-deals',
        'cw3-duels',
        'cw3-offers',
        'cw3-sex_digest',
        'cw3-yellow_pages',
        'cw3-au_digest',
    }

    def __init__(self, loop, db: PostgreSQLDatabase, callbacks: dict):
        if not all([key in self.keys for key in callbacks.keys()]):
            raise Exception("error keys name")
        self.db = db
        self.callbacks = callbacks
        self.consumer = AIOKafkaConsumer(
            *self.callbacks.keys(),
            auto_offset_reset='latest',
            bootstrap_servers=['digest-api.chtwrs.com:9092'],
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            loop=loop
        )
        self.kafka_active = True

    async def start(self):
        await self.consumer.start()

        while True:
            await self.work()
            await asyncio.sleep(10)

    async def work(self):
        async for message in self.consumer:
            await self.callbacks.get(message.topic, print)(message, self.db)

            if not self.kafka_active:
                await self.close()
                break

    async def stop(self):
        self.kafka_active = False

    async def close(self):
        await self.consumer.stop()