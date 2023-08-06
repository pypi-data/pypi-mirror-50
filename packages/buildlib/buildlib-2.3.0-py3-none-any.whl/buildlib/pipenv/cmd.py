from cmdi import CmdResult, command, strip_cmdargs

from . import lib


@command
def install(
    dev: bool = False,
    **cmdargs,
) -> CmdResult:
    return lib.install(**strip_cmdargs(locals()))


@command
def create_env(
    version: str,
    **cmdargs,
) -> CmdResult:
    return lib.create_env(**strip_cmdargs(locals()))
