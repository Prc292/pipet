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


def _step(eng, seconds=0.05):
    eng._last_step_time = time.time() - seconds
    eng.step()


def test_blinking_occurs():
    eng = tamagotchi.GameEngine()
    # force a blink next step
    eng.blink_timer = 0.0
    _step(eng, 0.02)
    # blinking should have started or just occurred
    assert eng.is_blinking() or eng._last_drawn_pet.get("eyes_open") is False


def test_belly_squish_on_hunger():
    eng = tamagotchi.GameEngine()
    eng.pet.hunger = 95.0
    _step(eng, 0.1)
    # reaction should set belly squish > 0 and draw should reflect it
    assert eng.get_belly_squish() > 0.0
    assert eng._last_drawn_pet.get("belly_squish", 0.0) > 0.0


def test_idle_bob_changes_over_time():
    eng = tamagotchi.GameEngine()
    initial = eng.idle_bob_offset
    _step(eng, 0.5)
    assert eng.idle_bob_offset != initial