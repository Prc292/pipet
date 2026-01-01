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


def test_medicine_heals_and_reduces_happiness():
    p = tamagotchi.Pet()
    p.health = 50.0
    p.happiness = 80.0
    p.give_medicine()
    assert p.health > 50.0
    assert p.happiness < 80.0


def test_medicine_caps_health():
    p = tamagotchi.Pet()
    p.health = 95.0
    p.give_medicine()
    assert p.health == 100.0


def test_medicine_dead_no_effect():
    p = tamagotchi.Pet()
    p.is_alive = False
    p.health = 10.0
    p.happiness = 20.0
    p.give_medicine()
    assert p.health == 10.0
    assert p.happiness == 20.0


def test_evolution_requires_care():
    p = tamagotchi.Pet()
    # make pet old enough to be YOUNG candidate
    p.birth_time = time.time() - (tamagotchi.STAGE_YOUNG_SECONDS + 1)
    p.health = 100.0
    p.happiness = 100.0
    p.update()
    assert p.life_stage == "YOUNG"

    # If care is poor, it should not evolve
    p2 = tamagotchi.Pet()
    p2.birth_time = time.time() - (tamagotchi.STAGE_YOUNG_SECONDS + 1)
    p2.health = 10.0
    p2.happiness = 10.0
    p2.update()
    assert p2.life_stage == "BABY"
