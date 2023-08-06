"""Implements broker classes.

Defines:
Broker
"""

import datetime as dt
import sqlite3

from soon_kyoo.db_config import db_path


class Broker:
    """Implements a basic FIFO queue using SQLite.
    """

    def enqueue(self, item, queue_name):
        con = sqlite3.connect(str(db_path))
        with con:
            c = con.execute(
                'SELECT position FROM queue ORDER BY position DESC')
            max_position = c.fetchone()
            new_position = max_position[0] + 1 if max_position else 0
            con.execute('INSERT INTO queue VALUES (?, ?, ?, ?, ?, ?)', (
                item['task_id'], queue_name, new_position, item['args'],
                item['kwargs'], dt.datetime.now(),
            ))
        con.close()

    def dequeue(self, queue_name):
        con = sqlite3.connect(str(db_path))
        con.row_factory = sqlite3.Row
        with con:
            c = con.execute(f'''SELECT * FROM queue
                WHERE queue_name = {queue_name!r}
                ORDER BY position ASC''')
            dequeued_item = c.fetchone()
            item_id = dequeued_item['task_id']
            c = con.execute(f'DELETE FROM queue WHERE task_id = {item_id!r}')
        con.close()
        if not dequeued_item:
            return
        return dequeued_item
