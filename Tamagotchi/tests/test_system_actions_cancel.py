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


def _open_menu_and_render(eng):
    eng.menu_open = True
    eng._last_step_time = time.time() - 1.0
    eng.step()


def test_confirm_cancel_prevents_action(tmp_path):
    old = tamagotchi.SAVE_FILE
    tamagotchi.SAVE_FILE = str(tmp_path / "pet_save.json")
    try:
        eng = tamagotchi.GameEngine()
        _open_menu_and_render(eng)
        # Request shutdown confirmation
        evt = tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": eng.popup_shutdown.center, "button": 1})
        tamagotchi.pygame.event.post(evt)
        eng.step()
        assert eng.pending_confirmation is not None
        eng.menu_open = True
        eng._last_step_time = time.time() - 1.0
        eng.step()
        yes, no = eng._system_confirmation_rects
        # Click No
        tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": no.center, "button": 1}))
        eng.step()
        # No save should have been written and action not recorded
        assert not (tmp_path / "pet_save.json").exists()
        assert getattr(eng, "_last_system_action", {}) == {}
    finally:
        tamagotchi.SAVE_FILE = old