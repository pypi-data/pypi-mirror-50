from cmdi import CmdResult, command, strip_cmdargs

from . import lib


@command
def freeze(
    sudo: bool = False,
    pip_bin: str = 'pip',
    requirements_file: str = 'requirements.txt',
    options: list = None,
    **cmdargs,
) -> CmdResult:
    return lib.freeze(**strip_cmdargs(locals()))


@command
def install(
    package: str,
    sudo: bool = False,
    pip_bin: str = 'pip',
    options: list = None,
    **cmdargs,
) -> CmdResult:
    return lib.install(**strip_cmdargs(locals()))


@command
def install_requirements(
    sudo: bool = False,
    pip_bin: str = 'pip',
    requirements_file: str = '',
    options: list = None,
    **cmdargs,
) -> CmdResult:
    return lib.install_requirements(**strip_cmdargs(locals()))


@command
def uninstall(
    package: str,
    sudo: bool = False,
    pip_bin: str = 'pip',
    options: list = None,
    **cmdargs,
) -> CmdResult:
    return lib.uninstall(**strip_cmdargs(locals()))
