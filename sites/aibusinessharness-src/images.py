"""Original editorial illustrations for the AI Business Harness blog.

Each function returns the inner SVG for one 1200x630 artwork. `frame()` wraps it
with the shared background, glow and brand mark so every image matches the site.
"""

W, H = 1200, 630
INK = "#e8eef8"
MUTED = "#8fa0b8"
LINE = "#5c718d"
BLUE = "#acc8ff"
BLUE2 = "#6f8fc6"
CARD = "#141c29"
CARD2 = "#1a2536"
FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def frame(inner: str, label: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">
<defs>
  <radialGradient id="glow" cx="62%" cy="48%" r="55%"><stop offset="0" stop-color="#3a5a8f" stop-opacity=".55"/><stop offset=".55" stop-color="#16233a" stop-opacity=".35"/><stop offset="1" stop-color="#080a0e" stop-opacity="0"/></radialGradient>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0f16"/><stop offset="1" stop-color="#070a0f"/></linearGradient>
  <linearGradient id="core" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2c3f5c"/><stop offset=".7" stop-color="#101722"/></linearGradient>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
  <pattern id="dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.1" fill="#ffffff" opacity=".05"/></pattern>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<rect width="{W}" height="{H}" fill="url(#dots)"/>
<rect width="{W}" height="{H}" fill="url(#glow)"/>
<g font-family="{FONT}">
{inner}
<g transform="translate(56 572)">
  <g transform="skewX(-15)"><rect x="0" y="0" width="5" height="20" fill="{INK}"/><rect x="9" y="4" width="5" height="16" fill="{INK}" opacity=".7"/><rect x="18" y="8" width="5" height="12" fill="{INK}" opacity=".45"/></g>
  <text x="38" y="16" font-size="13" letter-spacing="3" fill="{INK}">AI BUSINESS <tspan font-weight="700">HARNESS</tspan></text>
</g>
<text x="{W-56}" y="588" text-anchor="end" font-size="12" letter-spacing="3" fill="{MUTED}">{label}</text>
</g>
</svg>'''


def chip(x, y, text, w=None, active=False):
    w = w or (len(text) * 9 + 40)
    fill = "#1d2b42" if active else CARD
    stroke = BLUE2 if active else LINE
    color = INK if active else "#cfdcee"
    return (f'<g transform="translate({x} {y})"><rect x="{-w/2}" y="-20" width="{w}" height="40" rx="5" fill="{fill}" stroke="{stroke}" stroke-opacity=".8"/>'
            f'<text x="0" y="5" text-anchor="middle" font-size="12" font-weight="700" letter-spacing="2.4" fill="{color}">{text}</text></g>')


def node(x, y, r, text, sub=None, strong=False):
    s = (f'<circle cx="{x}" cy="{y}" r="{r+26}" fill="{BLUE}" opacity=".08" filter="url(#soft)"/>' if strong else "")
    s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#core)" stroke="{BLUE if strong else LINE}" stroke-opacity="{.8 if strong else .7}"/>'
    s += f'<text x="{x}" y="{y + (0 if sub else 5)}" text-anchor="middle" font-size="{17 if strong else 13}" font-weight="700" letter-spacing="2" fill="{INK}">{text}</text>'
    if sub:
        s += f'<text x="{x}" y="{y+20}" text-anchor="middle" font-size="10" letter-spacing="2.5" fill="{MUTED}">{sub}</text>'
    return s


def line(x1, y1, x2, y2, dash=True, color=LINE, op=.8):
    d = ' stroke-dasharray="4 6"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-opacity="{op}" stroke-width="1.4"{d}/>'


def check(x, y, s=1.0, color=BLUE):
    return f'<path d="M{x-7*s} {y} l{5*s} {5*s} l{10*s} {-11*s}" fill="none" stroke="{color}" stroke-width="{2.4*s}" stroke-linecap="round" stroke-linejoin="round"/>'


# 1 — the operating layer around a model
def img_operating_layer():
    cx, cy = 830, 300
    s = f'<circle cx="{cx}" cy="{cy}" r="215" fill="none" stroke="{LINE}" stroke-opacity=".5"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="160" fill="none" stroke="{BLUE2}" stroke-opacity=".55" stroke-dasharray="2 7"/>'
    items = [("EMAIL", -145), ("CRM", -55), ("FILES", 10), ("CALENDAR", 95), ("REPORTS", 160)]
    import math
    for t, a in items:
        rad = math.radians(a)
        x, y = cx + 215 * math.cos(rad), cy + 215 * math.sin(rad)
        s += line(cx + 75 * math.cos(rad), cy + 75 * math.sin(rad), x, y)
        s += chip(x, y, t)
    s += node(cx, cy, 72, "MODEL", "REASONING", strong=True)
    # approval gate on ring
    s += f'<g transform="translate({cx+160*math.cos(math.radians(65))} {cy+160*math.sin(math.radians(65))})"><circle r="22" fill="#1d2b42" stroke="{BLUE}"/>{check(0,0)}</g>'
    s += f'<text x="110" y="250" font-size="54" font-weight="600" letter-spacing="-2" fill="{INK}">The operating</text>'
    s += f'<text x="110" y="312" font-size="54" font-weight="600" letter-spacing="-2" fill="{BLUE}">layer around AI.</text>'
    s += f'<text x="112" y="360" font-size="15" letter-spacing="1" fill="{MUTED}">Tools · steps · approvals · records</text>'
    return s


# 2 — model / agent / harness layers
def img_three_layers():
    s = ""
    layers = [(520, "HARNESS", "CONTROLS · PERMISSIONS · RECORDS", 300, .35), (400, "AGENT", "GOAL · INSTRUCTIONS · TOOLS", 220, .55), (280, "MODEL", "REASONING", 140, .9)]
    cx, cy = 740, 300
    for w, t, sub, h, op in layers:
        s += f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{h/2}" fill="{CARD}" fill-opacity="{op}" stroke="{BLUE2 if t=="HARNESS" else LINE}" stroke-opacity=".8"/>'
    s += f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-size="18" font-weight="700" letter-spacing="3" fill="{INK}">MODEL</text>'
    s += f'<text x="{cx}" y="{cy-82}" text-anchor="middle" font-size="13" font-weight="700" letter-spacing="3" fill="#cfdcee">AGENT</text>'
    s += f'<text x="{cx}" y="{cy-122}" text-anchor="middle" font-size="13" font-weight="700" letter-spacing="3" fill="{BLUE}">HARNESS</text>'
    for i, t in enumerate(["SKILL", "ASSIGNMENT", "WORKPLACE"]):
        s += f'<text x="{cx}" y="{cy+[32,96,136][i]}" text-anchor="middle" font-size="10" letter-spacing="3" fill="{MUTED}">{t}</text>'
    s += f'<text x="110" y="250" font-size="50" font-weight="600" letter-spacing="-2" fill="{INK}">Model. Agent.</text>'
    s += f'<text x="110" y="310" font-size="50" font-weight="600" letter-spacing="-2" fill="{BLUE}">Harness.</text>'
    s += f'<text x="112" y="356" font-size="15" letter-spacing="1" fill="{MUTED}">Three layers, three different jobs</text>'
    return s


# 3 — task grid with best candidate rising
def img_task_grid():
    s = ""
    x0, y0 = 600, 130
    labels = ["INVOICES", "SCHEDULING", "INQUIRIES", "REPORTS", "DATA ENTRY", "REMINDERS", "INTAKE", "REVIEWS", "ESTIMATES"]
    k = 0
    for r in range(3):
        for c in range(3):
            x, y = x0 + c * 170, y0 + r * 120
            best = (r, c) == (2, 2)
            if best:
                continue
            s += f'<rect x="{x}" y="{y}" width="150" height="96" rx="6" fill="{CARD}" stroke="{LINE}" stroke-opacity=".6"/>'
            s += f'<text x="{x+16}" y="{y+30}" font-size="10" font-weight="700" letter-spacing="2" fill="{MUTED}">{labels[k]}</text>'
            bars = [(k * 37 + i * 23) % 60 + 20 for i in range(5)]
            for i, b in enumerate(bars):
                s += f'<rect x="{x+16+i*22}" y="{y+82-b*0.6}" width="12" height="{b*0.6}" rx="2" fill="{LINE}" opacity=".55"/>'
            k += 1
    x, y = x0 + 340, y0 + 240 - 14
    s += f'<rect x="{x-12}" y="{y-12}" width="174" height="120" rx="8" fill="{BLUE}" opacity=".12" filter="url(#soft)"/>'
    s += f'<rect x="{x}" y="{y}" width="150" height="96" rx="6" fill="#1d2b42" stroke="{BLUE}"/>'
    s += f'<text x="{x+16}" y="{y+30}" font-size="10" font-weight="700" letter-spacing="2" fill="{INK}">FOLLOW-UP</text>'
    for i, b in enumerate([30, 46, 58, 70, 82]):
        s += f'<rect x="{x+16+i*22}" y="{y+82-b*0.6}" width="12" height="{b*0.6}" rx="2" fill="{BLUE}" opacity=".85"/>'
    s += f'<text x="{x+75}" y="{y+128}" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2.4" fill="{BLUE}">START HERE ↑</text>'
    s += f'<text x="100" y="250" font-size="48" font-weight="600" letter-spacing="-2" fill="{INK}">Find the first</text>'
    s += f'<text x="100" y="308" font-size="48" font-weight="600" letter-spacing="-2" fill="{BLUE}">workflow worth it.</text>'
    s += f'<text x="102" y="352" font-size="15" letter-spacing="1" fill="{MUTED}">Frequent · consistent · costly when missed</text>'
    return s


# 4 — approval gate
def img_approval_gate():
    y = 300
    s = line(560, y, 1140, y, dash=False, color=LINE, op=.7)
    s += chip(620, y, "DRAFT")
    s += chip(780, y, "PREPARED")
    s += f'<rect x="880" y="{y-95}" width="10" height="190" rx="3" fill="{BLUE2}"/><rect x="990" y="{y-95}" width="10" height="190" rx="3" fill="{BLUE2}"/>'
    s += f'<rect x="880" y="{y-105}" width="120" height="14" rx="4" fill="{BLUE}"/>'
    s += f'<circle cx="945" cy="{y}" r="34" fill="#1d2b42" stroke="{BLUE}"/>'
    s += f'<circle cx="945" cy="{y-9}" r="9" fill="none" stroke="{INK}" stroke-width="2"/><path d="M928 {y+19} q17 -22 34 0" fill="none" stroke="{INK}" stroke-width="2"/>'
    s += f'<text x="945" y="{y+128}" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2.4" fill="{BLUE}">HUMAN APPROVAL</text>'
    s += f'<g transform="translate(1090 {y})"><circle r="24" fill="#1d2b42" stroke="{BLUE}"/>{check(0,0)}</g>'
    s += f'<text x="100" y="250" font-size="50" font-weight="600" letter-spacing="-2" fill="{INK}">AI prepares.</text>'
    s += f'<text x="100" y="310" font-size="50" font-weight="600" letter-spacing="-2" fill="{BLUE}">People approve.</text>'
    s += f'<text x="102" y="356" font-size="15" letter-spacing="1" fill="{MUTED}">Approval gates where mistakes cost most</text>'
    return s


def envelope(x, y, w=110, h=70, color=LINE, fill=CARD, op=1):
    return (f'<g opacity="{op}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{color}"/>'
            f'<path d="M{x} {y+4} L{x+w/2} {y+h*0.58} L{x+w} {y+4}" fill="none" stroke="{color}"/></g>')


# 5 — inbox sorting into lanes + drafts tray
def img_inbox():
    s = ""
    for i in range(4):
        s += envelope(560 + i * 8, 150 + i * 70, op=1 - i * 0.18)
    lanes = [("NEW INQUIRY", 170), ("URGENT", 270, True), ("CUSTOMER", 370), ("NEWSLETTER", 470)]
    for t, y, *hot in lanes:
        s += line(690, 220, 820, y, dash=True)
        s += chip(900, y, t, w=170, active=bool(hot))
    s += f'<rect x="1000" y="230" width="150" height="120" rx="8" fill="#1d2b42" stroke="{BLUE}"/>'
    s += f'<text x="1075" y="262" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2.4" fill="{BLUE}">DRAFTS</text>'
    for i in range(3):
        s += f'<rect x="1022" y="{280+i*20}" width="{106-i*18}" height="6" rx="3" fill="{INK}" opacity=".5"/>'
    s += line(985, 170, 1010, 230, dash=True, color=BLUE2)
    s += f'<text x="100" y="250" font-size="48" font-weight="600" letter-spacing="-2" fill="{INK}">An inbox that</text>'
    s += f'<text x="100" y="308" font-size="48" font-weight="600" letter-spacing="-2" fill="{BLUE}">sorts itself.</text>'
    s += f'<text x="102" y="352" font-size="15" letter-spacing="1" fill="{MUTED}">Sorted · flagged · drafted · you approve</text>'
    return s


# 6 — estimate queue
def img_estimates():
    s = ""
    rows = [("EST #2041", "6 DAYS", False), ("EST #2047", "5 DAYS", True), ("EST #2052", "4 DAYS", False)]
    for i, (a, b, hot) in enumerate(rows):
        y = 150 + i * 92
        s += f'<rect x="560" y="{y}" width="300" height="70" rx="6" fill="{"#1d2b42" if hot else CARD}" stroke="{BLUE if hot else LINE}" stroke-opacity=".8"/>'
        s += f'<text x="584" y="{y+31}" font-size="13" font-weight="700" letter-spacing="2" fill="{INK}">{a}</text>'
        s += f'<text x="584" y="{y+52}" font-size="10" letter-spacing="2" fill="{MUTED}">NO REPLY · {b}</text>'
        s += f'<circle cx="826" cy="{y+35}" r="13" fill="none" stroke="{MUTED}"/><path d="M826 {y+27} v8 l6 4" fill="none" stroke="{MUTED}" stroke-width="1.6"/>'
    s += line(860, 277, 930, 277, dash=False, color=BLUE2)
    s += f'<rect x="930" y="215" width="210" height="124" rx="8" fill="#1d2b42" stroke="{BLUE}"/>'
    s += f'<text x="952" y="246" font-size="11" font-weight="700" letter-spacing="2.4" fill="{BLUE}">FOLLOW-UP DRAFT</text>'
    for i in range(3):
        s += f'<rect x="952" y="{262+i*18}" width="{160-i*30}" height="6" rx="3" fill="{INK}" opacity=".45"/>'
    s += f'<g transform="translate(1120 330)"><circle r="20" fill="#0f1622" stroke="{BLUE}"/>{check(0,0,0.85)}</g>'
    s += f'<text x="100" y="250" font-size="48" font-weight="600" letter-spacing="-2" fill="{INK}">No quote left</text>'
    s += f'<text x="100" y="308" font-size="48" font-weight="600" letter-spacing="-2" fill="{BLUE}">behind.</text>'
    s += f'<text x="102" y="352" font-size="15" letter-spacing="1" fill="{MUTED}">Find · draft · approve · log</text>'
    return s


def window(x, y, w, h, title, body=""):
    return (f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{CARD}" stroke="{LINE}" stroke-opacity=".8"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="7" fill="{CARD2}"/>'
            f'<circle cx="{x+14}" cy="{y+13}" r="3.5" fill="{LINE}"/><circle cx="{x+26}" cy="{y+13}" r="3.5" fill="{LINE}"/>'
            f'<text x="{x+w-12}" y="{y+17}" text-anchor="end" font-size="9" font-weight="700" letter-spacing="2" fill="{MUTED}">{title}</text>{body}</g>')


# 7 — existing apps connected to a hub
def img_connect():
    hub = (820, 300)
    apps = [(570, 130, "EMAIL"), (950, 120, "CRM"), (560, 400, "SPREADSHEET"), (960, 410, "DESKTOP APP")]
    s = ""
    for x, y, t in apps:
        s += line(x + 85, y + 55, hub[0], hub[1])
    for x, y, t in apps:
        body = "".join(f'<rect x="{x+16}" y="{y+42+i*16}" width="{130-i*28}" height="6" rx="3" fill="{LINE}" opacity=".6"/>' for i in range(3))
        s += window(x, y, 170, 110, t, body)
    s += node(hub[0], hub[1], 50, "HUB", strong=True)
    s += f'<text x="100" y="250" font-size="48" font-weight="600" letter-spacing="-2" fill="{INK}">Keep your tools.</text>'
    s += f'<text x="100" y="308" font-size="48" font-weight="600" letter-spacing="-2" fill="{BLUE}">Connect them.</text>'
    s += f'<text x="102" y="352" font-size="15" letter-spacing="1" fill="{MUTED}">APIs · connectors · exports · browser</text>'
    return s


# 8 — API pipe vs browser cursor
def img_api_vs_browser():
    s = f'<line x1="860" y1="110" x2="860" y2="500" stroke="{LINE}" stroke-opacity=".5"/>'
    s += f'<text x="720" y="140" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2.4" fill="{BLUE}">API</text>'
    s += f'<text x="1010" y="140" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2.4" fill="{MUTED}">BROWSER</text>'
    s += f'<rect x="600" y="280" width="240" height="34" rx="17" fill="#1d2b42" stroke="{BLUE}"/>'
    for i in range(5):
        s += f'<rect x="{620+i*42}" y="291" width="26" height="12" rx="3" fill="{BLUE}" opacity="{.4+i*.12}"/>'
    s += chip(640, 220, "{ }", w=60) + chip(800, 380, "OK", w=60, active=True)
    body = "".join(f'<rect x="{900+16}" y="{230+i*22}" width="{170-i*35}" height="9" rx="3" fill="{LINE}" opacity=".6"/>' for i in range(4))
    body += f'<rect x="916" y="330" width="90" height="26" rx="4" fill="{CARD2}" stroke="{LINE}"/>'
    s += window(900, 190, 220, 190, "PORTAL", body)
    s += f'<path d="M995 340 l0 26 l7 -7 l6 13 l5 -2 l-6 -13 l10 0 z" fill="{INK}"/>'
    s += f'<text x="100" y="250" font-size="48" font-weight="600" letter-spacing="-2" fill="{INK}">API or</text>'
    s += f'<text x="100" y="308" font-size="48" font-weight="600" letter-spacing="-2" fill="{BLUE}">browser?</text>'
    s += f'<text x="102" y="352" font-size="15" letter-spacing="1" fill="{MUTED}">Choose the most structured path</text>'
    return s


# 9 — audit timeline
def img_audit_log():
    s = f'<line x1="640" y1="120" x2="640" y2="500" stroke="{LINE}" stroke-opacity=".7"/>'
    events = [("TRIGGER", "NEW INQUIRY RECEIVED", False), ("DECISION", "CLASSIFIED · PRICING QUESTION", False),
              ("ACTION", "REPLY DRAFTED", False), ("APPROVAL", "APPROVED BY OFFICE", True), ("RESULT", "VERIFIED · LOGGED", False)]
    for i, (a, b, hot) in enumerate(events):
        y = 140 + i * 84
        s += f'<circle cx="640" cy="{y+20}" r="9" fill="{"#1d2b42" if hot else CARD}" stroke="{BLUE if hot else LINE}" stroke-width="1.6"/>'
        s += f'<rect x="672" y="{y}" width="420" height="42" rx="5" fill="{"#1d2b42" if hot else CARD}" stroke="{BLUE if hot else LINE}" stroke-opacity=".7"/>'
        s += f'<text x="690" y="{y+26}" font-size="11" font-weight="700" letter-spacing="2.2" fill="{BLUE if hot else MUTED}">{a}</text>'
        s += f'<text x="800" y="{y+26}" font-size="11" letter-spacing="1.6" fill="{INK}">{b}</text>'
        s += f'<text x="1076" y="{y+26}" text-anchor="end" font-size="10" letter-spacing="1" fill="{MUTED}">09:{14+i*2:02d}</text>'
    s += f'<text x="100" y="250" font-size="48" font-weight="600" letter-spacing="-2" fill="{INK}">Every step,</text>'
    s += f'<text x="100" y="308" font-size="48" font-weight="600" letter-spacing="-2" fill="{BLUE}">on the record.</text>'
    s += f'<text x="102" y="352" font-size="15" letter-spacing="1" fill="{MUTED}">What it saw · decided · did · who approved</text>'
    return s


# 10 — four-week pilot
def img_pilot():
    s = ""
    weeks = [("WEEK 1", "DISCOVER"), ("WEEK 2", "DESIGN"), ("WEEK 3", "TEST"), ("WEEK 4", "DECIDE")]
    for i, (a, b) in enumerate(weeks):
        x = 580 + i * 140
        hot = i == 3
        s += f'<rect x="{x}" y="200" width="120" height="150" rx="7" fill="{"#1d2b42" if hot else CARD}" stroke="{BLUE if hot else LINE}" stroke-opacity=".8"/>'
        s += f'<text x="{x+60}" y="232" text-anchor="middle" font-size="10" font-weight="700" letter-spacing="2.4" fill="{MUTED}">{a}</text>'
        s += f'<text x="{x+60}" y="330" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2" fill="{BLUE if hot else INK}">{b}</text>'
        for r in range(3):
            for c in range(3):
                filled = (i * 9 + r * 3 + c) <= (i + 1) * 7
                s += f'<rect x="{x+22+c*28}" y="{250+r*18}" width="20" height="11" rx="2" fill="{BLUE if filled and hot else LINE}" opacity="{.85 if filled else .25}"/>'
        if i < 3:
            s += line(x + 120, 275, x + 140, 275, dash=False, color=BLUE2)
    s += f'<g transform="translate(1100 140)"><circle r="26" fill="#1d2b42" stroke="{BLUE}"/>{check(0,0)}</g>'
    s += f'<text x="100" y="250" font-size="48" font-weight="600" letter-spacing="-2" fill="{INK}">One workflow.</text>'
    s += f'<text x="100" y="308" font-size="48" font-weight="600" letter-spacing="-2" fill="{BLUE}">Thirty days.</text>'
    s += f'<text x="102" y="352" font-size="15" letter-spacing="1" fill="{MUTED}">Discover · design · test · decide</text>'
    return s


IMAGES = {
    "what-is-an-ai-business-harness": (img_operating_layer, "FOUNDATIONS"),
    "ai-model-vs-agent-vs-harness": (img_three_layers, "FOUNDATIONS"),
    "how-to-find-a-business-workflow-to-automate": (img_task_grid, "GETTING STARTED"),
    "human-approval-in-ai-workflows": (img_approval_gate, "SAFETY AND CONTROL"),
    "ai-email-assistant-small-business": (img_inbox, "WORKFLOWS"),
    "ai-estimate-follow-up-workflow": (img_estimates, "WORKFLOWS"),
    "connect-ai-to-existing-business-software": (img_connect, "INTEGRATIONS"),
    "ai-browser-automation-vs-api-integrations": (img_api_vs_browser, "INTEGRATIONS"),
    "what-to-log-ai-agent-business-work": (img_audit_log, "SAFETY AND CONTROL"),
    "30-day-ai-workflow-pilot": (img_pilot, "GETTING STARTED"),
}


def svg_for(slug: str) -> str:
    fn, label = IMAGES[slug]
    return frame(fn(), label)
