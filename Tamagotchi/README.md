# Tamagotchi (Pocket Pi-Pet)

A small pygame-based virtual pet demo.

Quickstart

- Install runtime dependency:

```bash
pip install -r requirements.txt
```

- Run the app:

```bash
python3 tamagotchi.py
```

- Run tests (dev deps):

```bash
pip install -r requirements-dev.txt
pytest
```

Notes

- For headless CI runs, set `SDL_VIDEODRIVER=dummy` to allow the app to start without a display.
- To speed up time for testing, set `TAMAGOTCHI_TIME_SCALE` to a value >1.0 (e.g., `60` to make 1 minute = 1 hour).
