import os
import time
import importlib.util

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
spec = importlib.util.spec_from_file_location(
    "tamagotchi",
    os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"),
)
_tmodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_tmodule)
tamagotchi = _tmodule


def _step_engine(eng, seconds=0.1):
    eng._last_step_time = time.time() - seconds
    eng.step()


def test_health_shows_persistent_badge():
    eng = tamagotchi.GameEngine()
    eng.pet.health = 10.0
    _step_engine(eng, 1.0)
    assert "health" in getattr(eng, "_last_low_needs", [])


def test_energy_shows_persistent_badge():
    eng = tamagotchi.GameEngine()
    eng.pet.energy = 5.0
    _step_engine(eng, 1.0)
    assert "energy" in getattr(eng, "_last_low_needs", [])


def test_happiness_shows_persistent_badge():
    eng = tamagotchi.GameEngine()
    eng.pet.happiness = 10.0
    _step_engine(eng, 1.0)
    assert "happiness" in getattr(eng, "_last_low_needs", [])
