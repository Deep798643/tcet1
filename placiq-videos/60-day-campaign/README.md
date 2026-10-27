# Placiq 60-day campaign

Vertical 1080x1920 / 30fps / H.264 + AAC shorts. Completed: 42 / 60 (see PRODUCTION_STATE.json).

Resume production:

```
cd placiq-videos/engine
python build.py --campaign 60day --resume
```

Re-render specific days: `python build.py --campaign 60day --days 3,4`  |  Preview contact sheets: add `--preview`.

Narration: Kokoro-82M (local). Music/SFX: procedural (engine/audio2.py). Product visuals: real Placiq demo footage. Nothing is auto-published.
