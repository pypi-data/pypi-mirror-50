# Aiorazemax
[![Build Status](https://travis-ci.com/21Buttons/aiorazemax.svg?branch=master)](https://travis-ci.com/21Buttons/aiorazemax)

✉️ Async communications using AWS SNS + SQS for Python services ✨

## Documentation

### In-Memory event manager

_Show me the code_

```python
from aiorazemax.event_manager import EventManager


class NorthKoreaThreatCreatedEvent:
    def __init__(self, id, target):
        self.id = id
        self.target = target


async def trump_subscriber(event: NorthKoreaThreatCreatedEvent):
    print(f"North korea will attack us or {event.target}!")


EventManager.subscribe(trump_subscriber, NorthKoreaThreatCreatedEvent)
await EventManager.trigger(NorthKoreaThreatCreatedEvent(0, "Mexico"))
```

Result:
```
North korea will attack us or Mexico!
```

### Trigger subscribers from SQS

#### Preconditions

SQS queue has to be subscribed to SNS topic before running the consumer

#### Code

```python
import asyncio

from aiorazemax.consumers import MessageConsumer
from aiorazemax.drivers import SQSDriver
from aiorazemax.event_manager import EventManager
from aiorazemax.publisher import SNSMessagePublisher


aws_settings = {
    'region_name': "",
    'aws_access_key_id': "",
    'aws_secret_access_key': "",
    'endpoint_url': ""
}


class NorthKoreaThreatCreatedEvent:
    def __init__(self, id, target):
        self.id = id
        self.target = target


def kp_message_to_event(event_message):
    message = event_message.body
    # Highly recommended to use Marshmallow to validate
    return NorthKoreaThreatCreatedEvent(message['body']['id'], message['body']['target_name'])


mapper = {
    'KPThreatCreated': kp_message_to_event
}


async def trump_subscriber(event: NorthKoreaThreatCreatedEvent):
    print(f"North korea will attack us or {event.target}!")


async def main():
    EventManager.subscribe(trump_subscriber, NorthKoreaThreatCreatedEvent)

    queue_driver = await SQSDriver.build('korea-threats-queue', aws_settings)
    consumer = MessageConsumer(mapper, EventManager, queue_driver)

    publisher = await SNSMessagePublisher.build('korea-topic', aws_settings)
    await publisher.publish('KPThreatCreated', {'id': 21, 'target_name': 'Portugal'})

    await consumer.process_message()

    await queue_driver.close()
    await publisher.close()


if __name__ == '__main__':
    asyncio.run(main())
```

Result:

```
North korea will attack us or Portugal!
```

## Installing

`pip install aiorazemax`


## Running the tests

To run end to end tests do:
```
make unit-tests
make integration-tests
```

## Authors

* Jairo Vadillo ([@jairovadillo](https://github.com/jairovadillo))

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
