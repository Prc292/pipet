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


def test_hud_expires_after_duration():
    eng = tamagotchi.GameEngine()
    eng.show_hud("Hello", duration=0.5)
    # Simulate expiry by rewinding start time
    eng.hud_start = time.time() - 1.0
    eng.hud_expiry = eng.hud_start + 0.5

    eng.step()
    assert eng.hud_text is None


def test_hud_fades_but_still_present_mid_duration():
    eng = tamagotchi.GameEngine()
    eng.show_hud("Hi", duration=2.0)
    # Simulate half duration elapsed
    eng.hud_start = time.time() - 1.0
    eng.hud_expiry = eng.hud_start + 2.0

    eng.step()
    assert eng.hud_text == "Hi"
