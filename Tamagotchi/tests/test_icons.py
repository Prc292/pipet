import os
import importlib.util

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
spec = importlib.util.spec_from_file_location(
    "tamagotchi",
    os.path.join(os.path.dirname(__file__), os.pardir, "tamagotchi.py"),
)
_tmodule = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_tmodule)
tamagotchi = _tmodule


def test_draw_stat_icons_and_render_one_frame():
    eng = tamagotchi.GameEngine()
    # Draw each icon directly and ensure it doesn't crash
    for i, s in enumerate(eng.stat_icons):
        rect = eng.stat_icon_rects[i]
        eng.draw_stat_icon(rect, s["key"], s["color"])
    # Render one frame (should not crash)
    assert eng.step() is True