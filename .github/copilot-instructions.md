# Purpose: guidance for AI coding agents working on this project

## Big Picture Architecture
- Single-file, event-loop-driven design (`tamagotchi.py`) for simplicity and portability.
- `Pet` manages game state, persistence, and stat decay; `GameEngine` handles UI, event loop, and platform-specific logic.
- All logic and UI changes should be accompanied by focused tests (see `tests/` and `Tamagotchi/tests/`).

# Copilot / AI Agent Instructions

Quick start
- Entrypoint: `tamagotchi.py` (single-file app). Key classes: `Pet` (game state & persistence) and `GameEngine` (UI & event loop).
- Run locally: `python3 tamagotchi.py` (or `python3 -m pdb tamagotchi.py` for debugging).
- Install deps: `pip install -r requirements.txt` and dev deps `pip install -r requirements-dev.txt` for tests.

## Important constants & env vars
- `SAVE_FILE` (default: `pet_save.json`): file written/read by `Pet.save()`/`Pet.load()`.
- `TIME_SCALE` / env `TAMAGOTCHI_TIME_SCALE`: multiplies elapsed seconds (useful to accelerate time in tests/debugging).
- `MAX_CATCHUP_SECONDS`: cap for how much elapsed time `load()` will apply to avoid large sudden decays.
- `SDL_VIDEODRIVER`: set to `dummy` in CI/headless runs (tests set it to `dummy`); Linux code sets `kmsdrm` for fullscreen by default.

## Persistence & safety patterns
- Saves use an *atomic replace* pattern: write to `SAVE_FILE + ".tmp"` then `os.replace()` to avoid truncated files.
- Save JSON keys: `hunger`, `happiness`, `energy`, `health`, `is_alive`, `last_update`.
- `Pet.load()` is defensive: it validates numeric keys (via local `get_num()`), falls back to defaults, and calls `self.update()` to apply catch-up (bounded by `MAX_CATCHUP_SECONDS`).

## Architecture & code style
- Single-file, procedural style. Keep logic (decay, state transitions, persistence) in `Pet` and UI/OS-specific code in `GameEngine`.
- Prefer small, localized edits over large refactors.

## How to add a new persistent stat (explicit)
1. Add attribute in `Pet.__init__` with a sensible default.
2. Include it in `Pet.save()` JSON payload.
3. Restore it in `Pet.load()` (validate/fallback to default).
4. Call `self.update()` in `load()` (already done) so catch-up applies.
5. Add a `draw_bar()` (or equivalent) in `GameEngine.run()` to show it.

## Testing & CI notes (concrete examples)
- Tests live under `tests/` (and a duplicate under `Tamagotchi/tests/` in this workspace).
- Tests import the module by filepath (see tests using `importlib.util.spec_from_file_location`), so avoid relying on PYTHONPATH changes.
- Run tests: `pip install -r requirements-dev.txt && pytest`.
- Headless smoke tests use `SDL_VIDEODRIVER=dummy` and may spawn the script in a subprocess; see `tests/test_engine_smoke.py` for example.
- Use `TAMAGOTCHI_TIME_SCALE` to speed time-related tests (see `tests/test_time_scaling.py`).

## Common bug hotspots & checks
- Save/load mismatch: ensure keys written in `save()` match what `load()` expects (and validate types).
- Catch-up math: `update()` multiplies elapsed by `TIME_SCALE` and applies `MAX_CATCHUP_SECONDS` cap—tests cover both behaviors.
- Platform window flags: Linux path sets `SDL_VIDEODRIVER=kmsdrm` and `pygame.FULLSCREEN`; macOS uses `pygame.SCALED|pygame.RESIZABLE`.

## Key files & directories
- `tamagotchi.py` — read `Pet` and `GameEngine` implementations first.
- `tests/test_pet.py`, `tests/test_engine_smoke.py`, `tests/test_time_scaling.py` — show how functionality and edge cases are validated.

If you edit behavior: add/adjust unit tests that reproduce the intended behavior (tests are small and focused). Ask for clarification if you need broader refactor permission.

## UI polish & assets
- For small UI polish (animated stat expand/collapse, HUD fade-ins/outs, icons vs letters), prefer incremental changes plus tests that drive time forward (manipulate `engine._last_step_time` or `time.time()` in tests to simulate elapsed time).
- Use `GameEngine` helpers (`toggle_stat`, `show_hud`) in tests to avoid flaky event-driven interaction where possible.
- Sound should be handled via a `SoundManager` abstraction that is a safe no-op in headless CI; tests should assert `last_played` or that `play_effect` does not raise.

## CI & PR guidance
- We include a GitHub Actions workflow (`.github/workflows/ci.yml`) that runs headless tests by setting `SDL_VIDEODRIVER=dummy` and running `pytest Tamagotchi/tests`.
- Use the provided PR template and add tests for UI and backend changes.

## Integration points & external dependencies
- Systemd service for Pi: see `systemd/tamagotchi.service`.
- Pi setup: see `pi_setup.sh`, `scripts/pi_install_deps.sh`, and `PI_OS_SETUP.md`.
- Sound handled via `SoundManager` abstraction (safe for headless/CI).
- External dependencies managed via `requirements.txt` and `requirements-dev.txt`.

---
If anything here is unclear or you'd like additional examples (CI config, packaging, contributor workflow, or integration details), ask for clarification or specify which section to expand.

