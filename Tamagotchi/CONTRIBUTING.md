Contributing
============

Thanks for wanting to contribute! A few guidelines to keep changes small, testable, and review-friendly:

- Run the test suite: `pytest Tamagotchi/tests`
- For UI tests and headless runs, set `SDL_VIDEODRIVER=dummy` (CI should do this for you).
- Add tests for any behavioral changes (pet logic, persistence, UI interactions).
- Keep changes small and focused (one behavior or fix per PR).
- When touching persistence, follow the atomic-replace pattern (`save()` writes to `SAVE_FILE + '.tmp'` then `os.replace()`).
- If your change affects game balance, add a small test that asserts the intended numeric effect to avoid regressions.

If you're unsure about the scope of a change, open an issue first so we can discuss the design.