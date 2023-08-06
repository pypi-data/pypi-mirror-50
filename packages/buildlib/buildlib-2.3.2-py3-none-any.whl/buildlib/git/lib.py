from typing import Optional, Union
import subprocess as sp


def add_all() -> None:
    sp.run(['git', 'add', '--all'], check=True)


def log(
    revision_range: str = '-5',
    reverse: bool = False,
    no_pager: bool = True,
):

    cmd = ['git']

    if no_pager:
        cmd.append('--no-pager')

    cmd.extend(['log', revision_range])

    if reverse:
        cmd.append('--reverse')

    sp.run(cmd, check=True)


def commit(msg: str = "") -> None:

    cmd = ['git', 'commit']

    if msg != '':
        cmd.extend(['-m', msg])

    sp.run(cmd, check=True)


def tag(
    version: str,
    branch: str,
) -> None:
    sp.run(['git', 'tag', version, branch], check=True)


def push(branch: str) -> None:
    sp.run(['git', 'push', 'origin', branch, '--tags'], check=True)


def get_default_branch() -> Union[str, None]:

    branch: Union[str, None] = None

    cp1 = sp.run(['git', 'show-branch', '--list'], stdout=sp.PIPE)

    if cp1.stdout.find(b'No revs') == -1 and cp1.returncode == 0:
        cp2 = sp.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=sp.PIPE
        )

        branch = cp2.stdout.replace(b'\n', b'')

    return branch


def status() -> None:
    sp.run(['git status'], shell=True)


def diff() -> None:
    sp.run(['git', 'diff'], check=True)
