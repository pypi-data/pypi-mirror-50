import logging
from typing import Union, Dict

from aiorazemax.drivers import SQSDriver
from aiorazemax.event_manager import EventManager


class MessageConsumer:
    def __init__(self, mapper_factory: Dict, event_manager: Union[EventManager, type(EventManager)], queue_driver: SQSDriver):
        self._mapper_factory = mapper_factory
        self._queue_driver = queue_driver
        self._event_manager = event_manager

    async def process_message(self) -> bool:
        # Receive message
        message = await self._queue_driver.receive_message()

        if not message:
            logging.debug("No messages to process")
            return False

        logging.debug(f"Message type is: {message.event_name}")
        try:
            # Parse message to event
            mapper = self._mapper_factory[message.event_name]
            logging.debug(f"Selected mapper is: {mapper}")

            event = mapper(message)
            logging.debug(f"Event type is: {event.__class__}")

            # Trigger subscribers
            await self._event_manager.trigger(event)
        except Exception as e:  # TODO: specify exceptions...
            logging.error(str(e))
            self._queue_driver.mark_message_unprocessed(message, e)
        else:
            await self._queue_driver.mark_message_processed(message)
        return True
