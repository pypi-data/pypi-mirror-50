"""
Main module for senile command-line utility.
"""
from senile import todo
from texttable import Texttable
import click
import logging
import senile
import sys

logger = logging.getLogger(__name__)

def add_options(options:list):
    "Aggregate click options from a list and pass as single decorator."
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        try:
            cmd_name = ALIASES[cmd_name].name
        except KeyError:
            pass
        return super().get_command(ctx, cmd_name)

@click.group(cls=AliasedGroup)
@click.version_option(version=senile.__version__,
    message="%(prog)s %(version)s - {}".format(senile.__copyright__))
@click.option('-d', '--debug', is_flag=True,
    help="Enable debug mode with output of each action in the log.")
@click.pass_context
def cli(ctx, **kwargs): # pragma: no cover
    logging.basicConfig(
        format = '%(asctime)s.%(msecs)03d, %(levelname)s: %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        filename = None,
        level = logging.DEBUG if ctx.params.get('debug') else logging.WARNING,
        )

@click.group(invoke_without_command=True)
@click.pass_context
def default(ctx, **kwargs):
    list(ctx)

@cli.command()
def ls(): # pragma: no cover
    "List tasks."
    table = Texttable()
    table.header(['id', 'tags', 'text', 'status'])
    table.set_cols_align(["r", "l", "l", "l"])
    table.set_header_align(["r", "l", "l", "l"])
    table.set_deco(Texttable.HEADER)
    for task in todo.get_tasks():
        table.add_row([
            task.id,
            ','.join(task.tags),
            task,
            task.status,
            ])
    print(table.draw())

@cli.command()
@click.argument('data', nargs=-1)
def add(data): # pragma: no cover
    "Add a new task."
    task = todo.Task()
    task.modify(data)
    task.save()

def get_task(identifier):
    "Get task by id or uuid."
    task = None
    tasks = todo.get_tasks()
    task_identifier = identifier
    if '-' in task_identifier:
        for t in tasks:
            if t.uuid == task_identifier:
                task = t
                break
    else:
        for t in tasks:
            if str(t.id) == task_identifier:
                task = t
                break
    return task

@cli.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('data', nargs=-1)
def mod(data): # pragma: no cover
    "Modify existing task."
    task = get_task(data[0])
    if not task:
        print("Task '{}' not found.".format(task_identifier))
        sys.exit(1)
    task.modify(data[1:])
    task.save()

@cli.command()
@click.argument('tasks', nargs=-1)
def done(tasks): # pragma: no cover
    "Set following task(s) to done."
    for identifier in tasks:
        task = get_task(identifier)
        if not task:
            print("Task '{}' not found.".format(task_identifier))
            continue
        task.done()
        task.save()

@cli.command()
@click.argument('tasks', nargs=-1)
def undone(tasks): # pragma: no cover
    "Set following task(s) to not done."
    for identifier in tasks:
        task = get_task(identifier)
        if not task:
            print("Task '{}' not found.".format(task_identifier))
            continue
        task.undone()
        task.save()

@cli.command()
@click.argument('tasks', nargs=-1)
def rm(tasks): # pragma: no cover
    "Delete following task(s)."
    for identifier in tasks:
        task = get_task(identifier)
        if not task:
            print("Task '{}' not found.".format(task_identifier))
            continue
        task.remove()

ALIASES = {
    'remove': rm,
    'del': rm,
    'modify': mod,
    'list': ls,
    'l': ls,
    'a': add,
    'm': mod,
}

if __name__ == '__main__': # pragma: no cover
    cli()

