import os
import pygame
import importlib.util

spec = importlib.util.spec_from_file_location(
    "tamagotchi",
    os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"),
)
_tmodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_tmodule)
tamagotchi = _tmodule


def test_menu_popup_and_clean_med(tmp_path, monkeypatch):
    # ensure headless
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    # isolate save file
    tamagotchi.SAVE_FILE = str(tmp_path / "pet_save.json")

    engine = tamagotchi.GameEngine()

    # Menu closed initially
    assert not engine.menu_open

    # Click menu button
    evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(engine.btn_menu.x + 2, engine.btn_menu.y + 2), button=1)
    pygame.event.post(evt)
    engine.step()
    assert engine.menu_open

    # Click clean popup (ensure it's not already nearly full so decay doesn't mask the change)
    engine.pet.cleanliness = 40.0
    old_clean = engine.pet.cleanliness
    evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(engine.popup_clean.x + 5, engine.popup_clean.y + 5), button=1)
    pygame.event.post(evt)
    engine.step()
    assert engine.pet.cleanliness > old_clean
    # HUD should show cleaning message
    assert engine.hud_text == "Cleaned!"

    # Click med popup (ensure it will actually heal)
    engine.pet.health = 80.0
    old_health = engine.pet.health
    evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(engine.popup_med.x + 5, engine.popup_med.y + 5), button=1)
    pygame.event.post(evt)
    engine.step()
    assert engine.pet.health > old_health
    assert engine.hud_text == "Healed!"
