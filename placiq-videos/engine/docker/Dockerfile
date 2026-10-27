# Placiq render image: FFmpeg + Kokoro-82M (CPU) + NumPy/SciPy/PIL. Local, open-source only.
FROM python:3.11-slim-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg espeak-ng fonts-dejavu-core git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir "kokoro>=0.9.4" soundfile numpy scipy pillow
# pre-fetch the Kokoro weights + English voices so renders work offline
RUN python -c "from kokoro import KPipeline; p=KPipeline(lang_code='a'); [list(p('Placiq.', voice=v)) for v in ['af_heart','am_michael','am_puck','af_bella','bf_emma','am_fenrir','af_nicole','bm_george']]"
WORKDIR /workspace/placiq-videos
