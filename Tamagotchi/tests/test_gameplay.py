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


def test_play_requires_energy():
    p = tamagotchi.Pet()
    p.energy = 10.0
    p.happiness = 50.0
    p.play()
    # energy == 10 should NOT allow play()
    assert p.happiness == 50.0
    assert p.energy == 10.0


def test_feed_on_dead_no_change():
    p = tamagotchi.Pet()
    p.is_alive = False
    p.hunger = 80.0
    p.health = 50.0
    p.energy = 40.0
    p.feed()
    # feeding a dead pet should do nothing
    assert p.hunger == 80.0
    assert p.health == 50.0
    assert p.energy == 40.0


def test_feed_health_capped():
    p = tamagotchi.Pet()
    p.health = 99.5
    p.is_alive = True
    p.feed()
    assert p.health <= 100.0


def test_feed_increases_energy():
    p = tamagotchi.Pet()
    p.energy = 50.0
    p.is_alive = True
    p.feed()
    assert p.energy > 50.0
    assert p.energy <= 100.0


def test_hunger_threshold_health_decay():
    p = tamagotchi.Pet()
    p.hunger = 81.0
    p.health = 100.0
    p.last_update = time.time() - 3600.0  # 1 hour ago
    p.update()
    # health should have decreased by ~5.0 for 1 hour at the decay rate
    assert p.health < 100.0
    assert p.health <= 100.0 - (5.0 * (1.0)) + 1e-6


def test_happiness_decays_over_time():
    p = tamagotchi.Pet()
    p.happiness = 100.0
    p.last_update = time.time() - 3600.0
    p.update()
    assert p.happiness < 100.0
    assert p.happiness <= 100.0 - (8.0 * (1.0)) + 1e-6


def test_state_transitions():
    p = tamagotchi.Pet()
    p.health = 39.0
    p.update()
    assert p.state == "SICK"

    p = tamagotchi.Pet()
    p.hunger = 91.0
    p.update()
    assert p.state == "SICK"

    p = tamagotchi.Pet()
    p.happiness = 30.0
    p.update()
    assert p.state == "SAD"
