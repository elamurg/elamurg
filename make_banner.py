"""
Generates banner.svg: a GitHub-style contribution grid that fills with
green from left to right, then reveals your name and headline.

Run:  python make_banner.py
Then commit banner.svg to your profile repo.
"""
import random

# ---- Your content (edit these) ------------------------------------------
FULL_NAME = "Ela Murgelj"
LINE_2 = "MSc Computer Science"
LINE_3 = "LLM multi-agent systems, RAG systems, recommendation systems"

# ---- Layout --------------------------------------------------------------
WIDTH, HEIGHT = 960, 300
COLS, ROWS = 52, 7          # 52 weeks x 7 days, like the real graph
CELL, GAP = 13, 4           # square size and spacing in pixels
PITCH = CELL + GAP          # distance from one square to the next
GRID_X = (WIDTH - (COLS * PITCH - GAP)) // 2   # centres the grid
GRID_Y = 28

# ---- GitHub dark-mode colours --------------------------------------------
BG, BORDER, EMPTY = "#0d1117", "#30363d", "#161b22"
GREENS = ["#0e4429", "#006d32", "#26a641", "#39d353"]  # levels 1-4

# ---- Timing (seconds) ----------------------------------------------------
COL_DELAY = 0.035           # each column starts this much after the last
ROW_DELAY = 0.01            # tiny extra delay down each column
TEXT_START = COLS * COL_DELAY + 0.3

random.seed(7)              # same "random" grid every time you run it

def level():
    """Pick an activity level 0-4, weighted so the grid looks realistic."""
    return random.choices([0, 1, 2, 3, 4], weights=[15, 30, 25, 18, 12])[0]

css = [
    f".cell{{fill:{EMPTY};animation-duration:.45s;"
    "animation-timing-function:ease-out;animation-fill-mode:forwards}",
]
for i, g in enumerate(GREENS, start=1):
    css.append(f"@keyframes f{i}{{to{{fill:{g}}}}}")
    css.append(f".l{i}{{animation-name:f{i}}}")
css.append("@keyframes rise{from{opacity:0;transform:translateY(8px)}"
           "to{opacity:1;transform:translateY(0)}}")
css.append(".t{opacity:0;animation:rise .7s ease-out forwards}")
css.append("@media (prefers-reduced-motion:reduce){.cell,.t{animation-duration:0s!important;"
           "animation-delay:0s!important}}")

cells = []
for c in range(COLS):
    for r in range(ROWS):
        lv = level()
        x, y = GRID_X + c * PITCH, GRID_Y + r * PITCH
        cls = f"cell l{lv}" if lv else "cell"
        delay = c * COL_DELAY + r * ROW_DELAY
        cells.append(
            f'<rect class="{cls}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'rx="2" style="animation-delay:{delay:.3f}s"/>'
        )

font = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
texts = [
    (FULL_NAME, 205, 40, "#e6edf3", 600),
    (LINE_2, 240, 19, "#8b949e", 400),
    (LINE_3, 270, 17, "#3fb950", 500),
]
text_els = []
for i, (txt, y, size, color, weight) in enumerate(texts):
    text_els.append(
        f'<text class="t" x="{GRID_X}" y="{y}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" '
        f'style="animation-delay:{TEXT_START + i * 0.3:.2f}s">{txt}</text>'
    )

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" font-family="{font}" role="img" aria-label="{FULL_NAME}, {LINE_2}. {LINE_3}">
<style>{"".join(css)}</style>
<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{HEIGHT-1}" rx="12" fill="{BG}" stroke="{BORDER}"/>
{chr(10).join(cells)}
{chr(10).join(text_els)}
</svg>'''

with open("banner.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("banner.svg written")