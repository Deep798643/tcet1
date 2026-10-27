"""Writes campaign-level docs + gallery data from real files on disk (never from intent)."""
import csv, datetime, json, os
from campaign import DAYS
from campaign_build import CAMP, day_dir, load_state, ROOT

START = datetime.date(2026, 11, 2)
TIMES = ['13:00', '18:30', '20:30', '21:30', '12:30', '19:30', '17:00']


def rel(p):
    return os.path.relpath(p, ROOT)


def write_all():
    st = load_state(); rows = []; man = []
    for D in DAYS:
        n = D['day']; od = day_dir(n); fin = os.path.join(od, 'final.mp4')
        rec = st['days'].get(str(n), {})
        done = rec.get('stage') == 'done' and os.path.exists(fin)
        meta = json.load(open(od + '/metadata.json')) if os.path.exists(od + '/metadata.json') else {}
        date = START + datetime.timedelta(days=n - 1)
        rows.append(dict(day=n, date=str(date), time_ist=TIMES[n % 7], topic=D['title'], pillar=D['pillar'], audience='Indian engineering/CS students 18-25',
                         format=D['fmt'], mp4=rel(fin) if done else '', thumbnail=rel(od + '/thumbnail.png') if done else '', hook=D['hooks'][0],
                         cta='learn.placiq.in' if n != 60 else 'placiq.in', caption=rel(od + '/captions_instagram.txt') if done else '',
                         status='ready_to_post' if done else rec.get('stage', 'not_started')))
        man.append(dict(day=n, title=D['title'], pillar=D['pillar'], format=D['fmt'], status=rows[-1]['status'], dir=rel(od),
                        duration=meta.get('duration'), qa=meta.get('qa'), hooks=D['hooks'], youtube_title=D['yt'],
                        ig=D['ig'] + '\n\n' + ' '.join(D['tags'])))
    with open(CAMP + '/CONTENT_CALENDAR.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(CAMP + '/ANALYTICS_TEMPLATE.csv', 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['day', 'platform', 'posted_at_ist', 'views', 'avg_watch_sec', 'completion_pct', 'likes', 'comments', 'shares', 'saves', 'profile_visits', 'link_clicks', 'notes'])
        for r in rows:
            for pl in ('instagram', 'youtube_shorts'):
                w.writerow([r['day'], pl] + [''] * 11)
    json.dump(dict(generated=datetime.datetime.utcnow().isoformat() + 'Z', total=len(DAYS), planned=60,
                   completed=sum(r['status'] == 'ready_to_post' for r in rows), videos=man), open(CAMP + '/CAMPAIGN_MANIFEST.json', 'w'), indent=1)
    open(CAMP + '/ALL_HOOKS.md', 'w').write('# All hooks\n\n' + '\n'.join(f"## Day {D['day']:02d} - {D['title']}\n" + '\n'.join(f"{i + 1}. {h}{' **(selected)**' if i == 0 else ''}" for i, h in enumerate(D['hooks'])) + '\n' for D in DAYS))
    open(CAMP + '/ALL_CAPTIONS.md', 'w').write('# All captions\n\n' + '\n'.join(f"## Day {D['day']:02d} - {D['title']}\n\n**Instagram**\n\n{D['ig']}\n\n{' '.join(D['tags'])}\n\n**YouTube title:** {D['yt']}\n\n**LinkedIn:** {D['li']}\n" for D in DAYS))
    sc = []
    for D in DAYS:
        p = day_dir(D['day']) + '/script.md'
        sc.append(open(p).read() if os.path.exists(p) else f"# Day {D['day']:02d} - {D['title']}\n(not rendered yet)\n")
    open(CAMP + '/ALL_SCRIPTS.md', 'w').write('\n\n'.join(sc))
    q = ['# Quality report', '', 'Automated checks per film (ffprobe/ffmpeg): 1080x1920, 30fps, 1 AAC stream, integrated loudness -17..-12 LUFS, true peak <= -0.9 dBTP, no black segments >1s, narration voiced ratio >0.3 (narrated only). Contact sheets (storyboard.png) are generated for every film; batch contact sheets were visually inspected by the agent before publishing.', '',
         '| Day | Title | Status | Dur | LUFS | TP | Black | Freeze>2.5s | Voiced |', '|---|---|---|---|---|---|---|---|---|']
    for m in man:
        qa = m['qa'] or {}
        q.append(f"| {m['day']} | {m['title']} | {m['status']} | {m['duration'] or ''} | {qa.get('lufs', '')} | {qa.get('true_peak', '')} | {qa.get('black_segments', '')} | {qa.get('frozen_segments_over_2_5s', '')} | {qa.get('narration_voiced_ratio', '')} |")
    open(CAMP + '/QUALITY_REPORT.md', 'w').write('\n'.join(q) + '\n')
    open(CAMP + '/README.md', 'w').write(f"""# Placiq 60-day campaign\n\nVertical 1080x1920 / 30fps / H.264 + AAC shorts. Completed: {sum(r['status'] == 'ready_to_post' for r in rows)} / 60 (see PRODUCTION_STATE.json).\n\nResume production:\n\n```\ncd placiq-videos/engine\npython build.py --campaign 60day --resume\n```\n\nRe-render specific days: `python build.py --campaign 60day --days 3,4`  |  Preview contact sheets: add `--preview`.\n\nNarration: Kokoro-82M (local). Music/SFX: procedural (engine/audio2.py). Product visuals: real Placiq demo footage. Nothing is auto-published.\n""")
    # gallery data
    gal = os.path.join(ROOT, 'gallery'); os.makedirs(gal, exist_ok=True)
    json.dump(man, open(gal + '/campaign.json', 'w'), indent=1)
