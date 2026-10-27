"""60-day campaign specs. Each day: scenes for the vertical engine + publishing copy. Spoken 'Place IQ' = Placiq."""
PAPER = dict(bg='#F5F2EC', bg2='#E9E4DA', fg='#0F1117', card='#FFFFFF', a1='#3151EE', fg_on_a1='#FFFFFF', a2='#FF533B', a3='#1DB954', muted='#8A877F', line='#D8D2C6', dark=False)
INK = dict(bg='#0F1117', bg2='#1B1E27', fg='#F5F7FF', card='#1E2230', a1='#3151EE', fg_on_a1='#FFFFFF', a2='#FF533B', a3='#D6FF38', muted='#7A8092', line='#2C3142', dark=True)
BLUE = dict(bg='#3151EE', bg2='#2741C9', fg='#FFFFFF', card='#2A45D6', a1='#0F1117', fg_on_a1='#FFFFFF', a2='#D6FF38', a3='#FFFFFF', muted='#AFC0FF', line='#4D69F2', dark=True)
MONO = dict(bg='#0A0A0A', bg2='#161616', fg='#F2F2F2', card='#1C1C1C', a1='#FFFFFF', fg_on_a1='#0A0A0A', a2='#3151EE', a3='#BBBBBB', muted='#7A7A7A', line='#2A2A2A', dark=True)
WHITE = dict(bg='#FFFFFF', bg2='#F1F3F9', fg='#0F1117', card='#F4F6FB', a1='#3151EE', fg_on_a1='#FFFFFF', a2='#0F1117', a3='#3151EE', muted='#8C93A3', line='#E1E5EE', dark=False)
TERM = dict(bg='#050807', bg2='#0B120F', fg='#C8FFD4', card='#0E1712', a1='#39FF88', fg_on_a1='#03140A', a2='#FF533B', a3='#3151EE', muted='#4E7A5E', line='#14241B', dark=True)
P = 'Place IQ'

DAYS = []


def day(n, **k):
    k['day'] = n; DAYS.append(k)


# ================================================================ WEEK 1 - STUDENT PAIN
day(1, title='The 37-Tab Student', pillar='Student pain', fmt='narrated', style='electro', root=45, pal=PAPER, voice='am_puck', speed=1.1,
    hooks=['Your browser has 37 tabs. Your prep has zero connections.', 'Count your tabs. I will wait.', 'This is what placement prep looks like at 1 AM.'],
    scenes=[dict(type='vtabs', say="Tab one: LeetCode. Tab thirty-seven: I don't even know anymore.", cap="Tab 1: LeetCode. Tab 37: I don't even know anymore.", p=dict(n=37), energy=1),
            dict(type='vtype', say="Every tab knows one thing about you. None of them talk to each other.", cap="Every tab knows one thing about you. None of them talk to each other.", p=dict(lines=['EVERY TAB KNOWS', 'ONE THING.', '*NONE TALK.']), energy=2, tr='glitch'),
            dict(type='vtabs', say=f"{P} pulls D S A, projects, resume and GitHub into one connected workflow.", cap="Placiq pulls DSA, projects, resume and GitHub into one connected workflow.", p=dict(n=37, merge=.15, seed=4), energy=3, drop=True),
            dict(type='vcta', say="Close the tabs. Keep the progress.", cap="Close the tabs. Keep the progress.", p=dict(v='stack', words=['CLOSE', 'THE TABS.', 'KEEP PROGRESS.']), energy=1, hold=1.2)],
    ig="37 tabs open and still no idea what to do next?\n\nLeetCode in one tab, your resume in another, a course you paused in the third. Each one knows a piece of you, and none of them talk.\n\nPlaciq connects DSA, projects, resume and GitHub into one workflow. Try it free at learn.placiq.in",
    tags=['#placementprep', '#engineeringstudents', '#dsa', '#codinglife', '#placiq'],
    yt='Your Browser Has 37 Tabs. Your Prep Has 0 Connections.', li="Students rarely lack resources; they lack connection between them. Here is what tab overload looks like, and why connected preparation matters.")

day(2, title='Busy, But Going Where?', pillar='Student pain', fmt='music', style='minimal', root=48, pal=INK,
    hooks=['11 hours of studying. How much of it can you show?', 'Busy is not ready.', 'Activity and progress are not the same bar.'],
    scenes=[dict(type='vtype', dur=2.2, cap='11 hours of studying today.', p=dict(lines=['11 HOURS', 'OF STUDYING.'], slam=True), energy=1),
            dict(type='vmeters', dur=6.0, cap='Activity: 100%. Progress you can show: 18%.', p=dict(hours=11, prog=.18), energy=2),
            dict(type='vtype', dur=3.2, cap='Busy is not ready. Evidence is.', p=dict(lines=['BUSY IS', '~NOT READY.', '*EVIDENCE IS.']), energy=3, drop=True),
            dict(type='vclip', dur=4.5, cap='Readiness that tracks what you actually shipped.', p=dict(clip='readiness', pan=((0, 0), (.9, .2)), cw=.55, title='Track proof, not hours.'), energy=3),
            dict(type='vcta', dur=3.0, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Busy is not ready.'), energy=1)],
    ig="Studied 11 hours. Can you show any of it?\n\nHours feel like progress. Recruiters and interviewers see evidence: shipped projects, solved patterns, a resume that proves it.\n\nTrack proof, not hours. learn.placiq.in",
    tags=['#studentlife', '#placements', '#productivity', '#placiq'],
    yt='11 Hours of Study vs Progress You Can Show', li='Activity is not the same as progress. A short look at why evidence-based preparation beats hours logged.')

day(3, title='The Productivity Graveyard', pillar='Student pain', fmt='music', style='breakbeat', root=43, pal=PAPER,
    hooks=['roadmap_v14.pdf', 'You have revised your roadmap more than you have followed it.', 'Planning is the most comfortable form of procrastination.'],
    scenes=[dict(type='vpile', dur=7.5, cap='roadmap_v1 ... roadmap_v14. Still on step 1.', p=dict(collapse=.68), energy=2),
            dict(type='vtype', dur=3.0, cap='Stop rewriting the plan. Start step 1.', p=dict(lines=['STOP', '~REWRITING.', '*START.'], slam=True), energy=3, drop=True),
            dict(type='vclip', dur=4.5, cap="Placiq turns a goal into today's quests.", p=dict(clip='readiness', pan=((.4, 0), (1, .3)), cw=.5, title="Today's quests, not v15.", callouts=[('daily quests', .5, .4, .35)]), energy=3),
            dict(type='vcta', dur=3.0, cap='Placiq - learn.placiq.in', p=dict(v='stack', words=['LESS PLAN.', 'MORE', 'PROGRESS.']), energy=1)],
    ig="roadmap_final_v14.pdf (still on step 1)\n\nPlanning feels productive. Execution is what shows up in interviews.\n\nPlaciq breaks your goal into small daily quests so you start today. learn.placiq.in",
    tags=['#roadmap', '#procrastination', '#codingjourney', '#placiq'],
    yt='Roadmap v14 and Still on Step 1', li='Over-planning is a common trap in placement preparation. Execution, in small steps, compounds.')

day(4, title='One Internship, Ten Platforms', pillar='Student pain', fmt='narrated', style='house', root=50, pal=WHITE, voice='af_heart', speed=1.06,
    hooks=['One internship. Ten platforms pulling at you.', 'Your prep is being pulled in ten directions.', 'Which app is your career living in?'],
    scenes=[dict(type='vorbit', say="One internship. Ten platforms. All of them pulling you in a different direction.", cap="One internship. Ten platforms. All pulling you in a different direction.", p=dict(hub=1.5), energy=1),
            dict(type='vorbit', say=f"Connected preparation means every tool feeds one picture of you. That's the idea behind {P}.", cap="Connected prep means every tool feeds one picture of you. That's the idea behind Placiq.", p=dict(hub=.25), energy=3, drop=True),
            dict(type='vcta', say="Your work, connected.", cap="Your work, connected.", p=dict(v='logo'), energy=1, hold=1.5)],
    ig="One internship. Ten platforms. Zero shared context.\n\nWhen your DSA, resume, projects and goals live in separate apps, you become the integration layer.\n\nPlaciq connects them into one picture of you. learn.placiq.in",
    tags=['#internship', '#placementseason', '#cse', '#placiq'],
    yt='One Internship, Ten Platforms', li='Fragmented tools create fragmented preparation. Connected preparation lets each activity inform the next.')

day(5, title='Student Browser Horror', pillar='Student pain', fmt='comedy', style='glitchhop', root=41, pal=TERM,
    hooks=['2:07 AM. Assignment due 9 AM. OA at 10.', 'A horror story in one terminal.', 'POV: placement season at 2 AM.'],
    scenes=[dict(type='vterm', dur=9.0, cap='2:07 AM - assignment due 9 AM, OA at 10, resume last edited 2024.', p=dict(lines=['$ date', ('Tue 02:07 AM', 'muted'), '$ ls deadlines/', ('assignment_DBMS.pdf   due 09:00', 'a2'), ('online_assessment     10:00', 'a2'), '$ git log --oneline | wc -l', ('3', 'muted'), '$ cat resume.pdf | grep 2026', ('no matches', 'a2'), '$ open leetcode', ('Daily: Hard', 'a2')], alert=('PANIC.EXE', .82), cps=38), energy=2),
            dict(type='vtype', dur=3.0, cap='Horror is not the deadline. It is the scattered prep.', p=dict(lines=['THE HORROR?', '*SCATTERED', 'PREP.']), energy=3, drop=True),
            dict(type='vclip', dur=4.5, cap='One workspace that knows what is due next.', p=dict(clip='copilot', pan=((0, 0), (.6, .2)), cw=.5, title='Know what matters next.'), energy=3),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Sleep is a feature.'), energy=1)],
    ig="POV: it's 2:07 AM and every deadline just remembered you exist.\n\nAssignment at 9, OA at 10, resume from last year. We have all been there.\n\nPlaciq keeps your prep in one place so 2 AM is less horror, more plan. learn.placiq.in",
    tags=['#codinghumor', '#engineeringlife', '#placementseason', '#placiq'],
    yt='Placement Prep Horror at 2:07 AM', li='A light look at late-night placement stress, and how organised preparation reduces it.')

day(6, title='The Skill Gap You Cannot See', pillar='Student pain', fmt='narrated', style='cinematic', root=40, pal=INK, voice='am_michael', speed=1.04,
    hooks=['Your dashboard says 90%. One bar is lying.', 'The weakness you never practise does not show up in your streak.', 'Green everywhere. Except where it matters.'],
    scenes=[dict(type='vdash', say="Forty-one day streak. Every bar looks great. But one of them is hiding something.", cap="41-day streak. Every bar looks great. But one is hiding something.", p=dict(), energy=1),
            dict(type='vtype', say="The gap you never practise is the one interviews find.", cap="The gap you never practise is the one interviews find.", p=dict(lines=['THE GAP YOU', 'SKIP IS THE GAP', '*THEY FIND.']), energy=3, drop=True),
            dict(type='vclip', say=f"{P}'s readiness view surfaces your primary bottleneck, so you fix the right thing first.", cap="Placiq's readiness view surfaces your primary bottleneck, so you fix the right thing first.", p=dict(clip='passport', pan=((0, 0), (.6, .3)), cw=.55, title='See the real gap.'), energy=2),
            dict(type='vcta', say="Find your gap. Free.", cap="Find your gap. Free.", p=dict(v='logo', tag='Find the real gap.'), energy=1, hold=1.2)],
    ig="Your dashboard is 90% green. One bar is lying to you.\n\nStreaks reward what you already like practising. The topic you avoid is often the one that shows up in the interview.\n\nPlaciq's free readiness audit highlights your primary bottleneck. learn.placiq.in",
    tags=['#dsa', '#interviewprep', '#skillgap', '#placiq'],
    yt='The Skill Gap Your Streak Hides', li='Progress dashboards can mask blind spots. Identifying the primary bottleneck changes what you practise next.')

day(7, title='Send This to Your Coding Friend', pillar='Student pain', fmt='comedy', style='funk', root=47, pal=BLUE,
    hooks=['Which one are you? Tag the friend.', 'Three coders. Every hostel has them.', 'Collect all three cards.'],
    scenes=[dict(type='vcards', dur=12.0, cap='The Tutorial Collector. The DSA Grinder. The Endless Starter.', p=dict(cards=[
        dict(name='The Tutorial Collector', emoji='01', stats=[('Videos saved', .98), ('Projects finished', .06), ('Confidence', .4)], ability='Special move: "I will start after this playlist."'),
        dict(name='The DSA Grinder', emoji='02', stats=[('Problems solved', .95), ('Projects built', .1), ('Sleep', .15)], ability='Special move: solves Hards, freezes on "tell me about your project."'),
        dict(name='The Endless Starter', emoji='03', stats=[('Repos created', .97), ('READMEs written', .05), ('Ideas', 1.0)], ability='Special move: 14 repos, all named test-final.')]), energy=2),
            dict(type='vtype', dur=3.0, cap='All three need the same thing: connected proof.', p=dict(lines=['ALL THREE NEED', '*CONNECTED', 'PROOF.']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Send this to them.'), energy=1)],
    ig="Tag the friend who is card #2.\n\nThe Tutorial Collector, the DSA Grinder and the Endless Starter all work hard. What they are missing is a way to connect that effort into proof.\n\nThat is what Placiq is built for. learn.placiq.in",
    tags=['#codingmemes', '#developers', '#engineeringstudents', '#placiq'],
    yt='3 Types of Coding Students (Which One Are You?)', li='Three common preparation patterns, all hard-working, all missing connected evidence. A light-hearted look.')

# ================================================================ WEEK 2 - AI MEMORY (D08-D10 in batch 1)
day(8, title='New Chat, Same Introduction', pillar='AI memory', fmt='music', style='trap', root=46, pal=WHITE,
    hooks=["You have introduced yourself to AI more than to your batchmates.", 'New chat. Same intro. Again.', 'Ctrl+C, Ctrl+V: my entire AI relationship.'],
    scenes=[dict(type='vchats', dur=8.0, cap="New chat #1... #14. Same introduction every time.", p=dict(n=14, count='SAME INTRO x%d'), energy=2),
            dict(type='vtype', dur=3.0, cap='What if it already knew you?', p=dict(lines=['WHAT IF IT', '*ALREADY', 'KNEW YOU?']), energy=3, drop=True),
            dict(type='vclip', dur=5.0, cap='PCME: persistent context memory across sessions.', p=dict(clip='pcme', pan=((0, 0), (.7, .2)), cw=.5, title='Memory that carries over.'), energy=3),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Introduce yourself once.'), energy=1)],
    ig="New chat. Same introduction. Again.\n\n\"Hi, I'm a 3rd-year CSE student...\" Typed so many times it lives in your clipboard.\n\nPlaciq's PCME memory carries your context across sessions. Introduce yourself once. learn.placiq.in",
    tags=['#ai', '#chatgpt', '#studentlife', '#placiq'],
    yt='New Chat, Same Introduction', li='Most AI tools start every session from zero. Persistent context changes the quality of guidance students receive.')

day(9, title='The Reset Button', pillar='AI memory', fmt='narrated', style='industrial', root=42, pal=INK, voice='am_michael', speed=1.06,
    hooks=['Your work keeps growing. Your AI keeps resetting.', 'Every new project. Every new chat. Context: deleted.', 'Watch the right side reset.'],
    scenes=[dict(type='vreset', say="Your work keeps growing. A hundred and forty problems. A chat app. Resume version four. But every new chat... resets.", cap="Your work keeps growing. 140 problems. A chat app. Resume v4. But every new chat... resets.", p=dict(), energy=2),
            dict(type='vtype', say=f"{P} keeps the context. So the advice grows with you.", cap="Placiq keeps the context. So the advice grows with you.", p=dict(lines=['KEEP', 'THE *CONTEXT.']), energy=3, drop=True),
            dict(type='vcta', say="No more resets.", cap="No more resets.", p=dict(v='stack', words=['NO MORE', 'RESETS.', 'KEEP GOING.']), energy=1, hold=1.2)],
    ig="Your work keeps growing. Your AI keeps hitting reset.\n\n140 problems, a half-built chat app, resume v4, and every new conversation starts at zero.\n\nPlaciq keeps context across sessions so advice grows with you. learn.placiq.in",
    tags=['#aitools', '#placementprep', '#cse', '#placiq'],
    yt='Your AI Keeps Hitting Reset', li='Context loss between sessions makes AI advice generic. Persistent memory keeps guidance relevant as students progress.')

day(10, title='The Context Eraser', pillar='AI memory', fmt='music', style='cinematic', root=38, pal=MONO,
    hooks=['Imagine a mentor who erases the board every time you leave.', 'Session 1. Session 2. Session 3. Same blank board.', 'This is what forgetting looks like.'],
    scenes=[dict(type='vboard', dur=10.0, cap="A mentor who erases everything about you after every session.", p=dict(cycles=3), energy=1),
            dict(type='vtype', dur=3.2, cap='Good mentors remember. So should your AI.', p=dict(lines=['GOOD MENTORS', '*REMEMBER.']), energy=3, drop=True),
            dict(type='vcta', dur=2.8, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='A mentor that remembers.'), energy=1)],
    ig="Imagine a mentor who wipes the board after every session.\n\nYour weak topics, your project, your goal: gone. That is how most AI chats work.\n\nPlaciq's PCME keeps the board. learn.placiq.in",
    tags=['#mentorship', '#ai', '#engineering', '#placiq'],
    yt='The Mentor Who Erases Everything', li='A visual metaphor for context loss in AI guidance, and why persistent memory matters for learners.')

day(11, title='AI Advice for Everyone', pillar='AI memory', fmt='comedy', style='funk', root=44, pal=PAPER,
    hooks=['Four different students. One identical roadmap.', 'The advice machine has one setting.', 'Generic in, generic out.'],
    scenes=[dict(type='vfactory', dur=9.5, cap='Four different students go in. One identical roadmap comes out.', p=dict(), energy=2),
            dict(type='vtype', dur=3.0, cap='Your path should start from your work.', p=dict(lines=['ADVICE SHOULD', 'START FROM', '*YOUR WORK.']), energy=3, drop=True),
            dict(type='vclip', dur=4.5, cap='Career Navigator builds a role-specific plan.', p=dict(clip='roadmap', pan=((0, 0), (.6, .3)), cw=.5, title='A plan for your role.'), energy=3),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Not one-size-fits-all.'), energy=1)],
    ig="Four students. Four different goals. One copy-paste roadmap.\n\nGeneric AI advice treats an ECE data lover and a backend-focused CSE student the same way.\n\nPlaciq's Career Navigator starts from your role and your actual work. learn.placiq.in",
    tags=['#careeradvice', '#roadmap', '#ai', '#placiq'], yt='The Generic Advice Machine', li='Generic recommendations ignore context. Role-specific plans built from a student\'s real work are more useful.')

day(12, title='Your Work Should Connect', pillar='AI memory', fmt='narrated', style='house', root=49, pal=WHITE, voice='af_heart', speed=1.06,
    hooks=['You solved 3 sliding-window problems. Did your mentor notice?', 'Your DSA practice should change your next recommendation.', 'Practice that talks back.'],
    scenes=[dict(type='vclip', say="This is a real D S A session in Place IQ. Step by step, every pointer move is visible.", cap="This is a real DSA session in Placiq. Step by step, every pointer move is visible.", p=dict(clip='dsa_run', pan=((.2, .2), (.75, .4)), cw=.55, title='Practice, step by step.', callouts=[('step-through', .5, .55, .5)]), energy=2),
            dict(type='vclip', say="And the Placement Copilot sees that work. Its suggestions come from your progress, strengths and weak spots.", cap="And the Placement Copilot sees that work. Its suggestions come from your progress, strengths and weak spots.", p=dict(clip='copilot', pan=((0, .1), (.5, .4)), cw=.5, title='Advice that knows it.', callouts=[('your progress in context', .5, .45, .4)]), energy=3, drop=True),
            dict(type='vcta', say="Your work, connected.", cap="Your work, connected.", p=dict(v='stack'), energy=1, hold=1.2)],
    ig="You did the practice. Your guidance should know about it.\n\nIn Placiq, your DSA sessions and projects feed the Placement Copilot, so suggestions reflect your real strengths and weak spots.\n\nSee it free at learn.placiq.in",
    tags=['#dsa', '#ai', '#placementprep', '#placiq'], yt='Your DSA Practice Should Change Your Next Step', li='Connected modules mean practice data informs guidance. A look at the DSA Visualizer and Placement Copilot together.')

day(13, title='The AI Tutor Intervention', pillar='AI memory', fmt='comedy', style='glitchhop', root=40, pal=INK,
    hooks=['Five AI tabs. Five different career plans.', 'POV: asking every chatbot what to learn next.', 'The group chat nobody asked for.'],
    scenes=[dict(type='vsplit', dur=8.5, cap='Five AI tabs. Five confident, contradictory plans.', p=dict(win=.66, win_txt='One tutor that knows your work.'), energy=2),
            dict(type='vclip', dur=4.5, cap='A Copilot that reads your progress first.', p=dict(clip='copilot', pan=((.3, 0), (.9, .3)), cw=.5, title='Context first.'), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='One voice. Your context.'), energy=1)],
    ig="Asked five AI tabs what to learn next. Got five different futures.\n\nWhen advice ignores your actual progress, it is just confident noise.\n\nPlaciq's Copilot reads your work before it answers. learn.placiq.in",
    tags=['#aihumor', '#codinglife', '#students', '#placiq'], yt='Five AI Tabs, Five Different Plans', li='Contradictory AI advice is a real source of student confusion. Context-aware guidance reduces it.')

day(14, title='PCME Product Reveal', pillar='AI memory', fmt='narrated', style='cinematic', root=41, pal=BLUE, voice='am_michael', speed=1.04,
    hooks=['Monday to Saturday. One memory.', 'What if every session built on the last?', 'Meet the memory behind Placiq.'],
    scenes=[dict(type='vtimeline', say="Monday, sliding window. Tuesday, an auth module. Thursday, a weak spot in D P. Scattered, until it isn't.", cap="Monday: sliding window. Tuesday: an auth module. Thursday: a weak spot in DP. Scattered, until it isn't.", p=dict(snap=.25), energy=2),
            dict(type='vclip', say="P C M E, the Persistent Context and Memory Engine, keeps that timeline. So every session builds on the last one.", cap="PCME, the Persistent Context & Memory Engine, keeps that timeline. Every session builds on the last one.", p=dict(clip='pcme', pan=((0, 0), (.7, .3)), cw=.5, title='PCME memory.'), energy=3, drop=True),
            dict(type='vcta', say="Place IQ. The career OS that remembers you.", cap="Placiq. The career OS that remembers you.", p=dict(v='logo', tag='The career OS that remembers you.'), energy=1, hold=1)],
    ig="Monday: sliding window. Thursday: weak on DP. Saturday: README pushed.\n\nOn their own, these are scattered moments. PCME, Placiq's Persistent Context & Memory Engine, keeps them as one timeline so every session builds on the last.\n\nlearn.placiq.in",
    tags=['#pcme', '#ai', '#careeros', '#placiq'], yt='PCME: The Memory Behind Placiq', li='Persistent context turns scattered study sessions into a continuous record that guidance can build on.')

# ================================================================ WEEK 3 - DSA
day(15, title='Two Sum Is Not Two Lines', pillar='DSA', fmt='narrated', style='electro', root=47, pal=PAPER, voice='am_puck', speed=1.08,
    hooks=['Two Sum in one pass. Here is the actual idea.', 'You memorised the code. Do you know why it works?', 'The one question that solves Two Sum.'],
    scenes=[dict(type='varr', say="Two Sum. Target nine. For each number, ask one question: have I already seen target minus me?", cap="Two Sum, target 9. For each number ask: have I already seen target minus me?", p=dict(mode='hash', vals=[2, 7, 11, 15], target=9, steps=2, title='TWO SUM, TARGET 9'), energy=2),
            dict(type='varr', say="Store each value with its index in a hash map. Check before you store. One pass. O of n time.", cap="Store value -> index in a hash map. Check before you store. One pass, O(n) time.", p=dict(mode='hash', vals=[3, 8, 4, 1, 5, 6], target=9, steps=5, title='CHECK, THEN STORE'), energy=3, drop=True),
            dict(type='vcta', say="Understand the pattern. Not just the code.", cap="Understand the pattern, not just the code.", p=dict(v='logo', tag='Patterns over memory.'), energy=1, hold=1)],
    ig="Two Sum is not about two lines of code. It is one question.\n\nFor each number: have I already seen target minus me? Check the hash map, then store. One pass, O(n).\n\nPractise patterns step by step in Placiq's DSA Visualizer. learn.placiq.in",
    tags=['#twosum', '#leetcode', '#dsa', '#hashmap', '#placiq'], yt='Two Sum Explained in One Question', li='The hash-map insight behind Two Sum, animated: check for the complement before storing each value.')

day(16, title='Pointer Chaos', pillar='DSA', fmt='music', style='breakbeat', root=45, pal=INK,
    hooks=['Your pointer when you have not understood the loop.', 'Where is p going? Nobody knows.', 'Random jumps vs one clear rule.'],
    scenes=[dict(type='varr', dur=9.0, cap='Pointer without a rule: random jumps. Pointer with a rule: p += 1, one step at a time.', p=dict(mode='chaos', vals=[4, 9, 2, 7, 5, 1, 8], title='WHERE IS p GOING?'), energy=2),
            dict(type='vtype', dur=3.0, cap='Every pointer needs a rule.', p=dict(lines=['EVERY POINTER', 'NEEDS A', '*RULE.']), energy=3, drop=True),
            dict(type='vclip', dur=4.0, cap='See pointer state in the real DSA Visualizer.', p=dict(clip='dsa_run', pan=((.25, .3), (.5, .45)), cw=.45, title='Watch the rule.'), energy=3),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Pointers with purpose.'), energy=1)],
    ig="Your pointer when you have not understood the loop invariant.\n\nA pointer should move by one clear rule. If you cannot state the rule, you cannot debug the loop.\n\nWatch pointer state step by step in Placiq's DSA Visualizer. learn.placiq.in",
    tags=['#pointers', '#dsa', '#codingmemes', '#placiq'], yt='Pointer Chaos vs One Clear Rule', li='Every pointer in an algorithm should move by a rule you can state. A short visual on invariants.')

day(17, title='The Dry-Run Nightmare', pillar='DSA', fmt='narrated', style='industrial', root=39, pal=MONO, voice='am_michael', speed=1.05,
    hooks=['Dry-running a loop in your head feels like this.', 'Lost in your own for-loop?', 'The maze is just a loop without a trace table.'],
    scenes=[dict(type='vmaze', say="Dry-running a loop in your head feels like a maze. You lose track of i, the sum, everything. The fix is boring and powerful: write a trace table, one iteration per row.", cap="Dry-running a loop in your head feels like a maze. The fix: a trace table, one iteration per row.", p=dict(), energy=2),
            dict(type='vtype', say="Trace it. Then trust it.", cap="Trace it. Then trust it.", p=dict(lines=['TRACE IT.', '*TRUST IT.'], slam=True), energy=3, drop=True),
            dict(type='vcta', say="Step through algorithms in Place IQ.", cap="Step through algorithms in Placiq.", p=dict(v='logo', tag='Trace it. Trust it.'), energy=1, hold=1)],
    ig="Dry-running a loop in your head feels like a maze.\n\nThe fix is a trace table: one row per iteration, every variable written down. Boring, and it works in interviews too.\n\nStep through algorithms visually in Placiq. learn.placiq.in",
    tags=['#dryrun', '#debugging', '#dsa', '#placiq'], yt='How to Dry-Run Any Loop', li='Trace tables make loop behaviour explicit. A simple technique that improves interview problem solving.')

day(18, title='Watch the Algorithm Think', pillar='DSA', fmt='music', style='minimal', root=50, pal=WHITE,
    hooks=['Sliding window, in 10 seconds.', 'Add one in, drop one out.', 'This is what O(n) looks like.'],
    scenes=[dict(type='varr', dur=9.0, cap='Sliding window, k = 3: add the new element, drop the old one. Never recompute the whole sum.', p=dict(mode='window', vals=[4, 2, 7, 1, 8, 3, 5, 6], k=3, steps=6, title='SLIDING WINDOW, k = 3'), energy=2),
            dict(type='vclip', dur=4.5, cap='Patterns animated step by step in Placiq.', p=dict(clip='dsa', pan=((0, .2), (.5, .5)), cw=.5, title='Animated patterns.'), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Watch it think.'), energy=1)],
    ig="Sliding window in 10 seconds: add one in, drop one out.\n\nInstead of recomputing every window sum, update it as the window moves. That is the whole O(n) trick.\n\nAnimate core patterns step by step in Placiq. learn.placiq.in",
    tags=['#slidingwindow', '#algorithms', '#dsa', '#placiq'], yt='Sliding Window in 10 Seconds', li='The sliding-window pattern visualised: incremental updates instead of recomputation.')

day(19, title='Brute Force vs Optimized', pillar='DSA', fmt='narrated', style='dnb', root=45, pal=INK, voice='am_puck', speed=1.08,
    hooks=['Both solutions are correct. Only one survives n = 10,000.', 'O(n squared) vs O(n), raced.', 'Correct is not the same as scalable.'],
    scenes=[dict(type='vrace', say="Both are correct. Brute force checks every pair: about n squared over two operations. The hash map checks each number once: about n. At ten thousand, that's fifty million versus ten thousand.", cap="Both correct. Brute force: ~n²/2 pair checks. Hash map: ~n. At n = 10,000: ~50 million vs ~10,000.", p=dict(), energy=2),
            dict(type='vtype', say="Start brute. Then optimise. Explain both.", cap="Start brute. Then optimise. Explain both.", p=dict(lines=['START BRUTE.', '*OPTIMISE.', 'EXPLAIN BOTH.']), energy=3, drop=True),
            dict(type='vcta', say="Compare approaches in Place IQ.", cap="Compare approaches in Placiq.", p=dict(v='logo', tag='Correct, then scalable.'), energy=1, hold=1)],
    ig="Both solutions pass the sample tests. Only one survives n = 10,000.\n\nBrute force checks about n^2/2 pairs. A hash map checks each value once. In interviews, start with brute force, then explain the optimisation.\n\nThe DSA Visualizer shows brute force and optimised side by side. learn.placiq.in",
    tags=['#timecomplexity', '#bigO', '#dsa', '#placiq'], yt='Brute Force vs Optimised, Raced', li='Time complexity made visible: why O(n^2) and O(n) diverge as input grows.')

day(20, title='DSA Without Understanding', pillar='DSA', fmt='music', style='electro', root=43, pal=BLUE,
    hooks=['1,803 questions. About a handful of core patterns.', 'Stop counting problems. Start counting patterns.', 'The question bank is big. The idea bank is small.'],
    scenes=[dict(type='vcollapse', dur=9.0, cap='Hundreds of problems collapse into a few reusable patterns.', p=dict(), energy=2),
            dict(type='vnumber', dur=3.5, cap="1,803 questions in Placiq's vault - learn the patterns behind them.", p=dict(n=1803, label='QUESTIONS IN THE VAULT'), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Patterns, not piles.'), energy=1)],
    ig="Stop counting problems. Start counting patterns.\n\nMost interview questions reuse a small set of ideas: two pointers, sliding window, hashing, BFS/DFS, binary search, DP.\n\nPlaciq's vault has 1,803 questions, organised so the patterns stand out. learn.placiq.in",
    tags=['#leetcode', '#dsapatterns', '#codinginterview', '#placiq'], yt='1,803 Questions, A Few Patterns', li='Pattern-based practice scales better than problem counting. A visual on consolidating DSA preparation.')

day(21, title='DSA Visualizer Hero Film', pillar='DSA', fmt='music', style='dnb', root=45, pal=INK,
    hooks=['This is what DSA looks like when it moves.', 'Real footage. No slides.', 'Press play on an algorithm.'],
    scenes=[dict(type='vtype', dur=2.0, cap='Press play on an algorithm.', p=dict(lines=['PRESS PLAY', 'ON AN *ALGORITHM.'], slam=True), energy=2),
            dict(type='vreel', dur=11.0, cap='Real Placiq DSA Visualizer: pick a pattern, step through it, read the live code and variables.', p=dict(clips=[('dsa', (0, .1), (.15, .3), .45), ('dsa_run', (.25, .3), (.5, .5), .42), ('dsa_run', (.7, .2), (1, .45), .4), ('dsa', (.4, .3), (.8, .5), .45)], labels=['PICK A PATTERN', 'STEP THROUGH IT', 'LIVE CODE + STATE', 'BRUTE VS OPTIMAL']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='DSA that moves.', foot='1,803-question vault  |  core patterns animated'), energy=1)],
    ig="This is what DSA looks like when it moves.\n\nReal footage of Placiq's DSA Visualizer: pick a pattern, step through each move, read the live code and variable state, compare brute force with optimal.\n\nTry the starter patterns free at learn.placiq.in",
    tags=['#dsavisualizer', '#algorithms', '#leetcode', '#placiq'], yt='DSA Visualizer: Real Product Footage', li="A fast look at Placiq's DSA Visualizer, step-through animations with live code and state.")

day(22, title='Tutorial Hell', pillar='Projects', fmt='narrated', style='trap', root=42, pal=MONO, voice='am_puck', speed=1.06,
    hooks=['The moment the tutorial ends.', 'Seven tutorials watched. Zero lines written alone.', 'What happens when the video stops?'],
    scenes=[dict(type='vvanish', say="Seven tutorials. Every one made sense. Then they're gone, and it's just you and a blinking cursor.", cap="Seven tutorials. Every one made sense. Then they're gone, and it's just you and a blinking cursor.", p=dict(), energy=1),
            dict(type='vtype', say="Watching is not building. Start small, but start alone.", cap="Watching is not building. Start small, but start alone.", p=dict(lines=['WATCHING', '~IS BUILDING.', '*START ALONE.']), energy=3, drop=True),
            dict(type='vcta', say="Guided projects, in Place IQ.", cap="Guided projects in Placiq.", p=dict(v='logo', tag='Escape tutorial hell.'), energy=1, hold=1)],
    ig="Seven tutorials, all made sense. Then the video ends.\n\nTutorial hell is not a knowledge problem, it is a practice problem. The blank editor is where learning actually starts.\n\nPlaciq's AI Project Builder guides you module by module, without writing it for you. learn.placiq.in",
    tags=['#tutorialhell', '#coding', '#projects', '#placiq'], yt='Tutorial Hell: When the Video Ends', li='Independent building is the step tutorials cannot replace. Guided practice bridges the gap.')

day(23, title='Your Eighth TODO App', pillar='Projects', fmt='comedy', style='arcade', root=48, pal=PAPER,
    hooks=['TODO app number eight. Achievement unlocked?', 'Your portfolio, but every project is a TODO list.', 'Recruiters have seen this one.'],
    scenes=[dict(type='vclones', dur=9.0, cap='todo-app, todo-app-2, todo-final... then one idea that solves a real problem.', p=dict(), energy=2),
            dict(type='vtype', dur=3.0, cap='Build something only you would build.', p=dict(lines=['BUILD WHAT', '*ONLY YOU', 'WOULD BUILD.']), energy=3, drop=True),
            dict(type='vclip', dur=4.5, cap='Project Builder catalog: scoped, guided projects.', p=dict(clip='builder', pan=((0, .1), (.6, .4)), cw=.5, title='Pick a real project.'), energy=3),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Retire the TODO app.'), energy=1)],
    ig="TODO app #8 is not the flex you think it is.\n\nClones teach basics, but a project that solves a problem you actually have tells a better story.\n\nPlaciq's AI Project Builder helps scope a project around your gaps. learn.placiq.in",
    tags=['#todoapp', '#webdev', '#portfolio', '#placiq'], yt='Your Eighth TODO App', li='Distinctive projects communicate more than repeated clones. A light look at portfolio choices.')

day(24, title='The Abandoned Repository', pillar='Projects', fmt='music', style='cinematic', root=38, pal=INK,
    hooks=['Welcome to the city of unfinished repos.', 'Last commit: 7 months ago.', 'Every scaffold is a project you started.'],
    scenes=[dict(type='vcity', dur=11.0, cap='A city of unfinished repos. Last commits months ago. Then one gets finished.', p=dict(), energy=1),
            dict(type='vtype', dur=3.0, cap='One finished project beats seven started.', p=dict(lines=['ONE *FINISHED', 'BEATS SEVEN', '_STARTED.']), energy=3, drop=True),
            dict(type='vcta', dur=2.8, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Finish the building.'), energy=1)],
    ig="Welcome to your GitHub skyline: seven buildings, all under scaffolding.\n\nStarting is exciting. Finishing is what interviewers can talk to you about.\n\nPlaciq's Project Builder breaks projects into checkpoints you can actually complete. learn.placiq.in",
    tags=['#github', '#sideprojects', '#developers', '#placiq'], yt='The City of Abandoned Repos', li='Unfinished projects are common. Checkpointed scope helps students complete one end to end.')

day(25, title='Blank Editor Fear', pillar='Projects', fmt='narrated', style='minimal', root=47, pal=WHITE, voice='af_heart', speed=1.05,
    hooks=['untitled.py. Cursor blinking. Panic rising.', 'Where do you even start a project?', 'Turn a blank file into a plan in 15 seconds.'],
    scenes=[dict(type='vblank', say="A blank editor is scary because it has no shape. Give it one. Sketch the parts: client, A P I, auth, database. Then split it into four milestones, and finish milestone one.", cap="A blank editor is scary because it has no shape. Sketch the parts. Split into milestones. Finish milestone one.", p=dict(), energy=2),
            dict(type='vcta', say="Plan it. Then build it. With Place IQ.", cap="Plan it. Then build it. With Placiq.", p=dict(v='stack', words=['PLAN IT.', 'BUILD IT.', 'SHIP IT.']), energy=1, hold=1, drop=True)],
    ig="untitled.py and a blinking cursor. We have all frozen here.\n\nGive the blank file a shape: sketch the components, split into milestones, finish milestone one.\n\nPlaciq's Project Builder turns ideas into guided modules. learn.placiq.in",
    tags=['#coding', '#projectplanning', '#softwaredesign', '#placiq'], yt='How to Beat Blank Editor Fear', li='A simple method for starting projects: sketch architecture, define milestones, complete the first one.')

day(26, title='From Idea to Implementation', pillar='Projects', fmt='music', style='house', root=50, pal=BLUE,
    hooks=['Idea to tests, in one scroll.', 'Requirements first. Code fourth.', 'The path every real project takes.'],
    scenes=[dict(type='vflow', dur=9.0, cap='Requirements -> Architecture -> Modules -> Implementation -> Tests.', p=dict(), energy=2),
            dict(type='vclip', dur=5.0, cap='Real Project Builder: guided modules and a live editor.', p=dict(clip='editor', pan=((0, .1), (.7, .4)), cw=.5, title='Guided, module by module.'), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Idea to implementation.'), energy=1)],
    ig="Requirements, architecture, modules, implementation, tests. In that order.\n\nMost unfinished projects skip the first two steps. Placiq's Project Builder walks you through each module with a live editor.\n\nlearn.placiq.in",
    tags=['#softwareengineering', '#projects', '#buildinpublic', '#placiq'], yt='Idea to Tests in 5 Steps', li='The stages of a real software project, visualised, and how guided building follows them.')

day(27, title='The AI That Asks First', pillar='Projects', fmt='narrated', style='funk', root=45, pal=PAPER, voice='af_heart', speed=1.06,
    hooks=['What if your AI asked you questions first?', 'A tutor that does not just dump code.', 'Three questions before one line of code.'],
    scenes=[dict(type='vasks', say="Most AI dumps code. A good tutor asks first. Who uses it? What breaks first? How will you test it? Then it checks your answer, checkpoint by checkpoint.", cap="Most AI dumps code. A good tutor asks first: who uses it, what breaks first, how will you test it. Then checks you, checkpoint by checkpoint.", p=dict(), energy=2),
            dict(type='vtype', say="Answers you build stick.", cap="Answers you build stick.", p=dict(lines=['ANSWERS YOU', '*BUILD', 'STICK.'], slam=True), energy=3, drop=True),
            dict(type='vcta', say="The Socratic way, in Place IQ.", cap="The Socratic way, in Placiq.", p=dict(v='logo', tag='It asks before it tells.'), energy=1, hold=1)],
    ig="What if your AI tutor asked you questions before giving answers?\n\nWho uses it? What breaks first? How will you test it? Reasoning it out yourself is what makes it stick in an interview.\n\nPlaciq's tutors guide with questions and checkpoints. learn.placiq.in",
    tags=['#socraticmethod', '#ai', '#learning', '#placiq'], yt='The AI Tutor That Asks First', li='Guided questioning builds understanding that code dumps do not. A look at checkpoint-based tutoring.')

day(28, title='Project Builder Hero Film', pillar='Projects', fmt='narrated', style='electro', root=44, pal=INK, voice='am_michael', speed=1.05,
    hooks=['From a project idea to evidence, in real footage.', 'This is the AI Project Builder.', 'Build it. Prove it.'],
    scenes=[dict(type='vreel', say="Pick a scoped project from the catalog. Open it in the I D E. Work through guided modules, with a tutor that knows your code. Then the analyzer reads the result like a reviewer would.", cap="Pick a scoped project. Open it in the IDE. Work through guided modules with a project-aware tutor. Then the analyzer reviews the result.", p=dict(clips=[('builder', (0, .1), (.4, .3), .5), ('editor', (0, 0), (.4, .3), .5), ('editor', (.15, .15), (.45, .3), .45), ('analyzer', (0, .1), (.6, .3), .5)], labels=['PICK A PROJECT', 'OPEN THE IDE', 'GUIDED MODULES', 'GET IT REVIEWED']), energy=3, drop=True),
            dict(type='vcta', say="The A I Project Builder. In Place IQ.", cap="The AI Project Builder, in Placiq.", p=dict(v='logo', tag='Evidence-backed shipping.'), energy=1, hold=1)],
    ig="From idea to evidence, in real product footage.\n\nPick a scoped project, open it in the IDE, work through guided modules with a tutor that knows your code, then get it reviewed by the Project Analyzer.\n\nGuided Project Builder modules are part of Placiq Pro. learn.placiq.in",
    tags=['#projectbuilder', '#ai', '#coding', '#placiq'], yt='AI Project Builder: Real Footage', li="A walkthrough of Placiq's AI Project Builder: catalog, IDE, guided modules and project analysis.")

# ================================================================ WEEK 5 - RESUME
day(29, title='Resume Claim vs Proof', pillar='Resume', fmt='narrated', style='breakbeat', root=46, pal=WHITE, voice='am_puck', speed=1.08,
    hooks=['"Built a scalable app." Prove it.', 'Every resume line is a claim.', 'Can you back up bullet two?'],
    scenes=[dict(type='vres', say="Built a scalable expense app. Okay, prove it. Link the repo, the tests, the architecture, the live demo, and the before and after numbers you actually measured.", cap="\"Built a scalable expense app.\" Prove it: repo, tests, architecture, live demo, numbers you actually measured.", p=dict(mode='claim'), energy=2),
            dict(type='vtype', say="Claims get questioned. Proof gets discussed.", cap="Claims get questioned. Proof gets discussed.", p=dict(lines=['CLAIMS GET', '_QUESTIONED.', '*PROOF GETS', 'DISCUSSED.']), energy=3, drop=True),
            dict(type='vcta', say="Back your resume with Place IQ.", cap="Back your resume with Placiq.", p=dict(v='logo', tag='Show the work.'), energy=1, hold=1)],
    ig="\"Built a scalable expense app.\" Can you prove it?\n\nEvery resume bullet is a claim. Link it to a repo, tests, a write-up, a demo, and numbers you actually measured.\n\nPlaciq connects your projects and GitHub to your resume. learn.placiq.in",
    tags=['#resume', '#resumetips', '#projects', '#placiq'], yt='Resume Claim vs Proof', li='Resume claims are stronger when linked to verifiable artifacts: repositories, tests and measured results.')

day(30, title='The Generic Resume Machine', pillar='Resume', fmt='comedy', style='industrial', root=40, pal=MONO,
    hooks=['Insert student. Receive "hardworking team player".', 'The resume factory has one template.', 'Why does every bullet sound the same?'],
    scenes=[dict(type='vfactory', dur=9.0, cap='Different students in. "Hardworking team player with good communication skills" out.', p=dict(machine='RESUME-O-TRON', output='Hardworking team player with good communication skills', inputs=['Riya: built a bus tracker', 'Kabir: led hackathon team', 'Meera: ML on crop data', 'Arjun: fixed college site'], verdict='Real stories in. Same bullet out.'), energy=2),
            dict(type='vtype', dur=3.0, cap='Your bullet should only fit you.', p=dict(lines=['A BULLET SHOULD', '*ONLY FIT', 'YOU.']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Write your own bullets.'), energy=1)],
    ig="Insert student. Receive \"hardworking team player\".\n\nTemplates flatten real stories. A bus tracker, a hackathon win and an ML project should not all become the same sentence.\n\nPlaciq's Resume Intelligence flags generic bullets and gaps. learn.placiq.in",
    tags=['#resume', '#careertips', '#freshers', '#placiq'], yt='The Generic Resume Machine', li='Generic phrasing hides distinct experience. Specific, evidence-based bullets communicate more.')

day(31, title='The Three-Second Resume', pillar='Resume', fmt='music', style='minimal', root=48, pal=PAPER,
    hooks=['Where does the eye go on your resume?', 'Messy resume vs clear resume, eye-tracked (fictional).', 'Hierarchy is a skill.'],
    scenes=[dict(type='vres', dur=10.0, cap='A cluttered layout scatters attention. Clear hierarchy guides the eye.', p=dict(mode='scan'), energy=2),
            dict(type='vtype', dur=3.0, cap='Make the important thing obvious.', p=dict(lines=['MAKE THE', 'IMPORTANT THING', '*OBVIOUS.']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - resume.placiq.in', p=dict(v='logo', tag='Readable at a glance.', url='resume.placiq.in'), energy=1)],
    ig="Where does the eye go on your resume?\n\nNo single rule decides how long a reviewer looks, but a clear hierarchy helps anyone find what matters fast: role, impact, proof.\n\nCheck yours with Placiq Resume Intelligence. resume.placiq.in",
    tags=['#resume', '#resumedesign', '#freshers', '#placiq'], yt='Resume Hierarchy in 15 Seconds', li='Visual hierarchy helps any reviewer find key information quickly. A fictional before/after.')

day(32, title='ATS Confusion', pillar='Resume', fmt='narrated', style='glitchhop', root=41, pal=TERM, voice='am_michael', speed=1.05,
    hooks=['Keyword stuffing, as seen by a parser.', 'You added 40 keywords. Now nobody can read it.', 'More keywords is not more relevant.'],
    scenes=[dict(type='vres', say="Stuff every keyword in, and your real experience disappears under a wall of buzzwords. People still read the resume after the parser does.", cap="Stuff every keyword in, and your real experience disappears. People still read it after the parser does.", p=dict(mode='stuff', fix='Use the job\'s words, for skills you can prove.'), energy=2),
            dict(type='vtype', say="Use the job's words, for skills you can actually prove.", cap="Use the job's words, for skills you can actually prove.", p=dict(lines=["USE THE JOB'S", 'WORDS, FOR SKILLS', 'YOU CAN *PROVE.']), energy=3, drop=True),
            dict(type='vcta', say="Check it with Resume Intelligence.", cap="Check it with Placiq Resume Intelligence.", p=dict(v='logo', tag='Relevant, not stuffed.', url='resume.placiq.in'), energy=1, hold=1)],
    ig="Added 40 keywords. Now nobody can read your experience.\n\nMatch the job description's language for skills you genuinely have, and keep each one tied to a project or result. A human reads it after any parser.\n\nPlaciq Resume Intelligence reviews like an ATS and a recruiter would. resume.placiq.in",
    tags=['#ats', '#resumetips', '#jobsearch', '#placiq'], yt='Keyword Stuffing vs a Readable Resume', li='Keyword stuffing reduces readability. Align terminology with the role for skills backed by evidence.')

day(33, title='Your Project Deserves Better', pillar='Resume', fmt='narrated', style='house', root=49, pal=WHITE, voice='af_heart', speed=1.06,
    hooks=['"Worked on a web app project." Let\'s fix that.', 'One vague bullet, rewritten live.', 'Your project did more than this line says.'],
    scenes=[dict(type='vres', say="Worked on a web app project. That says nothing. Try: built a group ledger A P I with FastAPI and Postgres, wrote eighteen tests, deployed it. What, with what, and the proof.", cap="\"Worked on a web app project.\" Try: built a group-ledger API (FastAPI, Postgres), wrote 18 tests, deployed it.", p=dict(mode='rewrite'), energy=2),
            dict(type='vcta', say="Specific. Truthful. Provable. Place IQ.", cap="Specific. Truthful. Provable.", p=dict(v='stack', words=['SPECIFIC.', 'TRUTHFUL.', 'PROVABLE.']), energy=3, drop=True, hold=1)],
    ig="\"Worked on a web app project.\" Your project deserves better.\n\nSay what you built, with which tools, and link the proof. Only claim what you did.\n\nPlaciq pulls your project evidence straight into your resume. learn.placiq.in",
    tags=['#resumewriting', '#projects', '#cse', '#placiq'], yt='Rewrite One Vague Resume Bullet', li='Specific, truthful project descriptions with linked evidence communicate real contribution.')

day(34, title='Two Resumes, One Difference', pillar='Resume', fmt='music', style='funk', root=46, pal=INK,
    hooks=['Same student. Same internship. Two resumes.', 'Spot the difference.', 'Which one gets the follow-up question?'],
    scenes=[dict(type='vres', dur=10.0, cap='Same internship, same student. Resume B uses specifics and evidence.', p=dict(mode='compare'), energy=2),
            dict(type='vtype', dur=3.0, cap='Specifics invite better questions.', p=dict(lines=['SPECIFICS', 'INVITE BETTER', '*QUESTIONS.']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - resume.placiq.in', p=dict(v='logo', tag='Same work. Better story.', url='resume.placiq.in'), energy=1)],
    ig="Same student. Same internship. Two very different resumes.\n\nResume B is not exaggerating, it is specific: what was trained, what shipped, which tools.\n\nTry Placiq Resume Intelligence on yours. resume.placiq.in",
    tags=['#resume', '#internship', '#careertips', '#placiq'], yt='Two Resumes, One Difference', li='Two fictional presentations of identical experience. Specificity changes how it is read.')

day(35, title='Resume Intelligence Hero', pillar='Resume', fmt='narrated', style='electro', root=45, pal=BLUE, voice='am_michael', speed=1.05,
    hooks=['Real footage: a resume, analysed.', 'ATS view. Recruiter view. One report.', 'This is Resume Intelligence 2.0.'],
    scenes=[dict(type='vreel', say="Resume Intelligence two point oh. Upload your resume. Get an A T S scan and a recruiter-style rubric. See classified skills, gaps, and a report you can act on.", cap="Resume Intelligence 2.0: upload, ATS scan + recruiter-style rubric, classified skills, gaps, an actionable report.", p=dict(clips=[('resume', (0, .1), (.4, .3), .5), ('resume', (.5, .2), (1, .5), .45), ('resume_report', (0, .1), (.5, .3), .5), ('resume_report', (.5, .2), (1, .5), .45)], labels=['UPLOAD', 'ATS + RECRUITER', 'SKILLS + GAPS', 'ACT ON IT']), energy=3, drop=True),
            dict(type='vcta', say="Try it at resume dot place I Q dot in.", cap="Try it at resume.placiq.in", p=dict(v='logo', tag='Resume Intelligence 2.0', url='resume.placiq.in'), energy=1, hold=1)],
    ig="Your resume, read two ways: by an ATS and by a recruiter-style rubric.\n\nReal footage of Placiq Resume Intelligence 2.0: upload, scan, see classified skills and gaps, then act on the report.\n\nFree plan includes a basic ATS scan. resume.placiq.in",
    tags=['#resumeintelligence', '#ats', '#ai', '#placiq'], yt='Resume Intelligence 2.0: Real Footage', li='A walkthrough of Placiq Resume Intelligence 2.0: ATS scan, recruiter rubric, skill classification and gaps.')

# ================================================================ WEEK 6 - GITHUB + EVIDENCE
day(36, title='Green Square Anxiety', pillar='GitHub evidence', fmt='music', style='trap', root=43, pal=INK,
    hooks=['365 green squares. So what?', 'Your contribution graph is not your portfolio.', 'Green does not explain anything.'],
    scenes=[dict(type='vgrid', dur=9.0, cap='365 green squares. What matters: what you built, why, what broke, can someone run it.', p=dict(), energy=2),
            dict(type='vclip', dur=4.5, cap='Placiq GitHub evidence: repos and commits as proof.', p=dict(clip='github', pan=((0, 0), (.6, .4)), cw=.5, title='Evidence, not squares.'), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Depth over green.'), energy=1)],
    ig="365 green squares and still anxious?\n\nThe contribution graph counts activity. Interviewers ask what you built, why you designed it that way, and what broke.\n\nPlaciq turns repos and commits into explainable evidence. learn.placiq.in",
    tags=['#github', '#opensource', '#developers', '#placiq'], yt='Green Squares Are Not a Portfolio', li='Contribution counts measure activity, not depth. Evidence of design decisions matters more.')

day(37, title='Projects Are Receipts', pillar='GitHub evidence', fmt='narrated', style='breakbeat', root=47, pal=PAPER, voice='am_puck', speed=1.08,
    hooks=['Your project should print a receipt.', 'Itemised proof of what you built.', 'Total: evidence.'],
    scenes=[dict(type='vreceipt', say="A good project prints a receipt. An architecture doc. Sixty-one commits. Eighteen passing tests. Seven logged decisions. Twelve fixed bugs. One live demo.", cap="A good project prints a receipt: architecture doc, 61 commits, 18 tests, 7 decisions, 12 bugs fixed, 1 live demo.", p=dict(), energy=2),
            dict(type='vcta', say="Keep the receipts. Place IQ.", cap="Keep the receipts.", p=dict(v='stack', words=['KEEP', 'THE', 'RECEIPTS.']), energy=3, drop=True, hold=1)],
    ig="Your project should come with a receipt.\n\nArchitecture notes, commits, tests, decisions, fixed bugs, a live demo. Itemised proof is easier to discuss than a one-line description.\n\nPlaciq collects that evidence as you build. learn.placiq.in",
    tags=['#projects', '#github', '#softwareengineering', '#placiq'], yt='Projects Are Receipts', li='Treat projects as itemised evidence: architecture, commits, tests and decisions.')

day(38, title='The README Test', pillar='GitHub evidence', fmt='music', style='arcade', root=50, pal=WHITE,
    hooks=['final2.py, test (1).py, README (empty).', 'Can a stranger run your repo in 60 seconds?', 'The README glow-up.'],
    scenes=[dict(type='vreadme', dur=9.5, cap='Messy repo -> README: what it is, how to run it, how it works, decisions, tests.', p=dict(), energy=2),
            dict(type='vtype', dur=3.0, cap='If they cannot run it, they cannot see it.', p=dict(lines=["IF THEY CAN'T", 'RUN IT,', "THEY CAN'T *SEE IT."]), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Document the work.'), energy=1)],
    ig="final2.py, test (1).py, and an empty README.\n\nA five-section README (what, run, how, decisions, tests) makes your repo understandable in a minute.\n\nPlaciq's GitHub evidence view rewards depth like this. learn.placiq.in",
    tags=['#readme', '#github', '#documentation', '#placiq'], yt='The README Test', li='Documentation is part of the work. A five-section README template, visualised.')

day(39, title='Certificate Mountain', pillar='GitHub evidence', fmt='narrated', style='cinematic', root=40, pal=PAPER, voice='af_heart', speed=1.04,
    hooks=['Twenty-six certificates. One question: can you build it?', 'Certificates are a start, not the finish.', 'The mountain vs the demo.'],
    scenes=[dict(type='vmountain', say="Certificates are real learning, and they matter. But next to them, one working demo answers the question every interviewer has: can you build it?", cap="Certificates are real learning, and they matter. But one working demo answers: can you build it?", p=dict(), energy=1),
            dict(type='vtype', say="Learn it. Then show it.", cap="Learn it. Then show it.", p=dict(lines=['LEARN IT.', '*SHOW IT.'], slam=True), energy=3, drop=True),
            dict(type='vcta', say="Turn learning into proof with Place IQ.", cap="Turn learning into proof with Placiq.", p=dict(v='logo', tag='Learning, then proof.'), energy=1, hold=1)],
    ig="26 certificates and one question: can you build it?\n\nCertificates represent real learning. Pair them with one working demo and the conversation changes.\n\nPlaciq helps turn what you learned into a project you can show. learn.placiq.in",
    tags=['#certifications', '#learning', '#portfolio', '#placiq'], yt='Certificate Mountain vs One Demo', li='Certificates show learning; working demonstrations show applied skill. Both have value.')

day(40, title='The Evidence Trail', pillar='GitHub evidence', fmt='music', style='house', root=45, pal=BLUE,
    hooks=['Follow the trail from practice to proof.', 'Every step leaves evidence.', 'DSA to design, connected.'],
    scenes=[dict(type='vtrail', dur=10.0, cap='DSA practice -> project milestone -> commit -> tests -> resume bullet -> mock interview.', p=dict(), energy=2),
            dict(type='vtype', dur=3.0, cap='Connected steps become a story.', p=dict(lines=['CONNECTED STEPS', 'BECOME A', '*STORY.']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='stack'), energy=1)],
    ig="Practice, milestone, commit, tests, resume bullet, mock interview.\n\nWhen each step links to the next, your preparation becomes a story you can explain.\n\nThat is what Placiq connects. learn.placiq.in",
    tags=['#careerprep', '#evidence', '#students', '#placiq'], yt='The Evidence Trail', li='Linking practice, project milestones and outcomes creates a coherent, explainable preparation record.')

day(41, title='Interview Proof', pillar='GitHub evidence', fmt='narrated', style='industrial', root=42, pal=MONO, voice='am_michael', speed=1.05,
    hooks=['"Why did you add a queue here?"', 'Rewind your own commits in an interview.', 'The best answer is in your git log.'],
    scenes=[dict(type='vrewind', say="Why did you add a queue here? Aarav, a fictional candidate, rewinds his own history. Initial A P I. A benchmark: two point four seconds. A duplicate-charge bug. Then the retry queue. He doesn't recite. He remembers.", cap="\"Why add a queue?\" Aarav (fictional) rewinds his own history: benchmark, a duplicate-charge bug, then the retry queue.", p=dict(), energy=2),
            dict(type='vcta', say="Build work you can explain. Place IQ.", cap="Build work you can explain.", p=dict(v='logo', tag='Work you can explain.'), energy=3, drop=True, hold=1)],
    ig="\"Why did you add a queue here?\"\n\nWhen you actually built it, the answer is in your own history: the benchmark, the bug, the decision.\n\nPlaciq's guided projects keep that trail. learn.placiq.in",
    tags=['#interviewprep', '#systemdesign', '#git', '#placiq'], yt='The Best Interview Answer Is in Your Git Log', li='Candidates who built their projects can reconstruct decisions from history. A fictional example.')

day(42, title='Skill Passport', pillar='GitHub evidence', fmt='music', style='electro', root=48, pal=INK,
    hooks=['Stamp by stamp, a readiness record.', 'Your skills, passport-verified.', 'One living record of your prep.'],
    scenes=[dict(type='vpassport', dur=8.0, cap='DSA, project, resume, GitHub, mock: stamps in one living readiness record.', p=dict(), energy=2),
            dict(type='vclip', dur=4.5, cap='Real Skill Passport in Placiq.', p=dict(clip='passport', pan=((0, 0), (.6, .4)), cw=.5, title='Skill Passport.'), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='One living record.'), energy=1)],
    ig="Stamp by stamp: DSA, projects, resume, GitHub, mock interviews.\n\nPlaciq's Skill Passport is one living readiness score across everything you have practised and shipped.\n\nlearn.placiq.in",
    tags=['#skillpassport', '#readiness', '#placementprep', '#placiq'], yt='Skill Passport: One Living Record', li="Placiq's Skill Passport combines evidence from multiple modules into one readiness record.")

# ================================================================ WEEK 7 - CAREER DIRECTION
day(43, title='AI Engineer or Data Scientist?', pillar='Career direction', fmt='narrated', style='minimal', root=47, pal=WHITE, voice='af_heart', speed=1.05,
    hooks=['AI engineer or data scientist? They share more than you think.', 'Two roles, one skill map.', 'Stop picking roles by job title.'],
    scenes=[dict(type='vroles', say="AI engineer or data scientist? Both need Python and linear algebra. One leans into L L M A P Is, M L ops and system design. The other into statistics, S Q L and experiment design.", cap="AI engineer or data scientist? Both need Python and linear algebra. One leans to LLM APIs, MLOps, system design; the other to statistics, SQL, experiments.", p=dict(), energy=2),
            dict(type='vclip', say="Career Navigator maps the skills a role needs, and what to learn next.", cap="Career Navigator maps the skills a role needs, and what to learn next.", p=dict(clip='navigator', pan=((0, 0), (.6, .3)), cw=.5, title='Map your role.'), energy=3, drop=True),
            dict(type='vcta', say="Choose with clarity. Place IQ.", cap="Choose with clarity.", p=dict(v='logo', tag='Choose with clarity.'), energy=1, hold=1)],
    ig="AI engineer or data scientist? They overlap more than the titles suggest.\n\nBoth lean on Python and linear algebra. AI engineering adds LLM APIs, MLOps and system design; data science adds statistics, SQL and experiment design.\n\nPlaciq's Career Navigator maps which skills each role needs. learn.placiq.in",
    tags=['#aiengineer', '#datascience', '#careerpath', '#placiq'], yt='AI Engineer vs Data Scientist: Skill Map', li='A simplified view of overlapping and distinct skills between AI engineering and data science roles.')

day(44, title='The Random Roadmap', pillar='Career direction', fmt='music', style='breakbeat', root=44, pal=PAPER,
    hooks=['Flutter, Rust, Figma, Kafka... for which job?', 'Your skill list has no destination.', 'Pick the role, then the skills.'],
    scenes=[dict(type='vsort', dur=9.0, cap='Random skills pile up. Pick a role, and they sort into NOW and LATER.', p=dict(), energy=2),
            dict(type='vtype', dur=3.0, cap='Role first. Skills second.', p=dict(lines=['*ROLE FIRST.', 'SKILLS SECOND.'], slam=True), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='A roadmap with a destination.'), energy=1)],
    ig="Flutter, Rust, Figma, Kafka, Unity... for which job?\n\nPick a target role first, and your skill list sorts itself into now and later.\n\nPlaciq's Career Navigator does that sorting with you. learn.placiq.in",
    tags=['#roadmap', '#careerclarity', '#techskills', '#placiq'], yt='The Random Roadmap Problem', li='Skills accumulate without direction. Anchoring learning to a target role creates priorities.')

day(45, title='What Should I Learn Next?', pillar='Career direction', fmt='narrated', style='house', root=50, pal=INK, voice='am_puck', speed=1.07,
    hooks=['Kubernetes? LLMs? Rust? Stop.', 'The answer is three things, not thirty.', 'Your next three steps, ranked.'],
    scenes=[dict(type='vcloud', say="Kubernetes. L L Ms. Rust. Everything looks urgent. But your next step should come from your gaps and your role. Maybe just three things: graphs, S Q L joins, and finishing milestone two.", cap="Kubernetes. LLMs. Rust. Everything looks urgent. Your next step should come from your gaps and your role: maybe just three things.", p=dict(), energy=2),
            dict(type='vcta', say="Three things. Not thirty. Place IQ.", cap="Three things. Not thirty.", p=dict(v='stack', words=['THREE', 'THINGS.', 'NOT THIRTY.']), energy=3, drop=True, hold=1)],
    ig="Kubernetes? LLMs? Rust? Everything feels urgent.\n\nYour next step should come from your actual gaps and your target role, and it is usually two or three things, not thirty.\n\nPlaciq prioritises what to learn next from your own progress. learn.placiq.in",
    tags=['#whattolearn', '#programming', '#focus', '#placiq'], yt='What Should I Learn Next? (3 Things)', li='Prioritisation beats breadth. Turning an overwhelming learning landscape into ranked next steps.')

day(46, title='LinkedIn Comparison Mode', pillar='Career direction', fmt='comedy', style='funk', root=46, pal=PAPER,
    hooks=['"Thrilled to announce I woke up at 4 AM."', 'Your feed at 1 AM during placement season.', 'A completely realistic feed (all fictional).'],
    scenes=[dict(type='vfeed', dur=10.0, cap='A (fictional) feed of impossible achievements. Compare with last-month you instead.', p=dict(), energy=2),
            dict(type='vtype', dur=3.0, cap='Your only fair benchmark: past you.', p=dict(lines=['YOUR ONLY FAIR', 'BENCHMARK:', '*PAST YOU.']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Track your own progress.'), energy=1)],
    ig="\"Thrilled to announce my cat merged a PR to the Linux kernel.\" (fictional, obviously)\n\nHighlight reels are not progress reports. The only fair comparison is you, last month.\n\nPlaciq tracks your own readiness over time. learn.placiq.in",
    tags=['#linkedin', '#comparison', '#studentlife', '#placiq'], yt='LinkedIn Comparison Mode (Fictional Feed)', li='A humorous look at comparison culture, and why tracking personal progress is healthier.')

day(47, title='College Deadline Multiverse', pillar='Career direction', fmt='music', style='industrial', root=39, pal=MONO,
    hooks=['Every deadline lands on the same Wednesday.', 'The calendar collapse.', 'Assignment + OA + review + mid-sem = Wednesday.'],
    scenes=[dict(type='vcal', dur=9.0, cap='Assignment, OA, project review, TPO resume deadline: all on the same Wednesday.', p=dict(), energy=2),
            dict(type='vtype', dur=3.0, cap='You cannot move deadlines. You can see them coming.', p=dict(lines=["YOU CAN'T MOVE", 'DEADLINES.', '*SEE THEM COMING.']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Plan the week, not the panic.'), energy=1)],
    ig="Somehow every deadline lands on the same Wednesday.\n\nAssignments, an OA, a project review and a resume deadline. You cannot move them, but you can see them coming and plan small daily steps.\n\nPlaciq's daily quests keep prep moving in busy weeks. learn.placiq.in",
    tags=['#collegelife', '#deadlines', '#engineering', '#placiq'], yt='When Every Deadline Is Wednesday', li='Academic and placement deadlines collide. Small daily preparation steps reduce last-minute pressure.')

day(48, title="Don't Train for Every Role", pillar='Career direction', fmt='narrated', style='cinematic', root=41, pal=BLUE, voice='am_michael', speed=1.04,
    hooks=['Six paths. One you.', 'Training for every role means mastering none.', 'Depth beats breadth.'],
    scenes=[dict(type='vpaths', say="Web dev. M L. Data. DevOps. Android. Security. Train for all six and you'll be shallow in each. Pick one direction, go deep, and adjust as you learn.", cap="Web dev, ML, data, DevOps, Android, security. Train for all six and you stay shallow. Pick one, go deep, adjust as you learn.", p=dict(), energy=2),
            dict(type='vcta', say="Find your focus with Place IQ.", cap="Find your focus with Placiq.", p=dict(v='logo', tag='Depth beats breadth.'), energy=3, drop=True, hold=1)],
    ig="Six career paths. One you.\n\nPreparing for every role at once spreads effort thin. Choose a direction, go deep, and reassess as you learn.\n\nPlaciq's Career Navigator helps you pick and plan a focus. learn.placiq.in",
    tags=['#careerfocus', '#techcareers', '#students', '#placiq'], yt="Don't Train for Every Role", li='Focused preparation for one target role tends to produce deeper, more demonstrable skill.')

day(49, title='Career Navigator Hero', pillar='Career direction', fmt='music', style='electro', root=45, pal=INK,
    hooks=['Real footage: role, skills, next steps.', 'This is Career Navigator.', 'Know which role fits.'],
    scenes=[dict(type='vtype', dur=2.0, cap='Which role fits you?', p=dict(lines=['WHICH ROLE', '*FITS YOU?'], slam=True), energy=2),
            dict(type='vreel', dur=11.0, cap='Real Career Navigator: pick a role, see its roadmap and skill gaps, get next actions.', p=dict(clips=[('navigator', (0, .1), (.4, .3), .5), ('navigator', (.5, .2), (1, .4), .45), ('roadmap', (0, .1), (.5, .3), .5), ('roadmap', (.4, .3), (1, .5), .45)], labels=['PICK A ROLE', 'SEE THE GAP', 'ROLE ROADMAP', 'NEXT ACTIONS']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Career Navigator'), energy=1)],
    ig="Which role fits you, which skills does it need, and what should you learn next?\n\nReal footage of Placiq's Career Navigator: role roadmaps, skill gaps and next actions.\n\nlearn.placiq.in",
    tags=['#careernavigator', '#careerplanning', '#tech', '#placiq'], yt='Career Navigator: Real Footage', li="A look at Placiq's Career Navigator: role fit, required skills and next steps.")

# ================================================================ WEEK 8 - CONNECTED OS
day(50, title='The Broken Workflow', pillar='Connected OS', fmt='music', style='glitchhop', root=42, pal=INK,
    hooks=['Watch your context fall through the cracks.', 'Five handoffs. Five drops.', 'Where does your progress go?'],
    scenes=[dict(type='vpacket', dur=10.0, cap='Your context drops at every tool handoff. Connected, it flows through.', p=dict(), energy=2),
            dict(type='vtype', dur=3.0, cap='Stop being the glue between your tools.', p=dict(lines=['STOP BEING', 'THE *GLUE.']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='stack'), energy=1)],
    ig="Watch your context fall through the cracks between tools.\n\nEvery handoff from a DSA site to notes to an AI chat to your resume loses something.\n\nIn Placiq, one context flows through every module. learn.placiq.in",
    tags=['#workflow', '#productivity', '#careeros', '#placiq'], yt='The Broken Prep Workflow', li='Information loss between disconnected tools, visualised, and what a connected flow looks like.')

day(51, title='One Student, Many Systems', pillar='Connected OS', fmt='narrated', style='trap', root=46, pal=PAPER, voice='af_heart', speed=1.06,
    hooks=['Five tools. Five different versions of you.', 'Which Aarav is real?', 'Your tools disagree about you.'],
    scenes=[dict(type='vconflict', say="Meet Aarav, a fictional student. His D S A site says beginner. His course app says advanced. His AI chat asks who he is. Five tools, five different Aaravs.", cap="Meet Aarav (fictional). DSA site: beginner. Course app: advanced. AI chat: who are you? Five tools, five different Aaravs.", p=dict(), energy=2),
            dict(type='vtype', say="One student deserves one source of truth.", cap="One student deserves one source of truth.", p=dict(lines=['ONE STUDENT.', 'ONE SOURCE', 'OF *TRUTH.']), energy=3, drop=True),
            dict(type='vcta', say="Place IQ. Your work, connected.", cap="Placiq. Your work, connected.", p=dict(v='logo'), energy=1, hold=1)],
    ig="Five tools, five different versions of the same student.\n\nWhen every app tracks you separately, none of them sees the whole picture.\n\nPlaciq keeps one connected profile across DSA, projects, resume and goals. learn.placiq.in",
    tags=['#edtech', '#students', '#careerprep', '#placiq'], yt='Five Tools, Five Versions of You', li='Fragmented systems create conflicting records of one learner. A fictional illustration.')

day(52, title='The Aarav Story', pillar='Connected OS', fmt='narrated', style='cinematic', root=40, pal=WHITE, voice='am_michael', speed=1.03,
    hooks=['Aarav started over. Again.', 'A fictional story about starting from zero, four times.', 'Week 1. Week 4. Week 9. Same start.'],
    scenes=[dict(type='vcomic', say="This is Aarav, a fictional student. Week one, a new DSA sheet. Week four, a new course. Week nine, a new project idea. Every restart felt like progress. None of it connected.", cap="Aarav (fictional). Week 1: new DSA sheet. Week 4: new course. Week 9: new project idea. Every restart felt like progress. None connected.", p=dict(panels=[('WEEK 1', 'New DSA sheet. Day 1 again.', 'DSA'), ('WEEK 4', 'New course. Starting from module 1.', 'COURSE'), ('WEEK 9', 'New project. Old one abandoned.', 'REPO'), ('WEEK 12', 'One workspace that remembers.', 'Placiq')]), energy=1),
            dict(type='vtype', say="Stop starting over. Start building on.", cap="Stop starting over. Start building on.", p=dict(lines=['STOP', '~STARTING OVER.', '*BUILD ON.']), energy=3, drop=True),
            dict(type='vcta', say="Place IQ remembers where you left off.", cap="Placiq remembers where you left off.", p=dict(v='logo', tag='Pick up where you left off.'), energy=1, hold=1)],
    ig="Aarav (fictional) started over four times in one semester.\n\nNew sheet, new course, new project. Each restart felt productive, but nothing built on anything.\n\nPlaciq remembers where you left off. learn.placiq.in",
    tags=['#studentstory', '#placementprep', '#consistency', '#placiq'], yt='The Aarav Story: Starting Over Again', li='A fictional narrative about repeated restarts in preparation, and the value of continuity.')

day(53, title='What Connected Really Means', pillar='Connected OS', fmt='narrated', style='house', root=48, pal=INK, voice='af_heart', speed=1.05,
    hooks=['"Connected" is not a buzzword. Here is what it means.', 'Real screens, real links.', 'How one module informs another.'],
    scenes=[dict(type='vreel', say="Connected means your Copilot sees your progress. Your Skill Passport scores across modules. Your resume is reviewed against your target role. And your projects carry the evidence.", cap="Connected means: the Copilot sees your progress, the Skill Passport scores across modules, the resume is reviewed for your role, projects carry the evidence.", p=dict(clips=[('copilot', (0, .1), (.4, .3), .5), ('passport', (0, 0), (.5, .3), .5), ('resume', (.3, .1), (.7, .4), .5), ('analyzer', (0, .1), (.5, .3), .5)], labels=['COPILOT SEES PROGRESS', 'PASSPORT SCORES ALL', 'RESUME FOR YOUR ROLE', 'PROJECTS = EVIDENCE']), energy=3, drop=True),
            dict(type='vcta', say="That's connected. Place IQ.", cap="That's connected.", p=dict(v='stack'), energy=1, hold=1)],
    ig="\"Connected\" should mean something specific.\n\nIn Placiq, the Copilot sees your progress, the Skill Passport scores across modules, your resume is reviewed against your target role, and projects carry evidence.\n\nReal screens, learn.placiq.in",
    tags=['#careeros', '#ai', '#product', '#placiq'], yt='What "Connected" Actually Means', li='A concrete look at how Placiq modules share context: Copilot, Skill Passport, Resume Intelligence and Project Analyzer.')

day(54, title='The Placiq Loop', pillar='Connected OS', fmt='narrated', style='electro', root=45, pal=BLUE, voice='am_puck', speed=1.06,
    hooks=['Seven steps. One loop. No finish line.', 'Diagnose to Reassess, animated.', 'Preparation is a loop, not a list.'],
    scenes=[dict(type='vloop7', say="Diagnose. Prioritize. Learn. Build. Evidence. Present. Reassess. Then go again, a little sharper every time.", cap="Diagnose. Prioritize. Learn. Build. Evidence. Present. Reassess. Then go again, a little sharper.", p=dict(), energy=3, drop=True),
            dict(type='vcta', say="The Place IQ loop.", cap="The Placiq loop.", p=dict(v='logo', tag='A loop, not a checklist.'), energy=1, hold=1)],
    ig="Diagnose. Prioritize. Learn. Build. Evidence. Present. Reassess. Repeat.\n\nPreparation is not a checklist you finish, it is a loop you get better at.\n\nThat loop is how Placiq is built. learn.placiq.in",
    tags=['#placiqloop', '#learning', '#growth', '#placiq'], yt='The Placiq Loop in 15 Seconds', li="Placiq's seven-step preparation loop: diagnose, prioritize, learn, build, evidence, present, reassess.")

day(55, title='From Fragments to Progress', pillar='Connected OS', fmt='music', style='dnb', root=43, pal=PAPER,
    hooks=['One shape. Four lives.', 'A tab becomes a passport.', 'Watch a fragment turn into progress.'],
    scenes=[dict(type='vmorph', dur=11.0, cap='A browser tab -> a practice card -> a connected node -> a readiness record.', p=dict(), energy=2),
            dict(type='vtype', dur=3.0, cap='Fragments become progress when they connect.', p=dict(lines=['FRAGMENTS', 'BECOME', '*PROGRESS.']), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='stack'), energy=1)],
    ig="A browser tab becomes a practice card, then a connected node, then a readiness record.\n\nThat is the whole idea: fragments only become progress when they connect.\n\nlearn.placiq.in",
    tags=['#motiondesign', '#progress', '#careeros', '#placiq'], yt='From Fragments to Progress', li='A continuous match-cut showing scattered preparation turning into a connected record.')

day(56, title='Placiq OS Reveal', pillar='Connected OS', fmt='narrated', style='house', root=50, pal=INK, voice='af_heart', speed=1.06,
    hooks=['Thirty-seven tabs become one OS.', 'Meet the career OS that remembers you.', 'Disconnected, then connected.'],
    scenes=[dict(type='vtabs', say="Thirty-seven tabs. Ten platforms. Zero memory.", cap="37 tabs. 10 platforms. Zero memory.", p=dict(n=37, seed=9), energy=1),
            dict(type='vtabs', say="Until it all connects.", cap="Until it all connects.", p=dict(n=37, merge=.05, seed=9, merged='PLACIQ OS'), energy=3, drop=True, tr='glitch'),
            dict(type='vreel', say="D S A that moves. Projects you finish. A resume backed by proof. A Copilot that remembers you.", cap="DSA that moves. Projects you finish. A resume backed by proof. A Copilot that remembers you.", p=dict(clips=[('dsa_run', (.25, .3), (.5, .5), .42), ('editor', (.1, .1), (.4, .3), .5), ('resume', (.3, .1), (.7, .4), .5), ('copilot', (.2, .1), (.6, .3), .5)], labels=['DSA THAT MOVES', 'PROJECTS YOU FINISH', 'RESUME WITH PROOF', 'COPILOT THAT REMEMBERS']), energy=3),
            dict(type='vcta', say="Place IQ. The career OS that remembers you.", cap="Placiq. The career OS that remembers you.", p=dict(v='logo', tag='The career OS that remembers you.'), energy=1, hold=1)],
    ig="37 tabs, 10 platforms, zero memory. Until it all connects.\n\nDSA that moves, projects you finish, a resume backed by proof and a Copilot that remembers you. One career OS.\n\nStart free: learn.placiq.in",
    tags=['#placiq', '#careeros', '#ai', '#placementprep'], yt='Placiq: The Career OS That Remembers You', li='A short product reveal: from disconnected preparation tools to one connected career OS.')

# ================================================================ BONUS 57-60
day(57, title='The No-Narration Masterpiece', pillar='Brand', fmt='music', style='dnb', root=45, pal=MONO,
    hooks=['No words. Just the work.', 'Turn the sound up.', 'A film in four movements.'],
    scenes=[dict(type='vtabs', dur=4.0, cap='37 tabs.', p=dict(n=37, seed=2), energy=1),
            dict(type='vmorph', dur=6.0, cap='Fragments connect.', p=dict(stages=[('tab', 'fragment'), ('node', 'connection'), ('passport', 'proof')]), energy=2),
            dict(type='vreel', dur=8.0, cap='Real Placiq footage: DSA, Project Builder, Resume, Skill Passport.', p=dict(clips=[('dsa_run', (.25, .3), (.5, .5), .42), ('editor', (.1, .1), (.4, .3), .5), ('resume_report', (0, .1), (.5, .3), .5), ('passport', (0, 0), (.5, .3), .5)], labels=['LEARN', 'BUILD', 'PROVE', 'PRESENT']), energy=3, drop=True),
            dict(type='vcta', dur=3.0, cap='Placiq. Your work, connected.', p=dict(v='stack'), energy=1)],
    ig="No narration. Turn the sound up.\n\nFrom 37 tabs to one connected record of your work, told in music, motion and real Placiq footage.\n\nlearn.placiq.in",
    tags=['#motiongraphics', '#brandfilm', '#placiq'], yt='Placiq: A Film Without Words', li='A music-led brand film: fragmented preparation to connected evidence, using real product footage.')

day(58, title='The Funniest Developer Reel', pillar='Brand', fmt='comedy', style='arcade', root=48, pal=TERM,
    hooks=['Me explaining code the AI wrote for me.', 'It compiled. I have no idea why.', 'Copy, paste, pray.'],
    scenes=[dict(type='vterm', dur=8.5, cap='Interviewer: "Walk me through this function." Me: (AI wrote it).', p=dict(title='interview.sh  -  live', lines=['$ ai "write rate limiter"', ('> 87 lines generated', 'muted'), '$ interviewer --ask', ('"Why a sliding window log?"', 'a2'), '$ me --answer', ('"...it was in the code"', 'a2'), '$ interviewer --followup', ('"What happens at scale?"', 'a2')], alert=('SEGFAULT (ME)', .8), cps=36), energy=2),
            dict(type='vasks', dur=8.0, cap='Understanding is when you can answer the follow-up.', p=dict(qs=[('Why a sliding window?', 'Fixed windows burst at edges'), ('Memory cost?', 'One timestamp per request'), ('At scale?', 'Move counts to Redis')], label='you can explain it now'), energy=3, drop=True),
            dict(type='vcta', dur=2.6, cap='Placiq - learn.placiq.in', p=dict(v='logo', tag='Understand it. Then ship it.'), energy=1)],
    ig="Me in the interview explaining code the AI wrote for me.\n\nGenerated answers pass the first question. Understanding passes the follow-up.\n\nPlaciq's Socratic tutors make you reason it through. learn.placiq.in",
    tags=['#developerhumor', '#ai', '#codinginterview', '#placiq'], yt='Explaining Code the AI Wrote', li='AI-generated code versus genuine understanding, a light-hearted look at the follow-up question.')

day(59, title='The Most Relatable Student Film', pillar='Brand', fmt='narrated', style='cinematic', root=38, pal=PAPER, voice='af_heart', speed=1.02,
    hooks=['She worked hard every single day. Why did it feel like nothing moved?', 'Effort everywhere. Progress nowhere.', 'A story about Meera (fictional).'],
    scenes=[dict(type='vcomic', say="Meera, a fictional student, studied every day. Videos in the morning. Problems at night. A project on weekends. Then the interview asked her to connect it all, and she couldn't.", cap="Meera (fictional) studied every day: videos, problems at night, a weekend project. Then the interview asked her to connect it all.", p=dict(panels=[('6 AM', 'Lecture videos before class.', 'VIDEO'), ('11 PM', 'Two more problems. Then two more.', 'DSA'), ('SUNDAY', 'Weekend project, half done.', 'REPO'), ('INTERVIEW', '"Tell me how it all fits together."', '?')]), energy=1),
            dict(type='vmeters', say="Her effort was real. It just wasn't connected.", cap="Her effort was real. It just wasn't connected.", p=dict(hours=9, prog=.35, l1='EFFORT', l2='CONNECTED PROGRESS', chips=['videos', 'problems', 'project', 'resume']), energy=2),
            dict(type='vcta', say="Place IQ. So your effort adds up.", cap="Placiq. So your effort adds up.", p=dict(v='logo', tag='So your effort adds up.'), energy=3, drop=True, hold=1.5)],
    ig="Meera (fictional) studied every day. Videos at 6 AM, problems at 11 PM, a project every weekend.\n\nThen an interviewer asked how it all fits together. Her effort was real; it just was not connected.\n\nPlaciq connects your work so effort adds up. learn.placiq.in",
    tags=['#studentlife', '#placementprep', '#relatable', '#placiq'], yt='Her Effort Was Real. It Just Wasn\'t Connected.', li='A fictional story about sustained effort without connection, and why connected preparation matters.')

day(60, title='The Flagship Launch Ad', pillar='Brand', fmt='narrated', style='house', root=50, pal=INK, voice='am_michael', speed=1.04,
    hooks=['Your career is a puzzle with pieces in ten different boxes.', 'Ten boxes. One picture.', 'What if every piece of your prep fit together?'],
    scenes=[dict(type='vorbit', say="Your career is a puzzle, with pieces in ten different boxes. D S A here. Projects there. A resume nobody's connected to anything.", cap="Your career is a puzzle with pieces in ten different boxes. DSA here. Projects there. A resume connected to nothing.", p=dict(hub=1.5, names=['DSA', 'Projects', 'Resume', 'GitHub', 'Courses', 'AI chat', 'Notes', 'Mock tests', 'Goals', 'Portfolio']), energy=1),
            dict(type='vorbit', say="Place IQ puts the pieces in one place, and remembers how they fit.", cap="Placiq puts the pieces in one place, and remembers how they fit.", p=dict(hub=.15, names=['DSA', 'Projects', 'Resume', 'GitHub', 'Courses', 'AI chat', 'Notes', 'Mock tests', 'Goals', 'Portfolio']), energy=3, drop=True),
            dict(type='vreel', say="Learn it. Build it. Prove it. Present it.", cap="Learn it. Build it. Prove it. Present it.", p=dict(clips=[('dsa_run', (.25, .3), (.5, .5), .42), ('editor', (.1, .1), (.4, .3), .5), ('resume_report', (0, .1), (.5, .3), .5), ('passport', (0, 0), (.5, .3), .5)], labels=['LEARN IT', 'BUILD IT', 'PROVE IT', 'PRESENT IT']), energy=3),
            dict(type='vcta', say="Place IQ. Your work, connected. Place I Q dot in.", cap="Placiq. YOUR WORK, CONNECTED. placiq.in", p=dict(v='stack', url='placiq.in', foot='https://placiq.in/'), energy=1, hold=1.5)],
    ig="Your career is a puzzle with pieces in ten different boxes.\n\nPlaciq puts DSA, projects, resume, GitHub and goals in one place, and remembers how they fit. Learn it, build it, prove it, present it.\n\nPlaciq. Your work, connected. https://placiq.in/",
    tags=['#placiq', '#yourworkconnected', '#careeros', '#placementprep'], yt='Placiq: Your Work, Connected', li='The flagship film for our 60-day series: Placiq, the AI-native Career Intelligence OS. Your work, connected.')
