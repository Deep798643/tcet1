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
