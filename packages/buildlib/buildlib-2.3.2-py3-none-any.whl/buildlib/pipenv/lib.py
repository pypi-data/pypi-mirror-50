from cmdi import CmdResult, command, strip_cmdargs
import subprocess as sp


def install(dev: bool = False) -> None:
    """
    Install packages from Pipfile.
    """
    dev_flag = ['--dev'] if dev else []

    sp.run(['pipenv', 'install'] + dev_flag, check=True)


def create_env(version: str) -> None:
    """
    Create a fresh python environment.
    @version: E.g.: '3.6'
    """
    sp.run(['pipenv', f'--python {version}'], check=True)
