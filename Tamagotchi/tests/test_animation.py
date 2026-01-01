import os
import time
import importlib.util

# Ensure headless rendering for tests
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

spec = importlib.util.spec_from_file_location(
    "tamagotchi",
    os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"),
)
_tmodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_tmodule)
tamagotchi = _tmodule


def test_stat_toggle_animates():
    eng = tamagotchi.GameEngine()
    # pick first stat icon center
    pos = eng.stat_icon_rects[0].center
    # Use the helper to toggle the stat open (more reliable in tests than posting events)
    key = eng.stat_icons[0]["key"]
    eng.toggle_stat(key)

    # Simulate 1 second elapsed so animation reaches target
    eng._last_step_time = time.time() - 1.0
    eng.step()  # apply a simulated 1s of animation time

    assert eng.stat_anim[eng.stat_icons[0]["key"]]["value"] > 0.9
    assert eng.stat_expanded[eng.stat_icons[0]["key"]] is True


def test_stat_toggle_collapses():
    eng = tamagotchi.GameEngine()
    key = eng.stat_icons[0]["key"]
    # open first
    eng.toggle_stat(key)
    eng._last_step_time = time.time() - 1.0
    eng.step()  # apply simulated 1s of animation time

    # Now toggle again to collapse
    eng.toggle_stat(key)
    # ensure the target was set to collapse
    assert eng.stat_anim[key]["target"] == 0.0
    eng._last_step_time = time.time() - 1.0
    eng.step()  # apply simulated 1s of animation time

    assert eng.stat_anim[eng.stat_icons[0]["key"]]["value"] < 0.1
    assert eng.stat_expanded[eng.stat_icons[0]["key"]] is False
