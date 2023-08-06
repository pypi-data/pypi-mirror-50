import subprocess as sp
import prmt
from headlines import h3

from . import lib as git
from . import cmd as git_cmd


def commit_msg(
    fmt=None,
    open_editor: bool = True,
) -> str:

    if open_editor:
        r = sp.run(['git', 'commit', '--dry-run'], stdout=sp.PIPE)
        instrucution = b"Lines starting with '#' will be ignored.\n\n" + r.stdout

        return prmt.string_from_editor(
            question='Commit Message',
            instruction=instrucution.decode("utf8"),
            file_type='gitcommit',
        )
    else:
        return prmt.string(
            question=r.stdout,
            fmt=fmt,
            blacklist=[''],
        )


def branch(
    default=None,
    fmt=None,
) -> str:

    default = git_cmd.get_default_branch().val

    return prmt.string(
        question='Enter BRANCH name:',
        default=default,
        fmt=fmt,
    )


def confirm_status(
    default: str = 'y',
    fmt=None,
) -> bool:

    print(h3('Git Status'))
    git_cmd.status()

    return prmt.confirm(
        question='GIT STATUS ok?',
        default=default,
        fmt=fmt,
    )


def confirm_diff(
    default: str = 'y',
    fmt=None,
) -> bool:

    print(h3('Git Diff'))
    git_cmd.diff()

    return prmt.confirm(
        question='GIT DIFF ok?',
        default=default,
        fmt=fmt,
    )


def should_run_git(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run ANY GIT COMMANDS?',
        default=default,
        fmt=fmt,
    )


def should_add_all(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run GIT ADD ALL ("git add --all")?',
        default=default,
        fmt=fmt,
    )


def should_commit(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run GIT COMMIT?',
        default=default,
        fmt=fmt,
    )


def should_tag(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='Run GIT TAG?',
        default=default,
        fmt=fmt,
    )


def should_push(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prmt.confirm(
        question='GIT PUSH to GITHUB?',
        default=default,
        fmt=fmt,
    )
