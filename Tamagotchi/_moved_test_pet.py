__test__ = False
# moved to tests/test_pet.py
import os
import tempfile
import time
import importlib.util

# Load tamagotchi module by path so tests work regardless of PYTHONPATH
spec = importlib.util.spec_from_file_location(
    "tamagotchi",
    os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"),
)
_tmodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_tmodule)
# expose as tamagotchi
tamagotchi = _tmodule


__test__ = False
# Moved to `tests/test_pet.py`

    # Use a temp save file
    save_path = tmp_path / "pet_save.json"
    tamagotchi.SAVE_FILE = str(save_path)

    pet = tamagotchi.Pet()
    pet.hunger = 10.5
    pet.happiness = 88.3
    pet.energy = 75.0
    pet.health = 66.6
    pet.is_alive = True
    # Save, then create a fresh Pet and load
    pet.save()

    p2 = tamagotchi.Pet()
    p2.load()

    # Allow for tiny differences due to immediate update() call
    assert abs(p2.hunger - pet.hunger) < 1.0
    assert abs(p2.happiness - pet.happiness) < 1.0
    assert abs(p2.energy - pet.energy) < 1.0
    assert abs(p2.health - pet.health) < 1.0
    assert p2.is_alive == pet.is_alive


def test_load_corrupt_json(tmp_path, capsys):
    save_path = tmp_path / "pet_save.json"
    tamagotchi.SAVE_FILE = str(save_path)

    # Write invalid JSON
    with open(tamagotchi.SAVE_FILE, 'w') as f:
        f.write('{ this is not valid json')

    p = tamagotchi.Pet()
    p.load()

    captured = capsys.readouterr()
    assert "failed to read save file" in captured.out
    # Defaults should be applied
    assert 0.0 <= p.hunger <= 100.0
    assert 0.0 <= p.happiness <= 100.0
    assert 0.0 <= p.energy <= 100.0
    assert 0.0 <= p.health <= 100.0


def test_load_missing_keys(tmp_path):
    save_path = tmp_path / "pet_save.json"
    tamagotchi.SAVE_FILE = str(save_path)

    # Write JSON with missing keys
    with open(tamagotchi.SAVE_FILE, 'w') as f:
        json.dump({"hunger": 1.2}, f)

    p = tamagotchi.Pet()
    p.load()

    # hunger should be from file (allow tiny delta due to immediate update), others default
    assert abs(p.hunger - 1.2) < 1e-3
    assert 0.0 <= p.happiness <= 100.0
    assert 0.0 <= p.energy <= 100.0
    assert 0.0 <= p.health <= 100.0
