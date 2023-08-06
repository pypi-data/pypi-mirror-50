
import json
import logging
import os
import uuid

data_file = os.path.expanduser('~/.senile')
logger = logging.getLogger(__name__)

def get_tasks():
    logger.info("Loading all tasks.")
    all_tasks = []
    all_ids = set()
    try:
        with open(data_file, 'r') as fd:
            for line in fd.readlines():
                if line.strip() == "":
                    continue
                task = Task()
                task.loads(line)
                if task.id <= 0 or task.id in all_ids:
                    x = 1
                    while x in all_ids:
                        x+=1
                    task.id = x
                all_ids.add(task.id)
                all_tasks.append(task)
    except FileNotFoundError:
        logger.warning('File "{}" not created yet. Add your first task.'.format(data_file))
    all_tasks.sort(key=lambda x: x.status)
    return all_tasks

def save_tasks(tasks):
    if not os.path.isdir(os.path.dirname(data_file)):
        logger.info("Creating data directory.")
        os.makedirs(os.path.dirname(data_file))
    with open(data_file, "w") as fd:
        logger.info("Saving all tasks.")
        for task in tasks:
            fd.write(task.dumps() + '\n')
        logger.info("All tasks saved.")


class Task(object):
    "TODO entry."

    def __init__(self):
        self.uuid = str(uuid.uuid1())
        self.id = 0
        self.text = ''
        self.tags = set()
        self.status = ''

    def __eq__(self, other):
        return self.uuid == other.uuid

    def modify(self, options):
        "Parses and populates data."

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

    def done(self):
        self.status = 'done'

    def undone(self):
        self.status = ''

    def __str__(self):
        return self.text

    def dumps(self):
        return json.dumps({
            'uuid':self.uuid,
            'id':self.id,
            'text':self.text,
            'tags':list(self.tags),
            'status':self.status,
            }
            )

    def loads(self, json_data):
        logger.info("Loading task from json.")
        for option, value in json.loads(json_data).items():
            if option == 'uuid':
                self.uuid = value
            elif option == 'id':
                self.id = value
            elif option == 'text':
                self.text = value
            elif option == 'tags':
                self.tags = set(value)
            elif option == 'status':
                self.status = value
            else:
                logger.warning("Unknown option '{}' in task.".format(option))

    def save(self):
        logger.info("Saving task: {}".format(self.uuid))
        tasks = get_tasks()
        tasks = list(filter((self).__ne__, tasks))
        tasks.append(self)
        save_tasks(tasks)

    def remove(self):
        logger.info("Deleting task: {}".format(self.uuid))
        tasks = get_tasks()
        tasks = list(filter((self).__ne__, tasks))
        save_tasks(tasks)

