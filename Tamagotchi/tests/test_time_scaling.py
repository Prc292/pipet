import os
import importlib.util
import time

spec = importlib.util.spec_from_file_location(
    "tamagotchi",
    os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"),
)
_tmodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_tmodule)
tamagotchi = _tmodule


def test_catchup_is_capped(tmp_path):
    save_file = tmp_path / "pet_save.json"
    tamagotchi.SAVE_FILE = str(save_file)

    data = {
        "hunger": 10.0,
        "happiness": 90.0,
        "energy": 90.0,
        "health": 100.0,
        "is_alive": True,
        "last_update": time.time() - (48 * 3600)
    }
    with open(tamagotchi.SAVE_FILE, 'w') as f:
        import json
        json.dump(data, f)

    p = tamagotchi.Pet()
    p.load()

    max_increase = 10.0 * (tamagotchi.MAX_CATCHUP_SECONDS / 3600.0)
    assert p.hunger <= 10.0 + max_increase + 1e-6


def test_time_scale_accelerates_decay():
    orig_scale = tamagotchi.TIME_SCALE
    try:
        tamagotchi.TIME_SCALE = 60.0
        p = tamagotchi.Pet()
        p.hunger = 10.0
        p.last_update = time.time() - 60.0
        p.update()
        assert p.hunger >= 19.9
    finally:
        tamagotchi.TIME_SCALE = orig_scale
