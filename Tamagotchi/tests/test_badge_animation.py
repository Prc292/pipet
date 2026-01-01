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


def _step_engine(eng, seconds=0.05):
    eng._last_step_time = time.time() - seconds
    eng.step()


def test_badge_pulses_over_time():
    eng = tamagotchi.GameEngine()
    eng.pet.hunger = 95.0
    # Step to initialize the badge and pulse phase
    _step_engine(eng, 0.05)
    p1 = eng.get_badge_pulse("hunger")
    assert p1 >= 0.0 and p1 <= 1.0
    # Advance a little and ensure pulse changed
    _step_engine(eng, 0.1)
    p2 = eng.get_badge_pulse("hunger")
    assert abs(p2 - p1) > 1e-3


def test_badge_zero_when_not_low():
    eng = tamagotchi.GameEngine()
    eng.pet.hunger = 10.0
    _step_engine(eng, 0.05)
    assert eng.get_badge_pulse("hunger") == 0.0
