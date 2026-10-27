"""60-day campaign producer: resumable queue -> TTS -> beat-quantized timeline -> score/SFX -> 1080x1920 render -> QA -> deliverables.
Usage: python build.py --campaign 60day --resume [--days 1,2,3]
"""
import json, math, os, subprocess, time, datetime
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
from PIL import Image, ImageDraw
from core import *
import build as B
import audio2 as A2
import vscenes3 as VS
from scenes import disp_reveal_times
from campaign import DAYS

CAMP = os.path.join(ROOT, '60-day-campaign')
STATE = os.path.join(CAMP, 'PRODUCTION_STATE.json')
CACHE = os.path.join(ROOT, 'build', 'campaign')


def day_dir(n):
    if n >= 57:
        return os.path.join(CAMP, 'BONUS_DAYS_57_TO_60', 'DAY_%02d' % n)
    return os.path.join(CAMP, 'WEEK_%02d' % ((n - 1) // 7 + 1), 'DAY_%02d' % n)


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return dict(days={}, updated=None)


def save_state(st):
    st['updated'] = datetime.datetime.utcnow().isoformat() + 'Z'
    json.dump(st, open(STATE, 'w'), indent=1)


def timeline(D):
    st = A2.STY[D['style']]; bpm = D.get('bpm', st['bpm'])
    beat = 60 / bpm; bar = beat * 4; q = beat * (2 if beat < .45 else 1)
    cache = os.path.join(CACHE, 'DAY_%02d' % D['day']); os.makedirs(cache, exist_ok=True)
    t = 0.0; scs = []
    narrated = D['fmt'] == 'narrated' or any('say' in s for s in D['scenes'])
    for i, s in enumerate(D['scenes']):
        S = dict(s); S['p'] = s.get('p', {}); S['idx'] = i; S['n'] = len(D['scenes']); S['daytag'] = 'DAY %02d' % D['day']
        if s.get('drop') and scs:
            nb = math.ceil((t - 1e-6) / bar) * bar; scs[-1]['dur'] += nb - t; t = nb
        lead = .3 if s.get('drop') else .15
        if 'say' in s:
            a, words = B.tts(s['say'], D.get('voice', 'af_heart'), D.get('speed', 1.06), os.path.join(cache, 'vo_%02d' % i))
            vd = len(a) / 24000
            dur = math.ceil((lead + vd + .35 + s.get('hold', 0)) / q) * q
            S.update(vo=a, vo_at=t + lead, words=[[w, b + lead, e + lead] for w, b, e in words])
        else:
            dur = math.ceil(s['dur'] / q) * q
            cw = s['cap'].split(); n = len(cw)
            span = min(dur * .55, .32 * n + .2)
            S.update(vo=None, vo_at=None, words=[[w, .2 + span * k / max(1, n), .2 + span * (k + 1) / max(1, n)] for k, w in enumerate(cw)])
        S.update(t0=t, dur=dur)
        S['chunks'] = B.chunks_for(s['cap'], S['words'], 6)
        scs.append(S); t += dur
    return scs, t, bpm, narrated


def sfx_for(S):
    ty, p, dur = S['type'], S['p'], S['dur']; ev = []
    if ty == 'vtype':
        n = sum(len(l.split(' ')) for l in p['lines'])
        for rt in disp_reveal_times(S, n):
            ev += [(rt, 'bass', .35), (rt, 'click', .5)] if p.get('slam') else [(rt, 'tick', .8)]
    elif ty == 'vtabs':
        N = p.get('n', 37)
        for i in range(N):
            ev.append((.05 + dur * .6 * (i / N) ** 1.25 + .15, 'pop', .2))
        if p.get('merge', 2) < 1:
            ev += [(dur * p['merge'], 'whoosh', .7), (dur * p['merge'] + .6, 'impact', .5)]
    elif ty == 'vterm':
        k = .15
        while k < dur * .8:
            ev.append((k, 'key', .7)); k += np.random.uniform(.05, .1)
        if p.get('alert'):
            ev += [(dur * p['alert'][1], 'glitch', .8), (dur * p['alert'][1], 'beep', .6)]
    elif ty == 'vpile':
        items = p.get('items', [0] * 14); ct = dur * p.get('collapse', .72)
        for i in range(len(items)):
            ev.append((.05 + i * (ct * .9 / len(items)) + .2, 'pop', .35))
        ev += [(ct, 'glitch', .6), (ct + .5, 'stamp', .6)]
    elif ty == 'vchats':
        n = p.get('n', 12)
        for i in range(n):
            ev.append((.8 + dur * .7 * (i / n) ** .6, 'notif', .4))
    elif ty == 'vreset':
        for i in range(6):
            ev += [(.3 + i * dur * .12, 'pop', .5), (.3 + i * dur * .12 + .05, 'glitch', .45)]
    elif ty == 'vboard':
        cyc = p.get('cycles', 3); seg = dur * .8 / cyc
        for c in range(cyc):
            ev.append((c * seg + seg * .6, 'eraser', .9))
    elif ty == 'vcards':
        seg = dur / len(p['cards'])
        for i in range(len(p['cards'])):
            ev += [(i * seg, 'whoosh', .6), (i * seg + 1.0, 'stamp', .4)]
    elif ty == 'vdash':
        ev += [(dur * .35, 'whoosh', .4), (dur * .6, 'beep', .7), (dur * .62, 'bass', .6)]
    elif ty == 'vmeters':
        for k in range(12):
            ev.append((.1 + k * dur * .05, 'tick', .5))
    elif ty == 'vorbit':
        for i in range(10):
            ev.append((.05 + i * .12, 'pop', .4))
        if p.get('hub', 2) < 1:
            ev += [(dur * p['hub'], 'whoosh', .6), (dur * p['hub'] + .6, 'bass', .7)]
    elif ty == 'vclip':
        ev.append((0, 'whoosh_down', .5))
        for c in p.get('callouts', []):
            ev.append((c[3] * dur, 'click', .9))
    elif ty == 'vcta':
        ev += [(.05, 'stinger', .5), (.9, 'pop', .6)]
    elif ty == 'vnumber':
        for k in range(14):
            ev.append((.1 + k * .1, 'tick', .5))
    if S['idx'] > 0:
        ev.append((-.38, 'whoosh', .45))
    return ev


def render(D, scs, total, path, frames=None, scale=1.0):
    C = {k: (hexc(v) if isinstance(v, str) else v) for k, v in D['pal'].items()}
    bg = bg_texture(C['bg'][:3], C['line'][:3], 54, 'dots' if D['day'] % 2 else 'lines')
    nF = int(round(total * FPS))
    proc = None
    if frames is None:
        proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                 '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', path], stdin=subprocess.PIPE)
    out = []; si = 0
    for f in (range(nF) if frames is None else frames):
        g = f / FPS
        si = max(i for i, S in enumerate(scs) if S['t0'] <= g + 1e-9)
        S = scs[si]; lt = g - S['t0']
        img = bg.copy(); d = ImageDraw.Draw(img)
        VS.VSCENES[S['type']](img, d, lt, S, C)
        VS.vhud(img, d, lt, S, C)
        if S.get('vo') is not None:
            for ct, cs, ce in S['chunks']:
                if cs - .05 <= lt < ce:
                    lines = VS.wrap(ct, 'mono', 40, 900)
                    for j, ln in enumerate(lines):
                        pill(img, d, ln, W / 2, 1600 + j * 70, C['fg'], C['bg'], 40, anchor='c')
                    break
        d.rectangle((0, H - 8, W * g / total, H), fill=C['a1'])
        tr = S.get('tr')
        if tr == 'glitch' and lt < .3:
            img = glitch(img, 1 - lt / .3, seed=f)
        elif lt < .2 and si > 0:
            z = 1 + .06 * (1 - eo(lt / .2)); cw, ch = W / z, H / z
            img = img.crop((int((W - cw) / 2), int((H - ch) / 2), int((W + cw) / 2), int((H + ch) / 2))).resize((W, H), Image.BILINEAR)
        if proc:
            proc.stdin.write(img.tobytes())
        else:
            out.append(img)
    if proc:
        proc.stdin.close(); proc.wait()
    return out


def wr(path, txt):
    open(path, 'w').write(txt)


def produce(D, st):
    n = D['day']; od = day_dir(n); os.makedirs(os.path.join(od, 'source'), exist_ok=True)
    rec = st['days'].setdefault(str(n), dict(stage='queued'))
    cache = os.path.join(CACHE, 'DAY_%02d' % n)
    scs, total, bpm, narrated = timeline(D)
    rec.update(stage='timeline', duration=round(total, 2)); save_state(st)
    SR = A2.SR; N = int(total * SR)
    # ---------------- audio
    vo = np.zeros(N)
    if narrated:
        for S in scs:
            if S.get('vo') is not None:
                A2.place(vo, resample_poly(S['vo'], 2, 1), S['vo_at'])
        vo = A2.vo_chain(vo)
    secs = [(S['t0'], S['t0'] + S['dur'], S.get('energy', 2), bool(S.get('drop'))) for S in scs]
    music, beat = A2.compose2(total, D['style'], secs, seed=n * 7 + 3, root=D.get('root', 45), bpm=bpm)
    music = A2.peaking(music, 2800, -3.0 if narrated else 0, .8)
    sfx = np.zeros(N); events = []
    for S in scs:
        for lt, kind, g in sfx_for(S):
            at = S['t0'] + lt
            if 0 <= at < total:
                A2.place(sfx, A2.SFX[kind](), at, g); events.append([round(at, 3), kind, g])
    sfx = np.tanh(sfx * .9)
    fade = np.ones(N); fl = int(SR * 1.2); fade[-fl:] = np.linspace(1, 0, fl) ** 2
    music *= fade
    duck = A2.duck_env(vo, .6) if narrated else np.ones(N)
    mix = vo + music * duck * (.55 if narrated else .8) + sfx * .45
    mo = music * .75 + sfx * .45
    sf.write(cache + '/mix_raw.wav', mix / (np.abs(mix).max() + 1e-9) * .8, SR)
    sf.write(cache + '/mo_raw.wav', mo / (np.abs(mo).max() + 1e-9) * .8, SR)
    B.loudnorm(cache + '/mix_raw.wav', od + '/mix.wav', TP=-3.0); B.loudnorm(cache + '/mo_raw.wav', cache + '/mo.wav', TP=-3.0)
    sf.write(od + '/music.wav', (music / (np.abs(music).max() + 1e-9) * .89).astype(np.float32), SR, subtype='PCM_16')
    sf.write(od + '/sfx.wav', (sfx / (np.abs(sfx).max() + 1e-9) * .89).astype(np.float32), SR, subtype='PCM_16')
    if narrated:
        sf.write(od + '/narration.wav', (vo * .9).astype(np.float32), SR, subtype='PCM_16')
        B.loudnorm(od + '/narration.wav', od + '/narration.wav', tmp=True)
        B.sh(f'ffmpeg -v error -y -i {od}/narration.wav -b:a 192k {od}/narration.mp3')
    else:
        for f in ('narration.wav', 'narration.mp3'):
            if os.path.exists(od + '/' + f):
                os.remove(od + '/' + f)
        wr(od + '/narration.NOT_APPLICABLE.txt', 'Music-led film: narration deliberately omitted. No silent placeholder audio was generated.\n')
    B.sh(f'ffmpeg -v error -y -i {od}/music.wav -b:a 192k {od}/music.mp3')
    B.sh(f'ffmpeg -v error -y -i {od}/mix.wav -c:a pcm_s16le {od}/mix16.wav && mv {od}/mix16.wav {od}/mix.wav')
    rec.update(stage='audio'); save_state(st)
    # ---------------- video
    silent = cache + '/silent.mp4'
    t0 = time.time(); render(D, scs, total, silent); rec['render_sec'] = round(time.time() - t0, 1)
    B.sh(f'ffmpeg -v error -y -i {silent} -i {od}/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart {od}/final.mp4')
    B.sh(f'ffmpeg -v error -y -i {silent} -i {cache}/mo.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart {od}/music_only.mp4')
    rec.update(stage='video'); save_state(st)
    # ---------------- stills, subtitles
    drop = next((S for S in scs if S.get('drop')), scs[len(scs) // 2])
    B.sh(f'ffmpeg -v error -y -ss {drop["t0"] + drop["dur"] * .7:.2f} -i {od}/final.mp4 -frames:v 1 {od}/thumbnail.png')
    B.sh(f'ffmpeg -v error -y -ss 0.6 -i {od}/final.mp4 -frames:v 1 {od}/opening_frame.png')
    B.sh(f'ffmpeg -v error -y -i {od}/final.mp4 -vf "fps={12 / total:.5f},scale=270:-1,tile=6x2" -frames:v 1 {od}/storyboard.png')
    srt, vtt, k = [], ['WEBVTT', ''], 1
    for S in scs:
        for c, cs, ce in S['chunks']:
            a0, a1 = S['t0'] + cs, min(S['t0'] + S['dur'], S['t0'] + max(ce, cs + .8))
            srt += [str(k), f'{B.srt_time(a0)} --> {B.srt_time(a1)}', c, '']; vtt += [f'{B.srt_time(a0, ".")} --> {B.srt_time(a1, ".")}', c, '']; k += 1
    wr(od + '/subtitles.srt', '\n'.join(srt)); wr(od + '/subtitles.vtt', '\n'.join(vtt))
    # ---------------- copy
    tags = ' '.join(D['tags'])
    wr(od + '/captions_instagram.txt', D['ig'] + '\n\n' + tags + '\n')
    yt_desc = f"{D['hooks'][0]}\n\n{D['li']}\n\nPlaciq is an AI-native Career Intelligence OS for students: DSA, projects, resume, GitHub and career goals, connected.\nTry it free: https://learn.placiq.in/\n\n#Shorts {tags}"
    wr(od + '/captions_youtube.txt', f"TITLE: {D['yt']}\n\nDESCRIPTION:\n{yt_desc}\n\nKEYWORDS: placiq, placement preparation, {D['pillar'].lower()}, engineering students, career os, {D['title'].lower()}\n\nPINNED COMMENT (optional): {D.get('comment', 'Which part of this is most relatable? Tell us below.')}\n")
    wr(od + '/captions_linkedin.txt', f"{D['li']}\n\nDay {n} of our 60-day series on connected career preparation. Placiq brings DSA practice, project evidence, resume intelligence and career direction into one learner workspace.\n\nhttps://learn.placiq.in/\n")
    wr(od + '/first_comment.txt', D.get('comment', 'Which part of this is most relatable? Tell us below.') + '\nStart free: https://learn.placiq.in/\n')
    script = [f"# Day {n:02d} - {D['title']}", '', f"Pillar: {D['pillar']}  |  Format: {D['fmt']}  |  Music: {D['style']} {bpm} BPM  |  Duration: {total:.1f}s", '',
              '## Hooks', *[f"{i + 1}. {h}{'  (SELECTED)' if i == 0 else ''}" for i, h in enumerate(D['hooks'])], '', '## Scenes']
    for S in scs:
        script.append(f"- [{S['t0']:.2f}s, {S['dur']:.2f}s] {S['type']}: " + (f"VO: \"{S['say']}\"" if S.get('say') else f"ON-SCREEN: {S['cap']}"))
    wr(od + '/script.md', '\n'.join(script) + '\n')
    # ---------------- QA
    qa = validate(od, total, narrated)
    tl = [dict(idx=S['idx'], type=S['type'], start=round(S['t0'], 3), dur=round(S['dur'], 3), say=S.get('say'), caption=S['cap'], params=S['p'],
               energy=S.get('energy'), drop=bool(S.get('drop')), words=S['words']) for S in scs]
    json.dump(dict(day=n, scenes=tl, sfx_events=events, bpm=bpm, style=D['style'], root=D.get('root')), open(od + '/source/timeline.json', 'w'), indent=1)
    wr(od + '/source/README.md', f"Editable source for Day {n:02d}.\n\n- Scene spec: `placiq-videos/engine/campaign.py` (day({n}, ...))\n- Scene library: `placiq-videos/engine/vscenes*.py`\n- Score/SFX: `placiq-videos/engine/audio2.py` (style `{D['style']}`, seed {n * 7 + 3})\n- Timeline with word timings + SFX events: `timeline.json`\n\nRe-render: `cd placiq-videos/engine && python build.py --campaign 60day --days {n}`\n")
    meta = dict(day=n, title=D['title'], pillar=D['pillar'], format=D['fmt'], narrated=narrated, voice=D.get('voice') if narrated else None,
                tts='Kokoro-82M (local)' if narrated else None, music_style=D['style'], bpm=bpm, duration=round(total, 2),
                hooks=dict(selected=D['hooks'][0], alternatives=D['hooks'][1:]), cta='learn.placiq.in' if n != 60 else 'placiq.in',
                youtube_title=D['yt'], hashtags=D['tags'], resolution='1080x1920', fps=30, qa=qa,
                files=sorted(os.listdir(od)), product_footage='Real captures from the Placiq product demo (assets/real-product)')
    json.dump(meta, open(od + '/metadata.json', 'w'), indent=1)
    rec.update(stage='done' if qa['pass'] else 'qa_failed', qa=qa, title=D['title'])
    save_state(st)
    return qa


def validate(od, total, narrated):
    pr = json.loads(B.sh(f'ffprobe -v error -show_entries stream=codec_type,codec_name,width,height,r_frame_rate:format=duration -of json {od}/final.mp4').stdout)
    v = next(s for s in pr['streams'] if s['codec_type'] == 'video'); a = [s for s in pr['streams'] if s['codec_type'] == 'audio']
    m = B.measure(od + '/final.mp4')
    bl = subprocess.run(f'ffmpeg -v info -i {od}/final.mp4 -vf "blackdetect=d=1.0:pix_th=0.05,freezedetect=n=0.001:d=2.5" -an -f null -', shell=True, capture_output=True, text=True).stderr
    black = bl.count('black_start'); freeze = bl.count('freeze_start')
    voiced = None
    if narrated:
        x, _ = sf.read(od + '/narration.wav'); x = x[:len(x) // 2400 * 2400].reshape(-1, 2400)
        voiced = round(float(np.mean(20 * np.log10(np.sqrt((x ** 2).mean(1)) + 1e-9) > -40)), 3)
    ok = (v['width'], v['height']) == (1080, 1920) and v['r_frame_rate'] == '30/1' and len(a) == 1 and m['true_peak_dbtp'] <= -0.9 \
        and -17 <= m['integrated_lufs'] <= -12 and black == 0 and (not narrated or voiced > .3)
    return dict(**{'pass': bool(ok)}, width=v['width'], height=v['height'], fps=v['r_frame_rate'], duration=float(pr['format']['duration']),
                audio_streams=len(a), lufs=m['integrated_lufs'], true_peak=m['true_peak_dbtp'], black_segments=black, frozen_segments_over_2_5s=freeze,
                narration_voiced_ratio=voiced)


def run(resume=True, days=None, preview=False):
    os.makedirs(CAMP, exist_ok=True)
    st = load_state()
    todo = [D for D in DAYS if (days is None or D['day'] in days)]
    if preview:
        for D in todo:
            scs, total, _, _ = timeline(D)
            fr = [int((S['t0'] + S['dur'] * .7) * FPS) for S in scs]
            ims = render(D, scs, total, None, frames=fr)
            sheet = Image.new('RGB', (len(ims) * 360, 640))
            for i, im in enumerate(ims):
                sheet.paste(im.resize((360, 640)), (i * 360, 0))
            sheet.save(os.path.join(CACHE, 'preview_%02d.png' % D['day']))
            print('preview', D['day'], round(total, 1), flush=True)
        return
    for D in todo:
        rec = st['days'].get(str(D['day']), {})
        if resume and days is None and rec.get('stage') == 'done' and os.path.exists(os.path.join(day_dir(D['day']), 'final.mp4')):
            print('skip day', D['day'], flush=True); continue
        print('== day', D['day'], D['title'], flush=True)
        try:
            qa = produce(D, st)
            print('   qa', json.dumps(qa), flush=True)
        except Exception as e:
            import traceback; traceback.print_exc()
            st['days'].setdefault(str(D['day']), {}).update(stage='error', error=str(e)[:300]); save_state(st)
    import campaign_docs; campaign_docs.write_all()
