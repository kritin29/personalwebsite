"""All site content lives here. Edit this file, then run:   python tools/build.py

Each entry in EXPERIENCE / PROJECTS becomes a row on /software and its own page at
/software/<slug>. Keep every field short: a reviewer should get the idea in under a minute.

Fields
  slug        URL part: /software/<slug>
  title       Name shown as the heading
  oneliner    One sentence under the title (also used in the list row)
  hud         4 (label, value) pairs for the info panel under the title
  row_kind    Small text on the right of the list row (dates, or a category)
  row_meta    Second line in the list row (role · place)
  links       [(label, url)] shown under the panel; leave [] if none
  note        One line shown instead of / beside links (e.g. why code isn't public)
  shots       [(src, width, height, alt, caption)]; first one is the hero image
  thumb       Small image for the list row, or None
  flow        [(label, text)] steps for the "how it works" diagram, or []
  problem     2-3 sentences
  solution    2-3 sentences
  how         3-5 short bullets
  stats       [(value, label)] big numbers under Results
  takeaway    One sentence: an insight, not a summary
"""

SOFTWARE_INTRO = ("I build full-stack web applications and applied AI systems: database-backed platforms, "
                  "LLM pipelines, and developer tools.")

GAMES_INTRO = ("I design and build games in Unreal Engine 5 and Roblox, from fast aerial combat to "
               "enemies that adapt to how you play.")

EXPERIENCE = [
    dict(
        slug="ispace",
        title="Ispace Software Solutions",
        oneliner="A Chrome extension that automated insurance verification across three payer portals.",
        hud=[("Role", "Software Engineering Intern"), ("Dates", "May – Jul 2026"),
             ("Location", "Hyderabad, India"), ("Stack", "JavaScript · Chrome MV3")],
        row_kind="May – Jul 2026",
        row_meta="Software Engineering Intern · Hyderabad",
        links=[],
        note="The code is proprietary and the screens contain patient data, so neither is shown here.",
        shots=[], thumb=None,
        flow=[("Input", "Patient list"), ("Visit", "3 payer portals"), ("Extract", "Per-portal DOM extractors"),
              ("Normalize", "One JSON schema"), ("Match", "50-code reference set"), ("Output", "Verified coverage")],
        problem=("Staff verified each patient's insurance by hand, portal by portal. The three payer portals "
                 "present the same information in three different layouts, and the department handles "
                 "500+ patients a week."),
        solution=("A Chrome Manifest V3 extension that reads each portal, pulls out the coverage details, "
                  "and checks them automatically, inside the browser staff already use."),
        how=["Per-portal DOM extractors in JavaScript turn three inconsistent page structures into a single JSON schema.",
             "Each patient is matched against a 50-code insurance reference set.",
             "Runs on top of the staff's existing portal sessions, so there is no new system to log in to."],
        stats=[("85%", "less time per verification"), ("500+", "patients a week")],
        takeaway="Most of the work was normalization: three portals described the same coverage three different ways.",
    ),
    dict(
        slug="undergraduation",
        title="Undergraduation LLC",
        oneliner=("Sole developer of Undergraduation's student and parent portals: an AI-assisted "
                  "college-planning app on React 19 and Supabase."),
        hud=[("Role", "Software Engineer Intern, sole developer of the portals"), ("Dates", "Jan – Apr 2026"),
             ("Location", "Boston (Remote)"), ("Stack", "React 19 · Supabase · Gemini · Pinecone")],
        row_kind="Jan – Apr 2026",
        row_meta="Software Engineer Intern · Boston (Remote)",
        links=[("Live app", "https://undergrad-dashboard-app.vercel.app")],
        note="Screenshots show the real app running on demo data.",
        shots=[("/assets/undergraduation/colleges.webp", 1440, 900,
                "Student portal college explorer with saved colleges and compare",
                "Student portal: explore, filter, save, and compare colleges."),
               ("/assets/undergraduation/parent.webp", 1440, 900,
                "Parent portal with a roadmap, financial aid planner, and AI counselor",
                "Parent portal: roadmap, financial aid planning, and an AI counselor alongside."),
               ("/assets/undergraduation/activities.webp", 1440, 900,
                "Activities portfolio extracted from a resume into Common App format",
                "Activities: upload a resume and get Common App-style entries.")],
        thumb=("/assets/undergraduation/thumb.webp", 264, 165),
        flow=[("Onboard", "Grade, scores, majors, budget, regions"), ("Retrieve", "College data from a Pinecone index"),
              ("Match", "Weighted score: major, budget, region, SAT, size"), ("Counsel", "Gemini answers with the page as context"),
              ("Sync", "Parent portal updates live via Supabase Realtime")],
        problem=("Families juggle college lists, essays, activities, deadlines, and financial-aid paperwork across "
                 "scattered tools. Parents can't see progress without asking, and students struggle to fit their "
                 "experience into the Common App's tight formats."),
        solution=("Two linked portals on one Supabase backend. Students build their college list, essays, and "
                  "activities with Gemini's help; parents get a live view of that work plus their own financial-aid "
                  "planner, document vault, and shared calendar."),
        mine=("I was the only developer on the student and parent portals and wrote every commit, from the Supabase "
              "schema and security policies to the Gemini prompts."),
        how=["A parent account links to a student; six Supabase Realtime channels refresh the parent view whenever the student's colleges, essays, activities, calendar, or profile change.",
             "Row-level security with a security-definer helper lets parents read their student's rows without recursive policies.",
             "College data lives in a Pinecone index, with tuition, acceptance rate, test ranges, majors, and deadlines on each record; matches are ranked by a weighted score.",
             "Gemini powers the counselor, an essay writer, editor, and grader (with an AI-likelihood score), and resume parsing into structured activities, with a rule-based fallback when no key is set.",
             "Role-checked sign-in keeps students and parents in their own portals."],
        features=[
            ("Two portals", "Separate student and parent experiences with role-checked sign-in."),
            ("Student onboarding", "A wizard for grade, scores, majors, budget, regions, and campus size."),
            ("AI counselor", "Gemini chat with multiple conversations, history, and feedback."),
            ("College explorer", "Search, filters, grid and list views, details, save, and compare."),
            ("AI picks", "Ranked college matches with the reasons listed."),
            ("Essay studio", "Common App prompts with a Gemini writer, editor, and grader."),
            ("Activities builder", "A 10-slot Common App list with 150-character limits, filled from a resume PDF."),
            ("Parent onboarding", "Benchmarks, interests, finances and FAFSA status, strategy, and linking a student."),
            ("Parent roadmap", "Section-by-section progress with an always-open counselor."),
            ("Live student view", "Parents see tests, colleges, essays, and activities as they change."),
            ("Recommendations", "Parent picks appear on the student's list as recommended."),
            ("Shared calendar", "Deadlines with repeats; essay and activity dates added automatically."),
            ("Financial aid planner", "Budget, aid strategy, and cost and ROI per saved college, with risk labels."),
            ("Document vault", "Uploads in seven categories, with CSS Profile and FAFSA progress."),
            ("Test planner", "SAT, ACT, and GPA compared against target colleges."),
        ],
        stats_label="By the numbers",
        stats=[("500+", "universities in the college index")],
        takeaway="As the only developer, I owned every layer, from the database schema to the prompts.",
    ),
    dict(
        slug="the-strategist",
        title="The Strategist",
        oneliner="A model that predicts whether a candidate will accept a job offer, plus a reporting tool.",
        hud=[("Role", "Data Science Intern"), ("Dates", "Jun – Aug 2025"),
             ("Location", "Hyderabad, India"), ("Stack", "Python · scikit-learn · Streamlit")],
        row_kind="Jun – Aug 2025",
        row_meta="Data Science Intern · Hyderabad",
        links=[],
        note="The code and data are proprietary, so they aren't shown here.",
        shots=[], thumb=None,
        flow=[("Input", "Candidate data"), ("Model", "scikit-learn classifier"), ("Output", "Offer-acceptance prediction")],
        problem=("The team extended offers without a way to tell which candidates were likely to accept, and "
                 "Power BI reports only broke results down one variable at a time."),
        solution=("A classification model that predicts offer acceptance, and a Streamlit tool that turns "
                  "single-variable Power BI reports into multi-variable Excel outputs."),
        how=["Trained and evaluated a scikit-learn classifier on candidate data.",
             "Built a Streamlit app that converts single-variable Power BI reports into multi-variable Excel outputs."],
        stats=[("75%", "prediction accuracy")],
        takeaway="A model the team could understand and act on mattered more than squeezing out extra accuracy.",
    ),
]

PROJECTS = [
    dict(
        slug="syncinfra",
        title="SyncInfra",
        oneliner=("A site-tracking platform for office fit-out contractors that ties daily progress, materials, and "
                  "delays together, and explains why a handover date moved."),
        hud=[("Role", "Lead engineer, team of 2"), ("Built", "Sep – Oct 2026"),
             ("Client", "Office fit-out contractor"), ("Stack", "TypeScript · Fastify · Postgres · React")],
        row_kind="Full-stack · Client project",
        row_meta="Lead engineer · Team of 2 · Sep – Oct 2026",
        links=[],
        note="Client project in a private repository. Screenshots use the demo seed data, with company names replaced.",
        shots=[("/assets/syncinfra/delays.webp", 1440, 900,
                "Floor layout with progress rings, a delay chain explaining a slipped handover date, and open flags",
                "Why the handover date moved: a 30-day root cause rippling through every dependent stage."),
               ("/assets/syncinfra/sites.webp", 1440, 900,
                "Sites overview with progress, risk tiles, and setup checklists",
                "Sites overview: signed-off progress, forecast against target, and risk at a glance."),
               ("/assets/syncinfra/audit.webp", 1440, 900,
                "Job-by-job matrix with the auditor's stage drawer open",
                "Auditor view: claimed versus signed-off work, trade by trade, room by room."),
               ("/assets/syncinfra/shortages.webp", 1440, 900,
                "Shortage desk with materials waiting on a decision",
                "What is short: shortages from site and from the system, each waiting on a decision.")],
        thumb=("/assets/syncinfra/thumb.webp", 264, 165),
        flow=[("Report", "Site engineer claims progress on a stage"), ("Audit", "Auditor signs off, cuts, or rejects it"),
              ("Event", "The write commits a domain event"), ("Recompute", "A worker rebuilds the affected rollups"),
              ("Ripple", "The forecast shifts every dependent stage"), ("Act", "Dashboards raise flags, shortages, and order-by dates")],
        problem=("On fit-out projects, progress, material stock, and the programme live in separate spreadsheets, chats, "
                 "and meetings. Delays surface late, nobody can say which task caused them, claimed progress gets mixed "
                 "up with verified progress, and material runs short without warning."),
        solution=("One record runs floor → job → area → stage, and installation progress and material consumption are "
                  "the same dataset. Only work signed off by an independent auditor counts. Every write recomputes the "
                  "forecast and pushes a slipped date down the chain, so every delay has a named root cause."),
        how=["Business rules live in Postgres itself: CHECK constraints, foreign keys, and triggers. Computed tables refuse any write that doesn't come from the recompute pipeline.",
             "Audit independence is enforced by triggers: whoever claims progress can't approve it, the approver can't report to the claimant (checked up the reporting chain), and nobody can clear a flag raised against themselves.",
             "Event-driven recompute: each write appends a domain event, Postgres NOTIFY wakes a pg-boss worker, and only the affected rollups are rebuilt, in about 200 ms.",
             "Capability-based access: every API entry point goes through one deny-by-default permission check that logs denials, and screens a role can't use are never drawn.",
             "Every write records who and when; the API refuses to start against a database that's behind its migrations; and a pure engine package with enforced boundaries holds the scheduling logic."],
        features=[
            ("Sites overview", "Progress, forecast against target, material at risk, blockers, and a setup checklist per site."),
            ("Site setup gate", "A new site stays locked until its bill of quantities and drawings are uploaded."),
            ("Floors and flows", "Each floor as a room layout, a job-by-job matrix, or room by room."),
            ("Stage drawer", "Every trade's sub-steps, claimed versus approved, with the auditor's sign-off form."),
            ("Delay chains", "Why the handover date moved: root causes and the days they add, stage by stage."),
            ("Flags", "Auto-raised problems that can only be cleared with a stated reason."),
            ("Progress log", "Every claim and what became of it, filterable by state, trade, and person."),
            ("Materials", "Bill of quantities by trade with lead times, a sample tracker, and a materials log per floor."),
            ("Delivery", "Purchase orders through five delivery states, with goods received."),
            ("Shortage desk", "Shortages from site and from the system, resolved as a transfer or an order."),
            ("Outsourced works", "Execution vendors by trade and floor, with inspections and rejections."),
            ("Team and hierarchy", "Role slots, assignments from director to site, and the chain of command."),
            ("The programme", "Confirm suggested dependency links, or draw flow and parallel arrangements."),
            ("People directory", "Company-wide staff, invitations, password resets, availability, and deactivation."),
            ("Vendors and credit notes", "Material and crew vendors with lead times and capacity, and credit notes nearing expiry."),
            ("Sign-in", "Password login, emailed invitation and reset links, and a person switcher for demos."),
        ],
        stats_label="By the numbers",
        stats=[("906", "automated tests"), ("92", "API endpoints"), ("83", "database tables")],
        takeaway="Putting the rules in the database meant no screen, script, or future feature could quietly break them.",
    ),
    dict(
        slug="facultywise",
        title="FacultyWise",
        oneliner=("An AI grading co-pilot for professors: it pulls Canvas submissions, scores them against the "
                  "rubric with GPT-4o, and posts reviewed grades back."),
        hud=[("Role", "Full-stack engineer"), ("Team", "2 people"),
             ("Status", "Piloted with 5 professors"), ("Stack", "React · TypeScript · Supabase · OpenAI · Inngest")],
        row_kind="AI · Web",
        row_meta="Full-stack engineer · Team of 2 · 2026",
        links=[("Live app", "https://professor-one.vercel.app/")],
        note="The code lives in a private team repository. Screenshots show the real app running on demo data; I'm happy to walk through the code.",
        shots=[("/assets/facultywise/grader.webp", 1440, 900,
                "FacultyWise grader: student list with AI scores and confidence, the submission, and a scored rubric",
                "Grader: AI scores per rubric criterion, with confidence badges and one-click posting to Canvas."),
               ("/assets/facultywise/assistant.webp", 1440, 900,
                "Assistant drafting a rubric in the split-screen document canvas",
                "Assistant: drafts course material in an editable canvas, then sends it to Canvas."),
               ("/assets/facultywise/review.webp", 1440, 900,
                "A truncated submission flagged for review with an AI-drafted comment",
                "Review triage: an incomplete submission is flagged before anything is posted.")],
        thumb=("/assets/facultywise/thumb.webp", 264, 165),
        flow=[("Connect", "Canvas token, pasted or via the extension"), ("Sync", "Courses, assignments, rubrics, submissions"),
              ("Extract", "36 file types into text or images"), ("Grade", "GPT-4o scores every rubric criterion"),
              ("Review", "Professor edits scores and feedback"), ("Post", "Grade, comment, and rubric back to Canvas")],
        problem=("Professors grade large batches of Canvas submissions by hand, in every format from PDFs and scans to "
                 "slides, spreadsheets, code, and phone photos. Writing rubric-aligned feedback for each one is slow."),
        solution=("FacultyWise connects to a professor's Canvas account, turns every submission into something a model "
                  "can read, and has GPT-4o score each rubric criterion and write feedback in the professor's voice. "
                  "The professor reviews and edits, then posts back to Canvas in one click."),
        mine=("I built the grading engine and its 36-type file pipeline, the Inngest batch-grading queue, the Chrome "
              "extension, the integrations and encrypted OAuth token layer, and the database migrations behind them, "
              "plus most of the home dashboard and the AI assistant."),
        how=["Canvas connects by personal token or through a Chrome MV3 extension that creates one in a click; tokens are encrypted with a key held in Supabase Vault and only readable server-side.",
             "The file pipeline reads PDFs (with a vision fallback for scans), renders slides to images, turns spreadsheets into tables with formulas, and handles Word docs, code, and HEIC phone photos.",
             "Grading a class runs on Inngest: one durable job fans out an event per submission, graded three at a time, with a fallback step so a job can never hang.",
             "GPT-4o returns structured JSON per criterion (reasoning, score, feedback, confidence) at low temperature with a fixed seed, so regrades are stable; the server clamps and sums the scores.",
             "Row-level security per professor, a 50-requests-per-hour AI rate limit, and sanitized submission HTML."],
        features=[
            ("Canvas sync", "Connect by token or extension, then choose which courses to sync."),
            ("Three-pane grader", "Course and assignment pickers, a student list with status and confidence, and the submission."),
            ("Any file format", "Viewer for text, PDFs, Word, images, code, and links, with tabs for multiple files."),
            ("One-click AI grade", "Scores the open submission per rubric criterion, with a confidence banner."),
            ("Grade all", "A background batch with a live progress counter that survives page reloads."),
            ("Interactive rubric", "Rating pills or point inputs per criterion, auto-summed, with manual override and CSV import."),
            ("Feedback in your voice", "AI comments written in the professor's own grading persona, fully editable."),
            ("Review triage", "Low-confidence or unreadable submissions are flagged before posting."),
            ("Post to Canvas", "Grade, comment, and rubric assessment written back in one click."),
            ("Grade button in Canvas", "The Chrome extension adds a FacultyWise button to Canvas assignment pages."),
            ("AI assistant", "Streaming chat with file attachments, Google Drive picker, and voice input."),
            ("Document canvas", "Editable documents with AI edits, version history, Word export, and Send to Canvas."),
            ("Daily briefing", "An AI-built priority task list from Canvas and connected tools."),
            ("Onboarding + persona", "Guided setup that installs the extension, syncs courses, and learns the grading style."),
        ],
        stats=[("36", "file types graded"), ("5", "professors in the pilot")],
        takeaway="Most of the work was getting messy real-world submissions into a form a model can grade fairly.",
    ),
    dict(
        slug="claudepearl",
        title="ClaudePearl",
        oneliner=("A desktop and phone app for AI-assisted development, with persistent project memory, "
                  "auto-loaded skills, and live control of Roblox Studio and Blender."),
        hud=[("Role", "Solo"), ("Built", "Jul 2026"),
             ("Status", "v1.5, in daily use"), ("Stack", "TypeScript · Fastify · SQLite · React · Tauri")],
        row_kind="Developer tool",
        row_meta="Solo project · Jul 2026",
        links=[],
        note="Private repository. Screenshots show the real app running on demo data.",
        why_lead=("By mid-2026, Claude Code already had memory, skills, and phone access. ClaudePearl rebuilds them "
                  "around how I actually work as a solo game developer:"),
        why=["One session, any screen: a local backend owns every session, so several named sessions keep running and I can steer any of them from my phone, with push alerts when replies land.",
             "Memory I control: decisions are saved on purpose with remember:, stored as structured data, summarized per session, and browsable, instead of notes the model picks for itself.",
             "Predictable context: skills are picked by keyword score and capped at two per prompt, so I always know what was loaded and why.",
             "Limits at a glance: context, the 5-hour and weekly windows, and cost stay on screen instead of behind a command.",
             "Game-dev tooling: live connection checks for Roblox Studio and Blender, and an overnight agent that researches Roblox trends and pitches a buildable concept."],
        shots=[("/assets/claudepearl/chat.webp", 1440, 900,
                "ClaudePearl chat view: Claude reads a skill, inspects Roblox Studio, and builds a model through MCP",
                "Chat: Claude reads a project skill, inspects Roblox Studio, and builds the model live."),
               ("/assets/claudepearl/memory.webp", 1440, 900,
                "Memory constellation: sessions, decisions, summaries and skills as stars",
                "Memory: every session, decision, summary, and skill, with the skills library lit up."),
               ("/assets/claudepearl/dreams.webp", 1440, 900,
                "Overnight research report with trending game niches and a buildable concept",
                "Dreams: the overnight research agent's report."),
               ("/assets/claudepearl/dashboard.webp", 1440, 900,
                "Dashboard with context, usage windows, session cost, tokens, and remembered decisions",
                "Dashboard: context, usage limits, cost, and the project's remembered decisions."),
               ("/assets/claudepearl/mcp.webp", 1440, 900,
                "MCP panel showing live connections to Roblox Studio and Blender",
                "MCP: live connection status for Roblox Studio and Blender.")],
        thumb=("/assets/claudepearl/thumb.webp", 264, 165),
        flow=[("Clients", "Tauri desktop app + phone web app"), ("API", "Fastify REST API + a live WebSocket stream"),
              ("Sessions", "One long-lived Agent SDK session per project"), ("Memory", "SQLite per project: decisions, summaries, messages"),
              ("Tools", "MCP bridges to Roblox Studio and Blender")],
        problem=("Building Roblox games with Claude Code meant sitting at the desk watching a terminal through long "
                 "runs, finding out about usage limits by hitting them, and re-explaining project decisions from one "
                 "session to the next."),
        solution=("A thin layer over the official Claude Agent SDK. One local backend owns every session, and the "
                  "desktop app and a phone web app are both clients of it, so a chat started at the desk continues "
                  "on the phone."),
        how=["Each session starts with the project's last summary and its 15 most recent decisions injected into the prompt.",
             "Skills are scored by keyword match against the prompt; only the top two are loaded, never the whole library.",
             "Messages sent mid-turn are queued into the running session, so Claude can be steered while it works.",
             "An overnight research agent runs headless with web-only tools, a turn cap, a usage check, and output validation before anything is saved.",
             "Tool status is probed directly, so the app shows whether Studio and Blender are really connected."],
        features=[
            ("Roblox + Blender", "Claude inspects and builds in Roblox Studio and Blender through MCP."),
            ("Dreams", "A 4 AM research agent that scouts Roblox trends and pitches a buildable concept."),
            ("Phone access", "A phone web app on the same sessions, over a private Tailscale network, with push alerts."),
            ("Memory constellation", "A 3D map of sessions, decisions, summaries, skills, and projects."),
            ("Usage HUD", "Context %, 5-hour and weekly limits with reset countdowns, and session cost."),
            ("Remembered decisions", "Prefix a message with remember: and it's injected into every future session."),
            ("Auto summaries", "Ending a session has Claude summarize it to seed the next one."),
            ("Skills library", "Project skill modules; the most relevant ones load automatically for each prompt."),
            ("Resumable sessions", "Named sessions per project that survive restarts, in parallel chat tabs."),
            ("Live streaming", "Token-by-token replies with tool calls, thinking, and results inline."),
            ("Steer mid-turn", "Send messages while Claude works, or press Esc to interrupt."),
            ("Image input", "Paste or attach up to 8 images per message."),
            ("In-app questions", "Answer Claude's clarifying questions right in the GUI."),
            ("Live game stats", "Public player stats for Roblox games, inside the app."),
        ],
        stats=[],
        takeaway="The win wasn't a nicer chat window; it was memory: sessions that remember why a decision was made.",
    ),
]

SKILLS = [
    ("Languages", "TypeScript, JavaScript, Python, Java, C++, SQL"),
    ("Web", "React, Next.js, Vite, Node.js, Fastify, Flask, Django, Tailwind CSS"),
    ("AI & data", "Claude Agent SDK, MCP, OpenAI and Gemini APIs, RAG, Pinecone, scikit-learn, pandas"),
    ("Data & infra", "PostgreSQL, Supabase, SQLite, Drizzle, pg-boss, Inngest, Docker, Vercel, Vitest, Git, Linux"),
    ("Platforms", "Chrome extensions (MV3), Tauri desktop apps, Canvas LMS API"),
]

# Games track content lives in tools/games.py
from games import GAMES  # noqa: E402
