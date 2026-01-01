__test__ = False
# moved to tests/test_engine_smoke.py
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


__test__ = False
# Moved to `tests/test_engine_smoke.py`

# removed test content; see tests/test_engine_smoke.py
    p.hunger = 50.0
    p.happiness = 50.0
    p.energy = 50.0

    p.feed()
    assert p.hunger < 50.0

    p.play()
    assert p.happiness > 50.0
    assert p.energy < 50.0


def test_headless_engine_starts(tmp_path):
    # Run the script in a temporary directory so it writes its own save file
    env = os.environ.copy()
    # Use SDL dummy driver to avoid opening a real window
    env["SDL_VIDEODRIVER"] = "dummy"
    # Path to the script
    script = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"))
    proc = subprocess.Popen([sys.executable, script], cwd=str(tmp_path), env=env)
    try:
        # Give it a short moment to start
        time.sleep(1.0)
        # Process should still be running (not crashed immediately)
        assert proc.poll() is None
    finally:
        proc.terminate()
        proc.wait(timeout=2)

    # confirm a save file was created; if created, validate JSON format
    save_file = tmp_path / "pet_save.json"
    if save_file.exists():
        with open(save_file, 'r') as f:
            data = json.load(f)
        assert "hunger" in data
        assert "health" in data
