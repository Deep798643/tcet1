"""End-to-end producer: Kokoro TTS -> beat-quantized timeline -> procedural score + SFX -> frames -> FFmpeg masters."""
import json, math, os, subprocess, sys, time, re
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
if '--campaign' in sys.argv:
    os.environ['PLACIQ_FMT'] = 'v'
from core import *
import scenes as SC
import audio as A
from videos import VIDEOS

OUT = os.path.join(ROOT, 'original-films')
BUILD = os.path.join(ROOT, 'build')
_pipes = {}


def kokoro():
    if 'k' not in _pipes:
        from kokoro import KPipeline
        _pipes['k'] = KPipeline(lang_code='a')
    return _pipes['k']


def tts(text, voice, speed, path):
    if os.path.exists(path + '.json'):
        a, _ = sf.read(path + '.wav'); return a, json.load(open(path + '.json'))
    pipe = kokoro()
    chunks, words, off = [], [], 0.0
    for r in pipe(text, voice=voice, speed=speed):
        au = r.audio.numpy() if hasattr(r.audio, 'numpy') else np.asarray(r.audio)
        for tk in (r.tokens or []):
            if tk.start_ts is not None and re.search(r'\w', tk.text):
                words.append([tk.text, off + tk.start_ts, off + (tk.end_ts or tk.start_ts + .2)])
        chunks.append(au); off += len(au) / 24000
        gap = np.zeros(int(24000 * .12)); chunks.append(gap); off += .12
    a = np.concatenate(chunks).astype(np.float32)
    # trim silence
    thr = 0.01 * np.max(np.abs(a))
    nz = np.where(np.abs(a) > thr)[0]
    s0, s1 = max(0, nz[0] - 600), min(len(a), nz[-1] + 2400)
    a = a[s0:s1]
    words = [[w, max(0, b - s0 / 24000), max(0, e - s0 / 24000)] for w, b, e in words]
    sf.write(path + '.wav', a, 24000)
    json.dump(words, open(path + '.json', 'w'))
    return a, words


def chunks_for(cap, words, maxw=7):
    cw = cap.split()
    if not words:
        return []
    n = len(cw)
    times = [words[min(len(words) - 1, int(i * len(words) / n))][1] for i in range(n)]
    out, i = [], 0
    while i < n:
        j = i
        while j < n and j - i < maxw:
            j += 1
            if cw[j - 1][-1] in '.?!' and j - i >= 2:
                break
        end = words[min(len(words) - 1, int((j - 1) * len(words) / n))][2] + .25
        out.append([' '.join(cw[i:j]), times[i], end])
        i = j
    for k in range(len(out) - 1):
        out[k][2] = min(out[k][2], out[k + 1][1])
    return out


def scene_sfx(S):
    """Sound design events (local time, kind, gain) mirroring each scene's animation clock."""
    ty, p, dur = S['type'], S['p'], S['dur']
    ev = []
    if ty == 'kinetic':
        toks = sum(len(l.split(' ')) for l in p['lines'])
        for rt in SC.disp_reveal_times(S, toks):
            ev.append((rt, 'bass' if p.get('style') == 'slam' else 'tick', .35 if p.get('style') == 'slam' else .8))
            if p.get('style') == 'slam':
                ev.append((rt, 'click', .6))
    elif ty == 'tabs':
        N = p.get('n', 47)
        for i in range(N):
            ev.append((0.05 + dur * .72 * (i / N) ** 1.3 + .2, 'pop', .22))
    elif ty == 'chat':
        td = p.get('type_dur', min(2.2, dur * .45))
        k = 0.1
        while k < td:
            ev.append((k, 'key', .9)); k += np.random.uniform(.045, .09)
        ev.append((td + .1, 'pop', .6))
        if p.get('recursion', True):
            for r in range(7):
                ev.append((td + r * (dur - td) / 7, 'glitch', .25))
    elif ty == 'graveyard':
        files = p.get('files', [1] * 6)
        for rt in SC.disp_reveal_times(S, len(files)):
            ev.append((rt + .3, 'bass', .4))
        ev.append((dur * .62, 'impact', .55))
    elif ty == 'array':
        steps = 6
        for i in range(steps):
            ev.append((i * dur * .75 / steps, 'tick', .9))
        if p.get('mode') == 'break':
            ev += [(dur * .55, 'glitch', .8), (dur * .55 + .1, 'impact', .5)]
    elif ty == 'counter':
        k = .1
        while k < .1 + min(1.8, dur * .6):
            ev.append((k, 'tick', .6)); k += .05 + .1 * (k / 2)
        ev.append((.1 + min(1.8, dur * .6), 'bass', .6))
    elif ty in ('graph', 'notes'):
        n = len(p.get('nodes', p.get('notes', [])))
        for rt in SC.disp_reveal_times(S, n):
            ev.append((rt, 'pop', .6))
    elif ty == 'screen':
        ev.append((0.0, 'whoosh_down', .5))
        for c in p.get('callouts', []):
            ev.append((c[3] * dur, 'click', .8))
    elif ty == 'montage':
        for rt in SC.disp_reveal_times(S, len(p['words'])):
            ev += [(rt - .05, 'bass', .45), (rt - .05, 'click', .7)]
    elif ty == 'loop':
        for rt in SC.disp_reveal_times(S, len(p['steps'])):
            ev.append((rt, 'tick', 1.0))
    elif ty == 'resume':
        ev.append((dur * .3, 'impact', .5))
        for i in range(5):
            ev.append((dur * .42 + i * dur * .09 + .25, 'pop', .6))
    elif ty == 'grid':
        ev += [(dur * .35, 'bass', .7), (dur * .55, 'glitch', .7), (dur * .55, 'whoosh', .5)]
    elif ty == 'cta':
        ev += [(0.05, 'stinger', .55), (1.1, 'pop', .6), (1.8, 'click', 1.0)]
    tr = S.get('tr')
    if S['idx'] > 0:
        ev.append((-0.42, 'whoosh', .55))
    if tr == 'glitch':
        ev.append((0, 'glitch', .6))
    if tr == 'zoom':
        ev.append((0, 'bass', .6))
    return ev


def build_timeline(V):
    bdir = os.path.join(BUILD, V['slug']); os.makedirs(bdir, exist_ok=True)
    beat = 60 / V['bpm']; bar = beat * 4
    q = beat * (2 if beat < .45 else 1)
    t = 0.0
    scs = []
    for i, s in enumerate(V['scenes']):
        S = dict(s); S['p'] = s.get('p', {}); S['idx'] = i; S['n'] = len(V['scenes'])
        a, words = tts(s['say'], V['voice'], V['speed'], os.path.join(bdir, 'vo_%02d' % i))
        if s.get('drop') and scs:
            nb = math.ceil((t - 1e-6) / bar) * bar
            scs[-1]['dur'] += nb - t; t = nb
        lead = .35 if s.get('drop') else .18
        vd = len(a) / 24000
        dur = math.ceil((lead + vd + .4 + s.get('hold', 0)) / q) * q
        S.update(t0=t, dur=dur, vo=a, vo_at=t + lead, vod=vd,
                 words=[[w, b + lead, e + lead] for w, b, e in words])
        S['chunks'] = chunks_for(s['cap'], S['words'])
        scs.append(S); t += dur
    return scs, t


# ------------------------------------------------------------------ audio
def render_audio(V, scs, total, adir):
    SR = A.SR; n = int(total * SR)
    vo = np.zeros(n)
    for S in scs:
        v = resample_poly(S['vo'], 2, 1)
        A.place(vo, v, S['vo_at'])
    vo = A.vo_chain(vo)
    sections = [(S['t0'], S['t0'] + S['dur'], S.get('energy', 2), bool(S.get('drop'))) for S in scs]
    music, beat = A.compose(total, V['bpm'], V['style'], sections)
    music = A.peaking(music, 2800, -3.0, .8)  # carve space for the voice
    sfx = np.zeros(n)
    events = []
    for S in scs:
        for (lt, kind, g) in scene_sfx(S):
            at = S['t0'] + lt
            if 0 <= at < total:
                A.place(sfx, A.SFX[kind](), at, g)
                events.append(dict(t=round(at, 3), kind=kind, gain=g, scene=S['idx']))
    sfx = np.tanh(sfx * .9)
    duck = A.duck_env(vo, .6)
    fade = np.ones(n); fl = int(SR * 1.5); fade[-fl:] = np.linspace(1, 0, fl) ** 2; fade[:int(SR * .02)] = np.linspace(0, 1, int(SR * .02))
    music_bus = music * fade
    mix = vo * 1.0 + music_bus * duck * .55 + sfx * .45
    mo = music_bus * .7 + sfx * .45
    stems = dict(narration=vo * .9, music=music_bus * .9 / (np.max(np.abs(music_bus)) + 1e-9), sfx=sfx * .9 / (np.max(np.abs(sfx)) + 1e-9))
    raw = os.path.join(BUILD, V['slug'])
    sf.write(raw + '/mix_raw.wav', mix / (np.max(np.abs(mix)) + 1e-9) * .8, SR)
    sf.write(raw + '/musiconly_raw.wav', mo / (np.max(np.abs(mo)) + 1e-9) * .8, SR)
    for k, x in stems.items():
        sf.write(f'{adir}/{k}.wav', x.astype(np.float32), SR, subtype='PCM_24')
    loudnorm(raw + '/mix_raw.wav', raw + '/mix.wav')
    loudnorm(raw + '/musiconly_raw.wav', raw + '/musiconly.wav')
    loudnorm(f'{adir}/narration.wav', f'{adir}/narration.wav', tmp=True)
    for k in ('narration', 'music', 'sfx'):
        sh(f'ffmpeg -v error -y -i {adir}/{k}.wav -c:a libmp3lame -b:a 256k {adir}/{k}.mp3')
    sh(f'cp {raw}/mix.wav {adir}/full_mix.wav && ffmpeg -v error -y -i {adir}/full_mix.wav -b:a 320k {adir}/full_mix.mp3')
    return events


def sh(c):
    return subprocess.run(c, shell=True, check=True, capture_output=True, text=True)


def loudnorm(src, dst, tmp=False, I=-14, TP=-2.2):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', src, '-af', f'loudnorm=I={I}:TP={TP}:LRA=11:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rfind('{'):r.stderr.rfind('}') + 1])
    af = (f"loudnorm=I={I}:TP={TP}:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,alimiter=limit={10 ** ((TP - 0.4) / 20):.3f}:attack=1:release=60:level=false")
    out = dst + '.tmp.wav' if tmp or src == dst else dst
    sh(f'ffmpeg -v error -y -i "{src}" -af "{af}" -ar 48000 -c:a pcm_s24le "{out}"')
    if out != dst:
        os.replace(out, dst)


def measure(path):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', path, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True)
    s = r.stderr[r.stderr.rfind('Summary:'):]
    I = float(re.search(r'I:\s+(-?[\d.]+) LUFS', s).group(1))
    tp = float(re.search(r'Peak:\s+(-?[\d.]+) dBFS', s).group(1))
    return dict(integrated_lufs=I, true_peak_dbtp=tp)


# ------------------------------------------------------------------ video
def render_video(V, scs, total, path, only=None):
    C0 = V['pal']; C = {k: (hexc(v) if isinstance(v, str) else v) for k, v in C0.items()}
    bg = bg_texture(C['bg'][:3], C['line'][:3], 48, V['bgkind'])
    nF = int(round(total * FPS))
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', path]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE) if only is None else None
    t_start = time.time(); si = 0
    frames = range(nF) if only is None else only
    stills = []
    for f in frames:
        g = f / FPS
        while si + 1 < len(scs) and g >= scs[si + 1]['t0']:
            si += 1
        while si > 0 and g < scs[si]['t0']:
            si -= 1
        S = scs[si]; lt = g - S['t0']
        img = bg.copy(); d = ImageDraw.Draw(img)
        SC.SCENES[S['type']](img, d, lt, S, C)
        SC.hud(img, d, lt, S, C)
        # burned caption
        for ctext, cs, ce in S['chunks']:
            if cs - .05 <= lt < ce:
                tw, th = tsize(ctext, 'mono', 28)
                a = min(1, (lt - cs + .05) / .12)
                pill(img, d, ctext, W / 2, H - 92, C['fg'], C['bg'], 28, anchor='c', a=a)
                break
        # progress bar
        d.rectangle((0, H - 6, W * g / total, H), fill=C['a1'])
        # transitions
        tr = S.get('tr')
        if tr == 'flash' and lt < .25:
            img = Image.blend(img, Image.new('RGB', (W, H), C['fg'][:3] if not C['dark'] else (255, 255, 255)), (1 - lt / .25) * .85)
        elif tr == 'glitch' and lt < .3:
            img = glitch(img, 1 - lt / .3, seed=f)
        elif lt < .22 and si > 0:
            z = 1 + (0.14 if tr == 'zoom' else .045) * (1 - eo(lt / .22))
            cw, ch = W / z, H / z
            img = img.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.BILINEAR)
        nxt = scs[si + 1] if si + 1 < len(scs) else None
        if nxt and nxt.get('tr') == 'wipe' and S['dur'] - lt < .2:
            x = W * eo((.2 - (S['dur'] - lt)) / .2)
            ImageDraw.Draw(img).rectangle((0, 0, x, H), fill=C['a1'])
        if tr == 'wipe' and lt < .2:
            x = W * eo(lt / .2)
            ImageDraw.Draw(img).rectangle((x, 0, W, H), fill=C['a1'])
        if proc:
            proc.stdin.write(img.tobytes())
            if f % 150 == 0:
                el = time.time() - t_start
                print(f'  {V["slug"]} frame {f}/{nF}  {f / max(el, 1e-3):.1f} fps', flush=True)
        else:
            stills.append(img)
    if proc:
        proc.stdin.close(); proc.wait()
    return stills


def srt_time(x, sep=','):
    return '%02d:%02d:%02d%s%03d' % (int(x // 3600), int(x % 3600 // 60), int(x % 60), sep, int(round((x % 1) * 1000)) % 1000)


def main(which=None):
    for V in VIDEOS:
        if which and V['slug'] not in which:
            continue
        print('==', V['slug'], flush=True)
        od = os.path.join(OUT, V['slug'])
        for sub in ('audio', 'captions', 'thumbnails', 'source'):
            os.makedirs(os.path.join(od, sub), exist_ok=True)
        scs, total = build_timeline(V)
        print(f'  timeline {total:.2f}s, {len(scs)} scenes', flush=True)
        events = render_audio(V, scs, total, os.path.join(od, 'audio'))
        silent = os.path.join(BUILD, V['slug'], 'video_silent.mp4')
        if not os.path.exists(silent) or os.environ.get('FORCE'):
            render_video(V, scs, total, silent)
        b = os.path.join(BUILD, V['slug'])
        final = os.path.join(od, f'{V["slug"]}_FINAL.mp4')
        mo = os.path.join(od, f'{V["slug"]}_MUSIC_ONLY.mp4')
        sh(f'ffmpeg -v error -y -i {silent} -i {b}/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart {final}')
        sh(f'ffmpeg -v error -y -i {silent} -i {b}/musiconly.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart {mo}')
        # captions
        srt, vtt, k = [], ['WEBVTT', ''], 1
        for S in scs:
            for c, cs, ce in S['chunks']:
                a0, a1 = S['t0'] + cs, S['t0'] + ce
                srt += [str(k), f'{srt_time(a0)} --> {srt_time(a1)}', c, '']
                vtt += [f'{srt_time(a0, ".")} --> {srt_time(a1, ".")}', c, '']; k += 1
        open(f'{od}/captions/{V["slug"]}.srt', 'w').write('\n'.join(srt))
        open(f'{od}/captions/{V["slug"]}.vtt', 'w').write('\n'.join(vtt))
        open(f'{od}/captions/script.txt', 'w').write('\n'.join(S['cap'] for S in scs))
        # thumbnails: reveal frame + storyboard
        rev = next(S for S in scs if S.get('drop'))
        fr = int((rev['t0'] + rev['dur'] * .7) * FPS)
        sh(f'ffmpeg -v error -y -ss {fr / FPS:.2f} -i {final} -frames:v 1 {od}/thumbnails/thumbnail.png')
        sh(f'ffmpeg -v error -y -ss {scs[0]["t0"] + scs[0]["dur"] * .8:.2f} -i {final} -frames:v 1 {od}/thumbnails/hook_frame.png')
        sh(f'ffmpeg -v error -y -i {final} -vf "fps={16 / total:.5f},scale=480:-1,tile=4x4" -frames:v 1 {od}/thumbnails/storyboard.png')
        # editable source: timeline + events + engine copy
        tl = [dict(idx=S['idx'], type=S['type'], tag=S.get('tag'), start=round(S['t0'], 3), dur=round(S['dur'], 3),
                   vo_start=round(S['vo_at'], 3), say=S['say'], caption=S['cap'], words=S['words'], params=S['p'],
                   energy=S.get('energy'), drop=bool(S.get('drop')), transition=S.get('tr')) for S in scs]
        json.dump(dict(title=V['title'], bpm=V['bpm'], style=V['style'], voice=V['voice'], tts='Kokoro-82M (local, Apache-2.0)',
                       duration=round(total, 3), scenes=tl, sfx_events=events), open(f'{od}/source/timeline.json', 'w'), indent=1)
        sh(f'cp {ROOT}/engine/*.py {od}/source/ && cd {od}/source && rm -f tts_bench.py')
        # verify
        probe = json.loads(sh(f'ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate:format=duration -of json {final}').stdout)
        nar, _ = sf.read(f'{od}/audio/narration.wav')
        nar = nar if nar.ndim == 1 else nar.mean(1)
        fr_ = nar[:len(nar) // 2400 * 2400].reshape(-1, 2400)
        voiced = float(np.mean(20 * np.log10(np.sqrt((fr_ ** 2).mean(1)) + 1e-9) > -40))
        mus, _ = sf.read(f'{od}/audio/music.wav')
        rep = dict(final=measure(final), music_only=measure(mo), probe=probe, narration_voiced_ratio=round(voiced, 3),
                   music_rms_dbfs=round(float(20 * np.log10(np.sqrt((mus ** 2).mean()) + 1e-9)), 2), duration=total)
        json.dump(rep, open(f'{od}/verify.json', 'w'), indent=1)
        print('  verify', json.dumps(rep['final']), 'voiced', voiced, flush=True)
        post = f"""{V['title']}\n\nPost copy:\n{scs[0]['cap']} {scs[1]['cap']}\nPlaciq is the AI-native Career Intelligence OS for engineering students - DSA, projects, resume, GitHub and career goals, connected.\nStart free: https://learn.placiq.in/\n\n#Placiq #PlacementPrep #DSA #EngineeringStudents #CareerOS #BuildInPublic\n\nNote: product visuals are real captures from the Placiq product demo; outcomes are not guaranteed.\n"""
        open(f'{od}/captions/post_copy.txt', 'w').write(post)


if __name__ == '__main__':
    if '--campaign' in sys.argv:
        import campaign_build
        a = sys.argv
        campaign_build.run(resume='--resume' in a, days=[int(x) for x in a[a.index('--days') + 1].split(',')] if '--days' in a else None,
                           preview='--preview' in a)
    else:
        main(sys.argv[1:] or None)
