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


def test_multiple_hunger_actions():
    eng = tamagotchi.GameEngine()
    eng.pet.hunger = 80.0
    _open_panel(eng, "hunger")
    rects = eng.stat_action_rects.get("hunger")
    assert rects and len(rects) == 2
    # Snack (smaller) first action
    btn, a = rects[0]
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn.center, "button": 1}))
    eng.step()
    assert eng.pet.hunger < 80.0
    # Feed (bigger) second action
    btn2, a2 = rects[1]
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn2.center, "button": 1}))
    eng.step()
    assert eng.pet.hunger < 70.0


def test_expensive_operation_requires_confirmation_and_executes():
    eng = tamagotchi.GameEngine()
    eng.pet.health = 30.0
    _open_panel(eng, "health")
    rects = eng.stat_action_rects.get("health")
    # find Operation action
    op = None
    for btn, a in rects:
        if a["label"] == "Operation":
            op = (btn, a)
            break
    assert op is not None
    btn, a = op
    # Click operation -> should set pending_confirmation and not apply immediate effect
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn.center, "button": 1}))
    eng.step()
    assert eng.pending_confirmation is not None
    assert eng.pet.health == 30.0
    # Now click Yes
    yes_rect, no_rect = eng.confirmation_rects.get("health")
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": yes_rect.center, "button": 1}))
    eng.step()
    assert eng.pet.health > 30.0
    assert eng.pending_confirmation is None


def test_confirmation_cancel():
    eng = tamagotchi.GameEngine()
    eng.pet.health = 30.0
    _open_panel(eng, "health")
    rects = eng.stat_action_rects.get("health")
    op = None
    for btn, a in rects:
        if a["label"] == "Operation":
            op = (btn, a)
            break
    assert op is not None
    btn, a = op
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": btn.center, "button": 1}))
    eng.step()
    assert eng.pending_confirmation is not None
    yes_rect, no_rect = eng.confirmation_rects.get("health")
    tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": no_rect.center, "button": 1}))
    eng.step()
    assert eng.pending_confirmation is None
    assert eng.pet.health == 30.0