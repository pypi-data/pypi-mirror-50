import logging
import asyncio
from typing import Union

from aioredis import ConnectionsPool,RedisConnection
from aioredis.commands import StringCommandsMixin,GenericCommandsMixin

class RedisLock(object):
    """

    redis 锁的用法，对应async with

    """
    def __init__(self,redis_c:Union[ConnectionsPool,RedisConnection],key,try_times=5,await_times=3):
        self._redis_c = redis_c
        self._key = key
        self._try_times = try_times
        self._await_times = await_times

    async def __aenter__(self):
        status = 0
        for _ in range(self._try_times):
            status = await StringCommandsMixin.msetnx(self._redis_c,self._key,"Redis_lock_add")
            if status==1:
                break
            else:
                logging.debug(f"do not get the lock,could wait and continue")
                await asyncio.sleep(self._await_times)
        if status==0:
            logging.warning(f"do not get the lock on time,could raise error")
            raise Exception("get lock out time")

    async def delete(self):
        """

        留待强制解除锁

        :return:
        """
        await GenericCommandsMixin.delete(self._redis_c,self._key)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.delete()