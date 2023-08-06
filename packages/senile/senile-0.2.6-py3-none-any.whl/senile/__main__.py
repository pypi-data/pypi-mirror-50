"""
Main module for senile command-line utility.
"""
from senile import todo as td
from texttable import Texttable
import click
import logging
import senile
import sys

logger = logging.getLogger(__name__)

def stop_all_tasks():
    # made this outside of cli so that it's callable by anyone
    already_started = td.get_tasks_per_status(td.status_desc['active'])
    for t in already_started:
        t.stop()
        t.save()

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
    help="Enable debug mode with output of each action.")
@click.pass_context
def cli(ctx, **kwargs): # pragma: no cover
    logging.basicConfig(
        format = '%(levelname)s: %(message)s',
        filename = None,
        level = logging.DEBUG if ctx.params.get('debug') else logging.WARNING,
        )

@cli.command()
@click.argument('data', nargs=-1)
def add(data): # pragma: no cover
    """Add a new task.\n
    aliases: a\n
    usage: senile add Some text description +tag1 +tag2 +tag3\n
    example: senile add Submit the project +work +project +new
    """
    task = td.Task()
    task.modify(data)
    task.save()

@cli.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('data', nargs=-1)
def modify(data): # pragma: no cover
    """Modify existing task.\n
    aliases: mod, m\n
    usage: senile mod ID_OR_UUID Updated text -TAG_TO_REMOVE +TAG_TO_ADD\n
    example: senile mod 5 Re-submit the finished project -new +old
    """
    task = td.Task.load(data[0])
    if not task:
        logger.warning("Task with identifier '{}' not found.".format(data[0]))
        return
    task.modify(data[1:])
    task.save()

@cli.command()
@click.argument('tasks', nargs=-1)
def remove(tasks): # pragma: no cover
    """Delete following task(s).\n
    aliases: rm\n
    usage: senile rm ID_OR_UUID_1 ID_OR_UUID_2 ID_OR_UUID_3\n
    example: senile rm d59de172 fcf8799e 4 5
    """
    for ident in tasks:
        task = td.Task.load(ident)
        if not task:
            logger.warning("Could not delete task with id '{}'.".format(ident))
            continue
        task.remove()

@cli.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('data', nargs=-1)
def list(data): # pragma: no cover
    """List tasks.\n
    aliases: ls, l\n
    usage: senile l SOME TEXT TO SEARCH +CONTAIN_TAG -DO_NOT_CONTAIN_TAG\n
    example: senile l project +work -old
    """
    print(td.task_table(data))

@cli.command()
@click.argument('task_id', nargs=1)
def info(task_id): # pragma: no cover
    """Show detailed info of a task.\n
    aliases: i, inf, show\n
    usage: senile show TASK_ID_OR_UUID\n
    example: senile show d59de172
    """
    task = td.Task.load(task_id)
    if not task:
        logger.warning("Could not find task with id '{}'.".format(task_id))
        return
    print(task.info())

@cli.command()
@click.argument('tasks', nargs=-1)
def hide(tasks): # pragma: no cover
    """Archive following task(s).\n
    usage: senile hide ID_OR_UUID_1 ID_OR_UUID_2 ID_OR_UUID_3\n
    example: senile hide d59de172 fcf8799e 4 5
    """
    for ident in tasks:
        task = td.Task.load(ident)
        if not task:
            logger.warning("Could not find task with id '{}'.".format(ident))
            continue
        task.hide()
        task.save()

@cli.command()
@click.argument('tasks', nargs=-1)
def done(tasks): # pragma: no cover
    """Set following task(s) to done.\n
    usage: senile done ID_OR_UUID_1 ID_OR_UUID_2 ID_OR_UUID_3\n
    example: senile done d59de172 fcf8799e 4 5
    """
    for ident in tasks:
        task = td.Task.load(ident)
        if not task:
            logger.warning("Could not find task with id '{}'.".format(ident))
            continue
        task.done()
        task.save()

@cli.command()
@click.argument('tasks', nargs=-1)
def todo(tasks): # pragma: no cover
    """Set following task(s) to todo.\n
    usage: senile todo ID_OR_UUID_1 ID_OR_UUID_2 ID_OR_UUID_3\n
    example: senile todo d59de172 fcf8799e 4 5
    """
    for ident in tasks:
        task = td.Task.load(ident)
        if not task:
            logger.warning("Could not find task with id '{}'.".format(ident))
            continue
        task.todo()
        task.save()

@cli.command()
@click.argument('task_id', nargs=1)
def start(task_id): # pragma: no cover
    """Start following task.\n
    usage: senile start TASK_ID_OR_UUID\n
    example: senile start 5\n
    note: Only 1 task can be started.
    """
    task = td.Task.load(task_id)
    if not task:
        logger.warning("Could not find task with id '{}'.".format(task_id))
        return
    stop_all_tasks()
    task.start()
    task.save()

@cli.command()
def stop(): # pragma: no cover
    """Stop tasks.\n
    Called without arguments and stops a single task that was started.
    """
    stop_all_tasks()

@cli.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument('data', nargs=-1)
def archive(data): # pragma: no cover
    """Same as list but show archived tasks.\n
    aliases: ar, arc, arch\n
    usage: senile ar SOME TEXT TO SEARCH +CONTAIN_TAG -DO_NOT_CONTAIN_TAG\n
    example: senile ar project +work -old
    """
    print(td.task_table(data, hidden=True))

@cli.command()
def tags(): # pragma: no cover
    """List all tags and their counts.\n
    aliases: t, tag\n
    Called without arguments. Lists tags of all tasks, even archived.
    """
    for cnt, tag in td.get_tags_count():
        print(cnt, tag)

@cli.command()
def normalize(): # pragma: no cover
    "Delete orphaned tags and fix existing tasks."
    td.normalize()

ALIASES = {
    'a': add,
    'mod': modify,
    'm': modify,
    'rm': remove,
    'del': remove,
    'ls': list,
    'l': list,
    'show': info,
    'inf': info,
    'i': info,
    'ar': archive,
    'arc': archive,
    'arch': archive,
    't': tags,
    'tag': tags,
}

if __name__ == '__main__': # pragma: no cover
    cli()

