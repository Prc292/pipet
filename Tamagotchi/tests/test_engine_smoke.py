import os
import subprocess
import sys
import time
import importlib.util
import json

# Import tamagotchi.py by path
spec = importlib.util.spec_from_file_location(
    "tamagotchi",
    os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"),
)
_tmodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_tmodule)
tamagotchi = _tmodule


def test_pet_feed_and_play():
    p = tamagotchi.Pet()
    p.hunger = 50.0
    p.happiness = 50.0
    p.energy = 50.0

    p.feed()
    assert p.hunger < 50.0

    p.play()
    assert p.happiness > 50.0
    assert p.energy < 50.0


def test_headless_engine_starts(tmp_path):
    env = os.environ.copy()
    env["SDL_VIDEODRIVER"] = "dummy"
    script = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"))
    proc = subprocess.Popen([sys.executable, script], cwd=str(tmp_path), env=env)
    try:
        time.sleep(1.0)
        assert proc.poll() is None
    finally:
        proc.terminate()
        proc.wait(timeout=2)

    save_file = tmp_path / "pet_save.json"
    if save_file.exists():
        with open(save_file, 'r') as f:
            data = json.load(f)
        assert "hunger" in data
        assert "health" in data
