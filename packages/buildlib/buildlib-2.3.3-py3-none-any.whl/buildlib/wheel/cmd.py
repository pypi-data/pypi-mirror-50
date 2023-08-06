from typing import Optional
from cmdi import CmdResult, command, strip_cmdargs

from . import lib


@command
def push(
    wheel: str = 'dist/*',
    repository: str = 'pypi',
    **cmdargs,
) -> CmdResult:
    return lib.push(**strip_cmdargs(locals()))


@command
def build(
    cleanup: bool = False,
    **cmdargs,
) -> CmdResult:
    return lib.build(**strip_cmdargs(locals()))
