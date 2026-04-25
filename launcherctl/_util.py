import subprocess


class LauncherCtlException(Exception):
    pass


def launcherctl(*args: str) -> str:
    proc = subprocess.run(
        ["/opt/bin/launcherctl", *args], text=True, check=False, capture_output=True
    )
    if not proc.returncode:
        return proc.stdout

    raise LauncherCtlException(f"{proc.stdout}\n{proc.stderr}")
