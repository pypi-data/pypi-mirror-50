from cmdi import CmdResult, command, strip_cmdargs

from . import lib


@command
def bump_version(
    semver_num: str = None,
    config_file: str = 'Project',
    **cmdargs,
) -> CmdResult:
    return lib.bump_version(**strip_cmdargs(locals()))
