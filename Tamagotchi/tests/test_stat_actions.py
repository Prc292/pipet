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


def _open_panel(eng, key):
    eng.toggle_stat(key)
    eng._last_step_time = time.time() - 1.0
    eng.step()


def test_hunger_feed_action():
    eng = tamagotchi.GameEngine()
    eng.pet.hunger = 50.0
    _open_panel(eng, "hunger")
    # ensure action rects were built
    rects = eng.stat_action_rects.get("hunger")
    assert rects and len(rects) > 0
    btn, action = rects[0]
    evt = tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn.center, "button": 1})
    tamagotchi.pygame.event.post(evt)
    eng.step()
    assert eng.pet.hunger < 50.0
    assert eng.sounds.last_played == "feed"


def test_happiness_play_action():
    eng = tamagotchi.GameEngine()
    eng.pet.happiness = 40.0
    _open_panel(eng, "happiness")
    rects = eng.stat_action_rects.get("happiness")
    btn, action = rects[0]
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn.center, "button": 1}))
    eng.step()
    assert eng.pet.happiness > 40.0
    assert eng.sounds.last_played == "play"


def test_energy_nap_action():
    eng = tamagotchi.GameEngine()
    eng.pet.energy = 40.0
    _open_panel(eng, "energy")
    rects = eng.stat_action_rects.get("energy")
    btn, action = rects[0]
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn.center, "button": 1}))
    eng.step()
    assert eng.pet.energy > 40.0
    assert eng.sounds.last_played == "nap"


def test_cleanliness_clean_action():
    eng = tamagotchi.GameEngine()
    eng.pet.cleanliness = 30.0
    _open_panel(eng, "cleanliness")
    rects = eng.stat_action_rects.get("cleanliness")
    btn, action = rects[0]
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn.center, "button": 1}))
    eng.step()
    assert eng.pet.cleanliness > 30.0
    assert eng.sounds.last_played == "clean"


def test_health_med_action():
    eng = tamagotchi.GameEngine()
    eng.pet.health = 40.0
    _open_panel(eng, "health")
    rects = eng.stat_action_rects.get("health")
    btn, action = rects[0]
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn.center, "button": 1}))
    eng.step()
    assert eng.pet.health > 40.0
    assert eng.sounds.last_played == "heal"


def test_action_sets_and_expires_cooldown():
    eng = tamagotchi.GameEngine()
    eng.pet.hunger = 50.0
    _open_panel(eng, "hunger")
    rects = eng.stat_action_rects.get("hunger")
    btn, action = rects[0]
    # perform action (Snack) which has a cooldown
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn.center, "button": 1}))
    eng.step()
    # immediately after executing, action should be disabled
    assert not eng.is_action_enabled("hunger", action.get("label"))
    cd = action.get("cooldown", 0.0)
    # advance time past cooldown
    eng._last_step_time = time.time() - (cd + 0.2)
    eng.step()
    assert eng.is_action_enabled("hunger", action.get("label"))


def test_action_blocked_while_cooling():
    eng = tamagotchi.GameEngine()
    eng.pet.hunger = 50.0
    _open_panel(eng, "hunger")
    rects = eng.stat_action_rects.get("hunger")
    btn, action = rects[0]
    # perform action once
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn.center, "button": 1}))
    eng.step()
    v1 = eng.pet.hunger
    last_sound = eng.sounds.last_played
    # try to trigger again immediately
    _open_panel(eng, "hunger")
    rects = eng.stat_action_rects.get("hunger")
    btn2, action2 = rects[0]
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn2.center, "button": 1}))
    eng.step()
    # pet state should be unchanged (allow small decay jitter) and no new sound played
    assert abs(eng.pet.hunger - v1) < 0.01
    assert eng.sounds.last_played == last_sound