# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['countdown_event']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'countdown-event',
    'version': '0.1.0',
    'description': 'An asyncio event which blocks until the count reaches zero',
    'long_description': '# countdown-event\n\nA synchronization class which blocks when the count is not zero.\n\nHere\'s an example\n\n```python\nimport asyncio\nfrom countdown_event import CountdownEvent\n\nasync def long_running_task(countdown_event,cancellation_event):\n    count = countdown_event.increment()\n    print(f\'incremented count to {count}\')\n    try:\n        print(\'Waiting for cancellation event\')\n        await cancellation_event.wait()\n    finally:\n        count = countdown_event.decrement()\n        print(f\'decremented count to {count}\')\n\nasync def stop_tasks(secs, countdown_event, cancellation_event):\n    print(f\'waiting {secs} seconds before setting the cancellation event\')\n    await asyncio.sleep(secs)\n    print(\'setting the cancellation event\')\n    cancellation_event.set()\n    print(\'waiting for tasks to finish\')\n    await countdown_event.wait()\n    print(\'countdown event cleared\')\n\nasync def main_async():\n    cancellation_event = asyncio.Event()\n    countdown_event = CountdownEvent()\n    tasks = [\n        long_running_task(countdown_event, cancellation_event),\n        long_running_task(countdown_event, cancellation_event),\n        long_running_task(countdown_event, cancellation_event),\n        stop_tasks(5, countdown_event, cancellation_event)\n    ]\n    await asyncio.wait(tasks)\n    assert countdown_event.count == 0\n    print("done")\n\nif __name__ == "__main__":\n    asyncio.run(main_async())\n```\n\nHere\'s the output.\n\n```\nincremented count to 1\nWaiting for cancellation event\nincremented count to 2\nWaiting for cancellation event\nwaiting 5 seconds before setting the cancellation event\nincremented count to 3\nWaiting for cancellation event\nsetting the cancellation event\nwaiting for tasks to finish\ndecremented count to 2\ndecremented count to 1\ndecremented count to 0\ncountdown event cleared\ndone\n```',
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@gmail.com',
    'url': 'https://github.com/rob-blackbourn/countdown-event',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
