import json
from typing import Optional
from cmdi import CmdResult, command, strip_cmdargs

from . import lib


@command
def bump_version(
    new_version: str,
    filepath: str = 'package.json',
    **cmdargs,
) -> CmdResult:
    return lib.bump_version(**strip_cmdargs(locals()))


@command
def publish(**cmdargs) -> CmdResult:
    return lib.publish()
