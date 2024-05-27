import launcherctl

print(launcherctl.launchers.current.name)
print([x for x in launcherctl.launchers.keys()])
if "oxide" in launcherctl.launchers:
    print("oxide:")
    oxide = launcherctl.launchers["oxide"]
    print(f"  current: {oxide.is_current}")
    print(f"  enabled: {oxide.is_enabled}")
    print(f"  active: {oxide.is_active}")

if "xochitl" in launcherctl.launchers:
    print("xochitl:")
    xochitl = launcherctl.launchers["xochitl"]
    print(f"  current: {xochitl.is_current}")
    print(f"  enabled: {xochitl.is_enabled}")
    print(f"  active: {xochitl.is_active}")

launcherctl.launchers["xochitl"].is_current
print([x for x in launcherctl.apps.keys()])
print([x for x in launcherctl.apps.running.keys()])
print([x for x in launcherctl.apps.paused.keys()])
if "calculator" in launcherctl.apps:
    calculator = launcherctl.apps["calculator"]
    print("calculator:")
    print(f"  running: {calculator.is_running}")
    print(f"  paused: {calculator.is_paused}")

if "xochitl" in launcherctl.apps:
    xochitl = launcherctl.apps["xochitl"]
    print("xochitl:")
    print(f"  running: {xochitl.is_running}")
    print(f"  paused: {xochitl.is_paused}")
