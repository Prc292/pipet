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


def test_stat_icon_toggle(tmp_path, monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    tamagotchi.SAVE_FILE = str(tmp_path / "pet_save.json")
    engine = tamagotchi.GameEngine()

    # Initially none expanded
    assert not any(engine.stat_expanded.values())

    # Click health icon
    rect = engine.stat_icon_rects[0]
    evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(rect.x + 2, rect.y + 2), button=1)
    pygame.event.post(evt)
    engine.step()
    assert engine.stat_expanded['health']

    # Click energy icon and ensure only that is expanded
    rect2 = engine.stat_icon_rects[3]
    evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(rect2.x + 2, rect2.y + 2), button=1)
    pygame.event.post(evt)
    engine.step()
    assert not engine.stat_expanded['health']
    assert engine.stat_expanded['energy']

    # Tap the same icon to collapse
    evt = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(rect2.x + 2, rect2.y + 2), button=1)
    pygame.event.post(evt)
    engine.step()
    assert not engine.stat_expanded['energy']
