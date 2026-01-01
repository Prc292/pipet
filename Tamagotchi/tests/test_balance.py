import time
import importlib.util
import os

spec = importlib.util.spec_from_file_location(
    "tamagotchi",
    os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"),
)
_tmodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_tmodule)
tamagotchi = _tmodule


def test_consistent_care_maintains_care_levels():
    p = tamagotchi.Pet()
    # Simulate repeated small cycles of care
    for _ in range(10):
        p.feed()
        p.play()
        p.clean()
        # simulate 1 minute passing
        p.last_update = time.time() - 60
        p.update()
    avg = (p.health + p.happiness) / 2.0
    assert avg >= 50.0


def test_neglect_decreases_health_over_time():
    p = tamagotchi.Pet()
    # set to very neglected state and simulate time
    p.hunger = 95.0
    p.energy = 10.0
    p.health = 100.0
    p.last_update = time.time() - 2 * 3600  # 2 hours
    p.update()
    assert p.health < 100.0
