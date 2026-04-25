import subprocess
from collections.abc import Callable

from ._util import launcherctl


class Launcher:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def logs(self, _onlogline: Callable[[str], None] | None = None) -> list[str] | None:
        raise NotImplementedError()

    def start(self) -> None:
        _ = launcherctl("start-launcher", self.name)

    def stop(self) -> None:
        _ = launcherctl("stop-launcher", self.name)

    def enable(self, start: bool = False) -> None:
        if start:
            _ = launcherctl("switch-launcher", "--start", self.name)

        else:
            _ = launcherctl("switch-launcher", self.name)

    @property
    def is_current(self) -> bool:
        return (
            subprocess.call(["/opt/bin/launcherctl", "is-current-launcher", self.name])
            == 0
        )

    @property
    def is_enabled(self) -> bool:
        return (
            subprocess.call(["/opt/bin/launcherctl", "is-enabled-launcher", self.name])
            == 0
        )

    @property
    def is_active(self) -> bool:
        return (
            subprocess.call(["/opt/bin/launcherctl", "is-active-launcher", self.name])
            == 0
        )


class API:
    def keys(self) -> list[str]:
        return launcherctl("list-launchers").splitlines()

    def __contains__(self, key: str) -> bool:
        return key in self.keys()

    def __getitem__(self, key: str) -> Launcher:
        if key not in self:
            raise KeyError()

        return Launcher(key)

    @property
    def current(self) -> Launcher:
        return Launcher(launcherctl("status").splitlines()[0][14:-4])

    def switch(self, launcher: Launcher | str, start: bool = False) -> None:
        if not isinstance(launcher, Launcher):
            launcher = Launcher(launcher)

        launcher.enable(start)


api = API()
