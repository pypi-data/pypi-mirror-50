"""Implements task classes.

Defines:
BaseTask - Base task class.
"""

import abc
import json
import uuid

import click

from .broker import Broker


class BaseTask(abc.ABC):
    """Base task class.

    Example Usage:
        class AdderTask(BaseTask):
            task_name = 'AdderTask'
            def run(self, a, b):
                result = a + b
                return result

        adder = AdderTask()
        adder.delay(9, 34)
    """

    task_name = None

    def __init__(self):
        if not self.task_name:
            raise ValueError("Class attribute 'task_name' should be set.")
        self.broker = Broker()
        self.set_status('detached')

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        # Subclasses should implement their run logic here.
        raise NotImplementedError('Task run method must be implemented.')

    def delay(self, *args, **kwargs):
        try:
            task_id = str(uuid.uuid4())
            task = dict(
                task_id=task_id,
                args=json.dumps(args),
                kwargs=json.dumps(kwargs),
            )
            self.broker.enqueue(
                item=task, queue_name=self.task_name)
            self.set_status('enqueued')
            click.echo(f'Queued task: {task_id}')
        except Exception:
            raise Exception(f'Unable to publish task {task_id} to the broker.')  

    def set_status(self, status):
        """Set status of the BaseTask instance. Options are:
        detached - Instantiated, not queued.
        enqueued - Queued via Broker.
        dequeued - Dequeued via Worker.
        running - Running via Worker.
        complete - Run complete.
        """
        if status not in (
                'detached', 'enqueued', 'dequeued', 'running', 'complete'):
            raise ValueError(f'Task status {status!r} not recognized.')
        self.status = status

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.status})")
