from ._util import launcherctl


class App:
    def __init__(self, name: str) -> None:
        self.name: str = name

    @property
    def is_running(self) -> bool:
        return self.name in api.running.keys()

    @property
    def is_paused(self) -> bool:
        return self.name in api.paused.keys()

    def start(self) -> None:
        _ = launcherctl("start-app", self.name)

    def stop(self) -> None:
        _ = launcherctl("stop-app", self.name)

    def pause(self) -> None:
        _ = launcherctl("pause-app", self.name)

    def resume(self) -> None:
        _ = launcherctl("resume-app", self.name)


class API:
    def keys(self) -> list[str]:
        return [x for x in launcherctl("list-apps").splitlines()]

    def __contains__(self, key: str) -> bool:
        return key in self.keys()

    def __getitem__(self, key: str) -> App:
        if key not in self:
            raise KeyError()

        return App(key)

    @property
    def running(self) -> dict[str, App]:
        return {
            x: App(x)
            for x in [x for x in launcherctl("list-running-apps").splitlines()]
        }

    @property
    def paused(self) -> dict[str, App]:
        return {
            x: App(x) for x in [x for x in launcherctl("list-paused-apps").splitlines()]
        }


api = API()
