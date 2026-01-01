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


def test_hunger_notification_and_reaction():
    eng = tamagotchi.GameEngine()
    eng.pet.hunger = 95.0
    # one step should trigger notification and start reaction
    _step_engine(eng, 1.0)
    assert eng.hud_text is not None
    assert "hungry" in eng.hud_text.lower()
    assert eng.pet_reaction is not None
    assert eng.pet_reaction["type"] == "hunger"
    # reaction should progress and then clear after duration
    total = eng.pet_reaction["duration"] + 0.1
    _step_engine(eng, total)
    # after sufficient time, reaction cleared
    assert eng.pet_reaction is None


def test_cleanliness_notification_and_reaction():
    eng = tamagotchi.GameEngine()
    eng.pet.cleanliness = 10.0
    _step_engine(eng, 1.0)
    assert eng.hud_text is not None
    assert "bath" in eng.hud_text.lower()
    assert eng.pet_reaction is not None
    assert eng.pet_reaction["type"] == "cleanliness"
    # reaction cleared after duration
    total = eng.pet_reaction["duration"] + 0.1
    _step_engine(eng, total)
    assert eng.pet_reaction is None


def test_notification_cooldown_prevents_spam():
    eng = tamagotchi.GameEngine()
    eng.pet.hunger = 95.0
    _step_engine(eng, 1.0)
    first_expiry = eng.needs_notified.get("hunger")
    assert first_expiry is not None
    # step again immediately - no new hud_text
    prev = eng.hud_text
    _step_engine(eng, 0.2)
    assert eng.hud_text == prev
    # advance past cooldown and trigger again
    eng._last_step_time = time.time() - (tamagotchi.NOTIFY_COOLDOWN + 0.2)
    eng.step()
    assert eng.hud_text is not None
    # expiry should be refreshed (>= is acceptable given timing granularity)
    assert eng.needs_notified.get("hunger") >= first_expiry