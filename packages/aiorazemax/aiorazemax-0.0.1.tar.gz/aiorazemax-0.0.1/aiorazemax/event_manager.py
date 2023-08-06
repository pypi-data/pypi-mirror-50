import asyncio
import logging
import types
from collections import defaultdict
from typing import Dict


logger = logging.getLogger(__name__)


class EventManager:
    __subscribers: Dict = defaultdict(set)

    @classmethod
    def subscribe(cls, subscriber, event):
        cls.__subscribers[event].add(subscriber)

    @classmethod
    async def trigger(cls, event):
        async_tasks = []
        for subscriber in cls.__subscribers.get(event.__class__, []):
            task = asyncio.create_task(subscriber(event))
            async_tasks.append(task)
        await asyncio.gather(*async_tasks)

    @classmethod
    def _reset(cls):
        """Never call this outside tests!"""
        cls.__subscribers = defaultdict(set)

    @classmethod
    def subscribers(cls) -> Dict:
        return dict(cls.__subscribers)
