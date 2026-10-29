# Placiq - Your work, connected (Launch film, cut A)

Editable source. `timeline.json` holds every shot (start, duration, layout, clip, headline), every narration line with word-level timings, and every SFX event.

Re-render (from repo root):

```
docker build --network host -t placiq-render placiq-videos/engine/docker
docker run --rm -v $PWD:/workspace -w /workspace/placiq-videos/engine placiq-render python launch.py A
```

Edit `SHOTS` in `launch.py` to change copy, layouts, clip choices or callouts; durations re-quantise to the beat automatically.
