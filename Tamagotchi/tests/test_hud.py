import os
import time
import pygame
import importlib.util

spec = importlib.util.spec_from_file_location(
    "tamagotchi",
    os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"),
)
_tmodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_tmodule)
tamagotchi = _tmodule


def test_hud_shows_and_expires(tmp_path, monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    tamagotchi.SAVE_FILE = str(tmp_path / "pet_save.json")
    engine = tamagotchi.GameEngine()

    # Trigger feed via hunger stat action and HUD
    engine.pet.hunger = 50.0
    engine.toggle_stat("hunger")
    engine._last_step_time = time.time() - 1.0
    engine.step()
    # Click the explicit 'Feed' action (2nd action)
    btn = None
    for b, act in engine.stat_action_rects["hunger"]:
        if act["label"] == "Feed":
            btn = b
            break
    assert btn is not None
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=btn.center, button=1))
    engine.step()
    assert engine.hud_text == "Feed!"

    # Force expiry and step should clear HUD
    engine.hud_expiry = time.time() - 1.0
    engine.step()
    assert engine.hud_text is None
