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


def test_clean_increases_cleanliness_and_affects_energy_happiness():
    p = tamagotchi.Pet()
    p.cleanliness = 40.0
    p.energy = 50.0
    p.happiness = 40.0
    p.clean()
    assert p.cleanliness > 40.0
    assert p.happiness > 40.0
    assert p.energy < 50.0


def test_clean_dead_no_change():
    p = tamagotchi.Pet()
    p.is_alive = False
    p.cleanliness = 10.0
    p.energy = 30.0
    p.happiness = 20.0
    p.clean()
    assert p.cleanliness == 10.0
    assert p.energy == 30.0
    assert p.happiness == 20.0


def test_cleanliness_low_causes_health_penalty():
    p = tamagotchi.Pet()
    # isolate cleanliness effect: ensure hunger and energy are fine
    p.hunger = 10.0
    p.energy = 100.0
    p.cleanliness = 10.0
    p.health = 100.0
    p.last_update = time.time() - 3600.0  # 1 hour ago
    p.update()
    # Health should decrease due to low cleanliness (approx 2.5 units/hour)
    assert p.health < 100.0
    assert p.health <= 100.0 - (2.5 * 1.0) + 1e-6
