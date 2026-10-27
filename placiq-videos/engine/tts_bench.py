import time, soundfile as sf, numpy as np
from kokoro import KPipeline
p = KPipeline(lang_code='a')
for v in ['af_heart','am_michael','am_puck']:
    t=time.time(); txt="Forty-seven tabs. Zero context. And your AI... forgot you. Again!"
    a=np.concatenate([x[2] for x in p(txt, voice=v, speed=1.08)])
    sf.write(f'/workspace/placiq-videos/build/bench_{v}.wav', a, 24000)
    print(v, 'audio', len(a)/24000, 'sec, took', round(time.time()-t,2), 'peak', float(abs(a).max()))
