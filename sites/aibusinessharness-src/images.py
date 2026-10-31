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


AMBER = "#f2b46b"


# 11 — what is an AI harness: model inside a ring of controls
def img_harness_explained():
    import math
    cx, cy = 845, 300
    s = f'<circle cx="{cx}" cy="{cy}" r="228" fill="none" stroke="{LINE}" stroke-opacity=".35"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="148" fill="none" stroke="{BLUE2}" stroke-width="10" stroke-opacity=".35"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="148" fill="none" stroke="{BLUE}" stroke-opacity=".55" stroke-dasharray="3 9"/>'
    for t, a in [("LEADS", -150), ("ESTIMATES", -30), ("INBOX", 90)]:
        r = math.radians(a)
        x, y = cx + 228 * math.cos(r), cy + 228 * math.sin(r)
        s += line(cx + 162 * math.cos(r), cy + 162 * math.sin(r), x, y)
        s += chip(x, y, t)
    for t, a, hot in [("TOOLS", -90, False), ("RULES", 0, False), ("APPROVAL", 180, True), ("RECORD", 45 + 90, False)]:
        r = math.radians(a)
        x, y = cx + 148 * math.cos(r), cy + 148 * math.sin(r)
        s += chip(x, y, t, active=hot)
    s += node(cx, cy, 66, "MODEL", "THE BRAIN", strong=True)
    s += f'<text x="100" y="236" font-size="52" font-weight="600" letter-spacing="-2" fill="{INK}">What is an</text>'
    s += f'<text x="100" y="298" font-size="52" font-weight="600" letter-spacing="-2" fill="{BLUE}">AI harness?</text>'
    s += f'<text x="102" y="344" font-size="15" letter-spacing="1" fill="{MUTED}">Explained for business owners</text>'
    s += f'<text x="102" y="372" font-size="15" letter-spacing="1" fill="{MUTED}">Tools · rules · approval · record</text>'
    return s


# inline — agent running wild vs harnessed agent
def img_wild_vs_harnessed():
    s = f'<line x1="600" y1="70" x2="600" y2="520" stroke="{LINE}" stroke-opacity=".5"/>'
    s += f'<text x="70" y="78" font-size="13" font-weight="700" letter-spacing="3" fill="{AMBER}">NO HARNESS</text>'
    s += f'<text x="70" y="102" font-size="14" fill="{MUTED}">Broad access · no steps · no review</text>'
    s += f'<text x="650" y="78" font-size="13" font-weight="700" letter-spacing="3" fill="{BLUE}">HARNESSED</text>'
    s += f'<text x="650" y="102" font-size="14" fill="{MUTED}">Approved tools · approval · a record</text>'
    ax, ay = 190, 320
    targets = [("ALL EMAIL", 450, 160), ("BANK", 470, 240), ("PAYROLL", 470, 320), ("CUSTOMERS", 460, 400), ("EVERY FILE", 440, 480)]
    for t, x, y in targets:
        s += f'<line x1="{ax+52}" y1="{ay}" x2="{x-62}" y2="{y}" stroke="{AMBER}" stroke-opacity=".7" stroke-width="1.4"/>'
        s += (f'<g transform="translate({x} {y})"><rect x="-62" y="-18" width="124" height="36" rx="5" fill="{CARD}" stroke="{AMBER}" stroke-opacity=".7"/>'
              f'<text y="5" text-anchor="middle" font-size="11" font-weight="700" letter-spacing="2" fill="#f6d6ad">{t}</text></g>')
    s += node(ax, ay, 52, "AGENT")
    s += f'<text x="{ax}" y="{ay+88}" text-anchor="middle" font-size="11" letter-spacing="2.4" fill="{AMBER}">ACTS ON ITS OWN</text>'
    # harnessed flow
    y = 300
    s += f'<rect x="640" y="150" width="510" height="310" rx="14" fill="none" stroke="{BLUE2}" stroke-opacity=".7" stroke-dasharray="3 7"/>'
    s += f'<text x="660" y="176" font-size="10" font-weight="700" letter-spacing="2.6" fill="{BLUE2}">HARNESS</text>'
    s += node(715, y, 44, "AGENT")
    s += line(759, y, 800, y, dash=False, color=BLUE2)
    s += f'<g transform="translate(850 {y-50})">{chip(0,0,"CRM",100)}</g><g transform="translate(850 {y+50})">{chip(0,0,"INBOX",100)}</g>'
    s += line(800, y, 800, y - 50, dash=False, color=BLUE2) + line(800, y, 800, y + 50, dash=False, color=BLUE2)
    s += line(900, y - 50, 950, y, dash=False, color=BLUE2) + line(900, y + 50, 950, y, dash=False, color=BLUE2)
    s += f'<circle cx="985" cy="{y}" r="34" fill="#1d2b42" stroke="{BLUE}"/>'
    s += f'<circle cx="985" cy="{y-9}" r="8" fill="none" stroke="{INK}" stroke-width="2"/><path d="M969 {y+17} q16 -20 32 0" fill="none" stroke="{INK}" stroke-width="2"/>'
    s += f'<text x="985" y="{y+58}" text-anchor="middle" font-size="10" font-weight="700" letter-spacing="2.2" fill="{BLUE}">YOU APPROVE</text>'
    s += line(1019, y, 1060, y, dash=False, color=BLUE2)
    s += f'<g transform="translate(1090 {y})"><circle r="24" fill="#1d2b42" stroke="{BLUE}"/>{check(0,0)}</g>'
    s += f'<text x="1090" y="{y+50}" text-anchor="middle" font-size="10" font-weight="700" letter-spacing="2.2" fill="{INK}">SENT</text>'
    s += f'<text x="1090" y="{y+66}" text-anchor="middle" font-size="10" letter-spacing="2.2" fill="{MUTED}">+ LOGGED</text>'
    s += f'<text x="895" y="430" text-anchor="middle" font-size="11" letter-spacing="2.4" fill="{MUTED}">ONLY THE TOOLS THE JOB NEEDS</text>'
    return s


# inline — three things called "harness"
def img_three_meanings():
    cards = [
        ("DEVELOPER PLATFORMS", ["Foundations engineers use", "to build their own agents"], "FOR ENGINEERS", False),
        ("SOFTWARE DELIVERY", ["Same word, different job:", "testing and shipping code"], "FOR DEV TEAMS", False),
        ("OPERATIONS HARNESS", ["Built around your own", "workflows and tools"], "FOR YOUR BUSINESS", True),
    ]
    s = f'<text x="600" y="92" text-anchor="middle" font-size="40" font-weight="600" letter-spacing="-1.5" fill="{INK}">Three things called <tspan fill="{BLUE}">"harness"</tspan></text>'
    for i, (t, lines_, tag, hot) in enumerate(cards):
        x = 90 + i * 350
        if hot:
            s += f'<rect x="{x-14}" y="136" width="328" height="358" rx="14" fill="{BLUE}" opacity=".12" filter="url(#soft)"/>'
        s += f'<rect x="{x}" y="150" width="300" height="330" rx="10" fill="{"#1d2b42" if hot else CARD}" stroke="{BLUE if hot else LINE}" stroke-opacity=".85"/>'
        s += f'<text x="{x+28}" y="196" font-size="11" font-weight="700" letter-spacing="2.6" fill="{BLUE if hot else MUTED}">0{i+1}</text>'
        s += f'<text x="{x+28}" y="232" font-size="15" font-weight="700" letter-spacing="2.2" fill="{INK}">{t}</text>'
        for j, ln in enumerate(lines_):
            s += f'<text x="{x+28}" y="{272+j*26}" font-size="17" fill="{"#dbe6f7" if hot else "#b8c6da"}">{ln}</text>'
        # mini glyph
        gy = 380
        if i == 0:
            for k in range(4):
                s += f'<rect x="{x+28+k*34}" y="{gy}" width="26" height="26" rx="4" fill="none" stroke="{LINE}"/>'
            s += f'<text x="{x+190}" y="{gy+19}" font-size="15" fill="{MUTED}">&lt;/&gt;</text>'
        elif i == 1:
            s += f'<path d="M{x+28} {gy+13} h170" stroke="{LINE}" stroke-width="1.6"/>'
            for k in range(4):
                s += f'<circle cx="{x+40+k*50}" cy="{gy+13}" r="8" fill="{CARD2}" stroke="{LINE}"/>'
        else:
            cx0 = x + 28
            for k, w in enumerate(["INQUIRY", "DRAFT", "APPROVE"]):
                cw = len(w) * 9 + 24
                s += chip(cx0 + cw / 2, gy + 13, w, cw, active=(k == 2))
                cx0 += cw + 8
        s += f'<text x="{x+28}" y="452" font-size="11" font-weight="700" letter-spacing="2.4" fill="{BLUE if hot else LINE}">{tag}</text>'
        if hot:
            s += f'<g transform="translate({x+262} 196)"><circle r="16" fill="#1d2b42" stroke="{BLUE}"/>{check(0,0,.7)}</g>'
    return s


# 14 — Microsoft's enterprise harness vs. the small business version
def img_enterprise_vs_local():
    s = f'<text x="600" y="86" text-anchor="middle" font-size="38" font-weight="600" letter-spacing="-1.5" fill="{INK}">Same idea, <tspan fill="{BLUE}">different size</tspan></text>'
    s += f'<text x="600" y="120" text-anchor="middle" font-size="15" letter-spacing="1" fill="{MUTED}">The harness, not the model, is what gets the work done</text>'
    # left panel: enterprise developer platform
    x0 = 80
    s += f'<rect x="{x0}" y="160" width="480" height="340" rx="10" fill="{CARD}" stroke="{LINE}" stroke-opacity=".85"/>'
    s += f'<text x="{x0+28}" y="200" font-size="12" font-weight="700" letter-spacing="2.6" fill="{MUTED}">ENTERPRISE</text>'
    s += f'<text x="{x0+28}" y="232" font-size="20" font-weight="600" fill="{INK}">A platform developers build on</text>'
    for r in range(3):
        for c in range(6):
            s += f'<rect x="{x0+28+c*72}" y="{262+r*40}" width="60" height="28" rx="4" fill="none" stroke="{LINE}" stroke-opacity=".8"/>'
    s += f'<text x="{x0+28}" y="410" font-size="15" fill="#b8c6da">20+ models · SDK · cloud runtime</text>'
    s += f'<text x="{x0+28}" y="470" font-size="11" font-weight="700" letter-spacing="2.4" fill="{LINE}">NEEDS AN ENGINEERING TEAM</text>'
    # right panel: small business harness
    x1 = 640
    s += f'<rect x="{x1-14}" y="146" width="508" height="368" rx="14" fill="{BLUE}" opacity=".12" filter="url(#soft)"/>'
    s += f'<rect x="{x1}" y="160" width="480" height="340" rx="10" fill="#1d2b42" stroke="{BLUE}" stroke-opacity=".85"/>'
    s += f'<text x="{x1+28}" y="200" font-size="12" font-weight="700" letter-spacing="2.6" fill="{BLUE}">YOUR BUSINESS</text>'
    s += f'<text x="{x1+28}" y="232" font-size="20" font-weight="600" fill="{INK}">A harness built and run for you</text>'
    cx0 = x1 + 28
    for k, w in enumerate(["LEADS", "ESTIMATES", "INBOX"]):
        cw = len(w) * 9 + 32
        s += chip(cx0 + cw / 2, 290, w, cw)
        cx0 += cw + 12
    s += line(x1 + 240, 312, x1 + 240, 352, dash=False, color=BLUE2)
    s += chip(x1 + 240, 372, "YOU APPROVE", 170, active=True)
    s += f'<g transform="translate({x1+380} 372)"><circle r="18" fill="#1d2b42" stroke="{BLUE}"/>{check(0,0,.8)}</g>'
    s += line(x1 + 325, 372, x1 + 362, 372, dash=False, color=BLUE2)
    s += f'<text x="{x1+28}" y="470" font-size="11" font-weight="700" letter-spacing="2.4" fill="{BLUE}">NEEDS THE TOOLS YOU ALREADY USE</text>'
    return s


# inline — how the layers stack up
def img_stack():
    layers = [
        ("BUSINESS OUTCOMES", "Follow-ups · records · scheduling · reporting", "WHAT YOU SEE", False),
        ("AI BUSINESS HARNESS", "Workflow rules · permissions · approvals · checks · monitoring", "WHERE YOU APPROVE", True),
        ("AGENT ENGINE", "Microsoft Copilot SDK / Foundry, or another runtime", "WE MANAGE", False),
        ("MODELS AND TOOLS", "AI models · skills · MCP · CRM · email · calendar", "WE CONNECT", False),
    ]
    s = f'<text x="600" y="70" text-anchor="middle" font-size="30" font-weight="600" letter-spacing="-1" fill="{INK}">How the pieces <tspan fill="{BLUE}">stack up</tspan></text>'
    x, w, h, gap, y0 = 150, 900, 92, 22, 104
    for i, (name, sub, tag, hot) in enumerate(layers):
        y = y0 + i * (h + gap)
        if hot:
            s += f'<rect x="{x-12}" y="{y-12}" width="{w+24}" height="{h+24}" rx="14" fill="{BLUE}" opacity=".14" filter="url(#soft)"/>'
        s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{"#1d2b42" if hot else CARD}" stroke="{BLUE if hot else LINE}" stroke-opacity=".85"/>'
        s += f'<text x="{x+32}" y="{y+40}" font-size="17" font-weight="700" letter-spacing="2.4" fill="{INK}">{name}</text>'
        s += f'<text x="{x+32}" y="{y+68}" font-size="16" fill="{"#dbe6f7" if hot else "#b8c6da"}">{sub}</text>'
        s += f'<text x="{x+w-32}" y="{y+40}" text-anchor="end" font-size="11" font-weight="700" letter-spacing="2.4" fill="{BLUE if hot else MUTED}">{tag}</text>'
        if i < len(layers) - 1:
            s += line(600, y + h, 600, y + h + gap, dash=False, color=BLUE2)
    return s


INLINE = {
    "ai-harness-running-wild-vs-harnessed": (img_wild_vs_harnessed, "AGENT VS HARNESS"),
    "ai-harness-three-meanings": (img_three_meanings, "WHICH HARNESS?"),
    "ai-business-harness-stack": (img_stack, "HOW IT STACKS UP"),
}


# 12 — what an agent product supplies vs. what the harness still adds
def img_grok_coverage():
    s = f'<text x="100" y="118" font-size="40" font-weight="600" letter-spacing="-1.5" fill="{INK}">Grok Bot covers part.</text>'
    s += f'<text x="100" y="166" font-size="40" font-weight="600" letter-spacing="-1.5" fill="{BLUE}">The harness covers the rest.</text>'
    left = [("CLOUD COMPUTER + APP SIGN-IN", "Bots work across your tools", False),
            ("MODEL-BASED AUTO-REVIEW", "A model screens risky actions", False),
            ("ENTERPRISE-ONLY CONTROLS", "Network rules · audit · recording", False)]
    right = [("SCOPED PERMISSIONS", "Minimum access per workflow", True),
             ("EXACT-ACTION APPROVAL", "A person signs off", True),
             ("VERIFY + RECONCILE", "Confirm results, never assume", True),
             ("DUPLICATE PROTECTION", "One send, one booking", True),
             ("BUSINESS RECORD", "Who approved what, and why", True)]
    s += f'<text x="100" y="232" font-size="11" font-weight="700" letter-spacing="2.6" fill="{MUTED}">WHAT GROK BOT SUPPLIES</text>'
    s += f'<text x="640" y="232" font-size="11" font-weight="700" letter-spacing="2.6" fill="{BLUE}">WHAT THE HARNESS STILL ADDS</text>'
    for i, (a, b, _) in enumerate(left):
        y = 252 + i * 92
        s += f'<rect x="100" y="{y}" width="460" height="76" rx="6" fill="{CARD}" stroke="{LINE}" stroke-opacity=".8"/>'
        s += f'<text x="124" y="{y+33}" font-size="12" font-weight="700" letter-spacing="2.2" fill="{INK}">{a}</text>'
        s += f'<text x="124" y="{y+56}" font-size="13" letter-spacing=".4" fill="{MUTED}">{b}</text>'
    for i, (a, b, _) in enumerate(right):
        y = 252 + i * 56
        s += f'<rect x="640" y="{y}" width="460" height="46" rx="6" fill="#1d2b42" stroke="{BLUE2}" stroke-opacity=".9"/>'
        s += f'<g transform="translate(664 {y+23})">{check(0, 0, .8)}</g>'
        s += f'<text x="690" y="{y+28}" font-size="11.5" font-weight="700" letter-spacing="2" fill="{INK}">{a}</text>'
        s += f'<text x="1084" y="{y+28}" text-anchor="end" font-size="11.5" letter-spacing=".3" fill="{MUTED}">{b}</text>'
    s += line(560, 380, 640, 380, dash=True, color=BLUE2, op=.9)
    return s


IMAGES = {
    "grok-ai-business-harness": (img_grok_coverage, "PLATFORMS"),
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
    "what-is-an-ai-harness-small-business": (img_harness_explained, "FOUNDATIONS"),
    "microsoft-copilot-harness-small-business": (img_enterprise_vs_local, "INDUSTRY NEWS"),
}


def svg_for(slug: str) -> str:
    fn, label = IMAGES.get(slug) or INLINE[slug]
    return frame(fn(), label)
