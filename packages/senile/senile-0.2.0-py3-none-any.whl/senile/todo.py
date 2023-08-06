
from senile import database as db
from texttable import Texttable
from time import time
import datetime
import json
import logging
import os
import uuid

data_file = os.path.expanduser('~/.senile')
logger = logging.getLogger(__name__)

status_desc = {
    'hidden': -1,
    'done': 0,
    'todo': 1,
    'active': 2,
    }

def get_tasks_per_status(status):
    tasks_query = """
        SELECT uuid FROM tasks
        WHERE tasks.status = {};
        """.format(status)
    res = db.execute(tasks_query)
    tasks = [ Task.load(x[0]) for x in res ]
    return tasks

def get_tags_count():
    tags_query = """
        SELECT COUNT(tag), tag
        FROM task_tags
        GROUP BY tag ;
        """
    res = db.execute(tags_query)
    return sorted(res, key=lambda x: x[0], reverse=True)

def find_tasks(data):
    include_tags = set()
    exclude_tags = set()
    word_search = set()
    tasks = None
    for item in data:
        if item[0] == '+':
            include_tags.add(item[1:])
        elif item[0] == '-':
            exclude_tags.add(item[1:])
        else:
            word_search.add(item)
    tasks_query = """
        SELECT uuid from tasks
        INNER JOIN task_tags
        ON tasks.uuid = task_tags.task_id
        """
    if len(word_search):
        tasks_query +=  """
            WHERE 0
            """
        for word in word_search:
            tasks_query += """
            OR tasks.text LIKE '%{}%'
            """.format(word)
    tasks_query +="""
        GROUP BY tasks.uuid
        HAVING 1
        """
    for tag in include_tags:
        tasks_query += """
        AND SUM(task_tags.tag = '{}')
        """.format(tag)
    for tag in exclude_tags:
        tasks_query += """
        AND NOT SUM(task_tags.tag = '{}')
        """.format(tag)
    tasks_query += """
        ORDER BY
        tasks.status DESC,
        tasks.id ASC ;
        """
    res = db.execute(tasks_query)
    tasks = [ Task.load(x[0]) for x in res ]
    return tasks

def task_table(data, hidden=False): # pragma: no cover
    "List tasks in ascii table."
    table = Texttable()
    table.header(['id', 'uuid', 'tags', 'text', 'duration', 'status'])
    table.set_cols_align(["r", "l", "l", "l", "l", "l"])
    table.set_cols_dtype(['t', 't', 't', 't', 't', 't'])
    table.set_header_align(["r", "l", "l", "l", "l", "l"])
    table.set_deco(Texttable.HEADER)
    for task in find_tasks(data):
        if task.status == status_desc['hidden']:
            if not hidden:
                continue
        status_text = {v: k for k, v in status_desc.items()}[task.status]
        table.add_row([
            task.id if task.id >= 0 else "-",
            task.uuid.split('-')[0],
            ' '.join(task.tags),
            task.text,
            task.calc_duration(),
            status_text,
            ])
    return table.draw()

class Task(object):
    "Task entry."
    
    def __init__(self):
        self.uuid = str(uuid.uuid1())
        self.id = 0
        self.text = ''
        self.tags = set()
        self.status = status_desc['todo']
        self.created_time = time()
        self.modified_time = self.created_time
        self.start_time = 0
        self.done_time = 0
        self.duration = 0

    def __eq__(self, other):
        return self.uuid == other.uuid

    def modify(self, options):
        "Parses and populates data in options."

        text = []
        logger.info("Updating data in task: {}".format(self.uuid))
        for option in options:
            if option[0] == '+':
                logger.info("Adding tag '{}' in task: {}".format(option[1:], self.uuid))
                self.tags.add(option[1:])
            elif option[0] == '-':
                try:
                    logger.info("Removing tag '{}' in task: {}".format(option[1:], self.uuid))
                    self.tags.remove(option[1:])
                except KeyError:
                    # the tag was not there
                    pass
            else:
                logger.info("Changing text in task: {}".format(self.uuid))
                text.append(option)
        if text: self.text = " ".join(text)
        self.modified_time = time()

    def hide(self):
        if self.status == status_desc['hidden']:
            logger.warning("Task was already hidden: {}".format(self.uuid))
            return
        self.status = status_desc['hidden']
        self.id = 0

    def done(self):
        if self.status in (status_desc['done'], status_desc['hidden']):
            return
        self.done_time = time()
        if self.status == status_desc['active']:
            self.duration += self.done_time - self.start_time
        self.status = status_desc['done']

    def todo(self):
        if self.status == status_desc['todo']:
            logger.warning("Task was already todo: {}".format(self.uuid))
            return
        if self.status == status_desc['active']:
            self.duration += time() - self.start_time
        self.status = status_desc['todo']

    def start(self):
        if self.status == status_desc['active']:
            logger.warning("Task was already started: {}".format(self.uuid))
            return
        self.start_time = time()
        self.status = status_desc['active']
        self.done_time = 0

    def stop(self):
        if self.status != status_desc['active']:
            logger.warning("Task was not started: {}".format(self.uuid))
            return
        self.todo()

    def calc_duration(self):
        dur = 0
        if self.status == status_desc['active']:
            dur = self.duration + time() - self.start_time
        else:
            dur = self.duration
        return str(datetime.timedelta(seconds=int(dur)))

    def __str__(self):
        return self.text
    
    def info(self):
        inf = "{}|{}\n{}\n\nstatus: {}\ncreated: {}\nmodified: {}\ndone: {}\n"
        inf += "duration: {}\n"
        inf = inf.format(
                self.id,
                self.uuid,
                self.text,
                self.status,
                self.created_time,
                self.modified_time,
                self.done_time,
                self.duration,
                )
        return inf

    def load(ident):
        task_sql = None
        if len(ident) == 8 or '-' in ident:
            task_sql = """
                SELECT * FROM tasks
                WHERE tasks.uuid LIKE '{}%';
                """.format(ident)
        else:
            task_sql = """
                SELECT * FROM tasks
                WHERE tasks.id = '{}'
                AND tasks.status > 0;
                """.format(ident)
        res = db.execute(task_sql)
        if len(res) > 1:
            logger.warning("Found multiple tasks with id '{}'.".format(ident))
            return None
        if len(res) < 1:
            logger.warning("Task with id '{}' not found.".format(ident))
            return None
        task = Task()
        task.uuid           = res[0][0]
        task.id             = res[0][1]
        task.text           = res[0][2]
        task.status         = res[0][3]
        task.created_time   = res[0][4]
        task.modified_time  = res[0][5]
        task.start_time     = res[0][6]
        task.done_time      = res[0][7]
        task.duration       = res[0][8]
        tags_sql = """
            SELECT tag FROM task_tags
            WHERE task_id = '{}';
        """.format(task.uuid)
        res = db.execute(tags_sql)
        for r in res:
            task.tags.add(r[0])
        return task

    def save(self):
        if not self.text:
            logger.error("Can't add task with no description.")
            return
        if self.id < 1 and self.status != status_desc['hidden']:
            ids_query = """
                SELECT id from tasks;
                """
            ids = [ x[0] for x in db.execute(ids_query) ]
            x = 1
            while True:
                if x not in ids: break
                else: x+=1
            self.id = x
        if self.status == status_desc['hidden']:
            self.id = 0
        logger.info("Saving task: {}".format(self.uuid))
        task_sql = """
        INSERT OR REPLACE INTO tasks
        (uuid, id, text, status, created_time, modified_time, start_time, done_time, duration)
        values ('{}', '{}', '{}', {}, {}, {}, {}, {}, {});
        """.format(
            self.uuid,
            self.id,
            self.text,
            self.status,
            self.created_time,
            self.modified_time,
            self.start_time,
            self.done_time,
            self.duration,
            )
        logger.info("Saving task '{}'.".format(self.uuid))
        db.execute(task_sql)
        remove_tags_sql = """
        DELETE FROM task_tags WHERE task_id = '{}';
        """.format(self.uuid)
        logger.info("Deleting all task tags for '{}'.".format(self.uuid))
        db.execute(remove_tags_sql)
        for tag in self.tags:
            tag_sql = """
            INSERT OR REPLACE INTO task_tags
            (task_id, tag) values ('{}', '{}');
            """.format(self.uuid, tag)
            logger.info("Adding tags '{}' for '{}'.".format(tag, self.uuid))
            db.execute(tag_sql)
        return

    def remove(self):
        del_task_sql = """
        DELETE FROM tasks WHERE uuid = '{}';
        """.format(self.uuid)
        del_tags_sql = """
        DELETE FROM task_tags WHERE task_id = '{}';
        """.format(self.uuid)
        logger.info("Deleting task: {}".format(self.uuid))
        db.execute(del_task_sql)
        logger.info("Deleting tags asociated with task: {}".format(self.uuid))
        db.execute(del_task_sql)

