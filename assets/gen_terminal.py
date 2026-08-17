"""Generate the animated terminal SVG for the GitHub profile README."""

CHAR = 9  # mono advance at font-size 15
X_PROMPT, X_CMD = 28, 46
CURSOR_W, CURSOR_H = 9, 18

# (command, cmd_baseline_y, [(out_baseline_y, inner_xml), ...])
STATS = [
    (
        "agents deployed ......... ",
        '<tspan fill="#ffa657" font-weight="bold">20+</tspan>',
    ),
    (
        "accuracy ................ ",
        '<tspan fill="#ffa657" font-weight="bold">80% → 96%+</tspan>',
    ),
    (
        "response time ........... ",
        '<tspan fill="#ffa657" font-weight="bold">3–5 min → &lt;30 s</tspan>',
    ),
    (
        "eval cases .............. ",
        '<tspan fill="#ffa657" font-weight="bold">500+</tspan><tspan fill="#8b949e"> pre-deploy</tspan>',
    ),
    (
        "knowledge graph ......... ",
        '<tspan fill="#ffa657" font-weight="bold">4k → 30k</tspan><tspan fill="#8b949e"> assets @ 99%</tspan>',
    ),
    (
        "inference latency ....... ",
        '<tspan fill="#ffa657" font-weight="bold">150 ms</tspan><tspan fill="#8b949e"> (tensorrt)</tspan>',
    ),
]

LINES = [
    (
        "whoami",
        82,
        0.09,
        [
            (
                109,
                '<tspan fill="#e6edf3">akshay reddy — staff ai engineer · agentic systems · bangalore</tspan>',
                28,
            )
        ],
    ),
    (
        "./agents --prod --stats",
        147,
        0.05,
        [
            (174 + 27 * i, f'<tspan fill="#8b949e">{label}</tspan>{val}', 46)
            for i, (label, val) in enumerate(STATS)
        ],
    ),
    (
        "ls patents/",
        343,
        0.05,
        [
            (
                370,
                '<tspan fill="#79c0ff">agent-construction   data-products   payment-prediction-ml</tspan>',
                28,
            )
        ],
    ),
    (
        "ls honors/",
        404,
        0.05,
        [
            (
                431,
                '<tspan fill="#79c0ff">mistral-ai-hackathon.</tspan><tspan fill="#ffa657" font-weight="bold">1st</tspan>'
                '<tspan fill="#79c0ff">   totalenergies-scholar.</tspan><tspan fill="#ffa657" font-weight="bold">€32k</tspan>'
                '<tspan fill="#79c0ff">   eu-blue-horizon.</tspan><tspan fill="#ffa657" font-weight="bold">2020</tspan>',
                28,
            )
        ],
    ),
    (
        "cat education",
        465,
        0.05,
        [
            (
                492,
                '<tspan fill="#e6edf3">msc</tspan><tspan fill="#8b949e"> — école polytechnique, paris (data science) · </tspan>'
                '<tspan fill="#e6edf3">b.e.</tspan><tspan fill="#8b949e"> — national institute of engineering</tspan>',
                28,
            )
        ],
    ),
]

FINAL_PROMPT_Y = 526
IDLE, GAP_OUT, GAP_LINE, OUT_STEP = 0.4, 0.15, 0.25, 0.15


def fmt(t: float) -> str:
    return f"{t:.2f}s"


def steps(start: int, n: int) -> str:
    return ";".join(str(start + CHAR * i) for i in range(n + 1))


parts: list[str] = []
defs: list[str] = []
t = 0.15

for idx, (cmd, y, char_t, outs) in enumerate(LINES):
    n = len(cmd)
    show, type_b = t, t + IDLE
    type_d = n * char_t
    out_t = type_b + type_d + GAP_OUT
    cid = f"c{idx}"
    defs.append(
        f'<clipPath id="{cid}"><rect x="{X_CMD}" y="{y - 16}" width="0" height="22">'
        f'<animate attributeName="width" values="{steps(0, n)}" calcMode="discrete" '
        f'begin="{fmt(type_b)}" dur="{fmt(type_d)}" fill="freeze"/></rect></clipPath>'
    )
    parts.append(f'<!-- {cmd.split()[0].lstrip("./")} -->')
    parts.append(
        f'<text x="{X_PROMPT}" y="{y}" fill="#3fb950" opacity="0">$'
        f'<set attributeName="opacity" to="1" begin="{fmt(show)}" fill="freeze"/></text>'
    )
    parts.append(
        f'<g clip-path="url(#{cid})"><text x="{X_CMD}" y="{y}" fill="#e6edf3" '
        f'textLength="{CHAR * n}" lengthAdjust="spacing">{cmd}</text></g>'
    )
    parts.append(
        f'<rect x="{X_CMD}" y="{y - 14}" width="{CURSOR_W}" height="{CURSOR_H}" fill="#e6edf3" opacity="0">'
        f'<set attributeName="opacity" to="0.85" begin="{fmt(show)}"/>'
        f'<animate attributeName="x" values="{steps(X_CMD, n)}" calcMode="discrete" '
        f'begin="{fmt(type_b)}" dur="{fmt(type_d)}" fill="freeze"/>'
        f'<set attributeName="opacity" to="0" begin="{fmt(out_t)}" fill="freeze"/></rect>'
    )
    for j, (oy, inner, ox) in enumerate(outs):
        parts.append(
            f'<text x="{ox}" y="{oy}" opacity="0">{inner}'
            f'<set attributeName="opacity" to="1" begin="{fmt(out_t + OUT_STEP * j)}" fill="freeze"/></text>'
        )
    t = out_t + OUT_STEP * (len(outs) - 1) + GAP_LINE

parts.append("<!-- final prompt + blinking cursor -->")
parts.append(
    f'<text x="{X_PROMPT}" y="{FINAL_PROMPT_Y}" fill="#3fb950" opacity="0">$'
    f'<set attributeName="opacity" to="1" begin="{fmt(t)}" fill="freeze"/></text>'
)
parts.append(
    f'<rect x="{X_CMD}" y="{FINAL_PROMPT_Y - 14}" width="{CURSOR_W}" height="{CURSOR_H}" fill="#e6edf3" opacity="0">'
    f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.01;0.5;0.51;1" '
    f'begin="{fmt(t)}" dur="1.2s" repeatCount="indefinite"/></rect>'
)

body = "\n  ".join(parts)
defs_xml = "\n    ".join(defs)
svg = f"""<svg viewBox="0 0 860 556" xmlns="http://www.w3.org/2000/svg" font-family="ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace" font-size="15">
  <defs>
    {defs_xml}
  </defs>

  <!-- window -->
  <rect x="1" y="1" width="858" height="554" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>
  <circle cx="26" cy="24" r="7" fill="#ff5f57"/>
  <circle cx="48" cy="24" r="7" fill="#febc2e"/>
  <circle cx="70" cy="24" r="7" fill="#28c840"/>
  <text x="430" y="29" text-anchor="middle" fill="#8b949e" font-size="13">akshay@internet-zero — zsh</text>
  <line x1="1" y1="44" x2="859" y2="44" stroke="#21262d"/>

  {body}
</svg>
"""

from pathlib import Path

out = str(Path(__file__).parent / "terminal.svg")
with open(out, "w") as f:
    f.write(svg)
print(f"wrote {out}, total timeline ≈ {t:.2f}s")
