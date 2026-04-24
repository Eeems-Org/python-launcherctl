import subprocess


class LauncherCtlException(Exception):
    pass


def launcherctl(*args: str) -> str:
    try:
        return subprocess.check_output(["/opt/bin/launcherctl", *args], text=True)

    except subprocess.CalledProcessError as e:
        raise LauncherCtlException(f"{e.stdout}\n{e.stderr}") from e  # pyright: ignore[reportAny]
