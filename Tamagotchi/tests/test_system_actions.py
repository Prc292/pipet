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


def test_shutdown_saves_and_simulates(tmp_path):
    # Use a dedicated save file to ensure pet.save writes there
    old = tamagotchi.SAVE_FILE
    tamagotchi.SAVE_FILE = str(tmp_path / "pet_save.json")
    try:
        eng = tamagotchi.GameEngine()
        _open_menu_and_render(eng)
        # Click the shutdown button to request confirmation
        evt = tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": eng.popup_shutdown.center, "button": 1})
        tamagotchi.pygame.event.post(evt)
        eng.step()
        # Should be pending confirmation now
        assert eng.pending_confirmation is not None and eng.pending_confirmation.get("action") == "shutdown"
        # Render menu to get confirmation rects
        eng.menu_open = True
        eng._last_step_time = time.time() - 1.0
        eng.step()
        yes, no = eng._system_confirmation_rects
        # Click Yes
        tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": yes.center, "button": 1}))
        eng.step()
        assert (tmp_path / "pet_save.json").exists()
        assert getattr(eng, "_last_system_action", {}).get("action") == "shutdown"
        assert getattr(eng, "_last_system_action", {}).get("simulated") is True
    finally:
        tamagotchi.SAVE_FILE = old


def test_restart_saves_and_simulates(tmp_path):
    old = tamagotchi.SAVE_FILE
    tamagotchi.SAVE_FILE = str(tmp_path / "pet_save.json")
    try:
        eng = tamagotchi.GameEngine()
        _open_menu_and_render(eng)
        # Request restart confirmation
        evt = tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": eng.popup_restart.center, "button": 1})
        tamagotchi.pygame.event.post(evt)
        eng.step()
        assert eng.pending_confirmation is not None and eng.pending_confirmation.get("action") == "restart"
        eng.menu_open = True
        eng._last_step_time = time.time() - 1.0
        eng.step()
        yes, no = eng._system_confirmation_rects
        tamagotchi.pygame.event.post(tamagotchi.pygame.event.Event(tamagotchi.pygame.MOUSEBUTTONDOWN, {"pos": yes.center, "button": 1}))
        eng.step()
        assert (tmp_path / "pet_save.json").exists()
        assert getattr(eng, "_last_system_action", {}).get("action") == "restart"
        assert getattr(eng, "_last_system_action", {}).get("simulated") is True
    finally:
        tamagotchi.SAVE_FILE = old
