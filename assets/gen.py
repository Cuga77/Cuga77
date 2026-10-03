#!/usr/bin/env python3
"""Генерирует SVG для профиля: шапку и карточки проектов в тёмной и светлой темах.

Запуск: python3 assets/gen.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

THEMES = {
    "dark": dict(bg="#0d1117", card="#161b22", border="#30363d", text="#e6edf3",
                 muted="#8b949e", accent="#00add8", accent2="#f0883e", chip="#1f2a37", grid="#21262d"),
    "light": dict(bg="#ffffff", card="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#59636e", accent="#0a7ea4", accent2="#c4500f", chip="#e6f1f6", grid="#eaeef2"),
}

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

PROJECTS = [
    # slug, описание (2 строки), значение, подпись, стек
    ("food-delivery-platform",
     ["B2C + B2B API, вебхуки, Transactional Outbox,", "идемпотентность, ноль перепродаж"],
     "1600/с", "заказов · p99 ≤ 17 мс", ["Go", "PostgreSQL", "OpenAPI", "k6"]),
    ("comix_search",
     ["Поиск на микросервисах: gRPC, события через", "NATS, полнотекстовый поиск с лемматизацией"],
     "37 мс", "p95 под нагрузкой", ["Go", "gRPC", "NATS", "PostgreSQL"]),
    ("reviewer_assignment",
     ["Назначение ревьюеров для PR, фоновая очередь", "на FOR UPDATE SKIP LOCKED"],
     "141 RPS", "p95 = 83 мс · 0 % ошибок", ["Go", "PostgreSQL", "k6"]),
    ("loglinter",
     ["Плагин golangci-lint: проверяет вызовы slog / zap", "и ловит утечки секретов в логах"],
     "AST", "go/analysis · go/types", ["Go", "golangci-lint"]),
    ("CIS-engine",
     ["Краулер, индексатор и поисковый API,", "CLI с релизами под Windows, macOS, Linux"],
     "3 ОС", "GoReleaser · testcontainers", ["Go", "PostgreSQL", "Kubernetes"]),
    ("codecrafters-shell-go",
     ["POSIX-оболочка: конвейеры, перенаправления,", "история и автодополнение по Tab"],
     "POSIX", "pipes · redirects", ["Go"]),
]


def header(t):
    w, h = 880, 230
    # граф «сервисов» справа: узлы и рёбра, по рёбрам бегут пакеты
    nodes = [(600, 70), (700, 45), (790, 95), (660, 140), (760, 180), (840, 150), (560, 175)]
    edges = [(0, 1), (1, 2), (0, 3), (3, 4), (2, 5), (4, 5), (3, 6), (1, 3), (2, 4)]
    lines, packets = [], []
    for i, (a, b) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{t["border"]}" stroke-width="1.5"/>')
        if i % 2 == 0:
            color = t["accent"] if i % 4 == 0 else t["accent2"]
            packets.append(
                f'<circle r="3" fill="{color}"><animateMotion dur="{2.4 + i * 0.35:.2f}s" '
                f'repeatCount="indefinite" path="M{x1},{y1} L{x2},{y2}"/></circle>')
    circles = "".join(
        f'<circle cx="{x}" cy="{y}" r="7" fill="{t["card"]}" stroke="{t["accent"] if i % 3 else t["accent2"]}" stroke-width="2"/>'
        for i, (x, y) in enumerate(nodes))
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="1" fill="{t["grid"]}"/>'
        for x in range(500, w, 20) for y in range(10, h, 20))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>
  .cursor {{ animation: blink 1.1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
</style>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{t["card"]}" stroke="{t["border"]}"/>
{dots}
{"".join(lines)}{"".join(packets)}{circles}
<g font-family="{FONT}">
  <text x="44" y="62" font-family="{MONO}" font-size="14" fill="{t["accent"]}">// backend · systems</text>
  <text x="42" y="112" font-size="44" font-weight="700" fill="{t["text"]}">Илья Богатов</text>
  <text x="44" y="146" font-size="18" fill="{t["muted"]}">Сервисы на <tspan fill="{t["accent"]}" font-weight="600">Go</tspan> и серверы реального времени на <tspan fill="{t["accent2"]}" font-weight="600">Rust</tspan></text>
  <text x="44" y="192" font-family="{MONO}" font-size="14" fill="{t["muted"]}"><tspan fill="{t["accent"]}">$</tspan> go test -race ./... <tspan fill="#3fb950">ok</tspan><tspan class="cursor" fill="{t["text"]}"> ▍</tspan></text>
</g>
</svg>
'''


def card(t, slug, desc, value, label, stack):
    w, h = 430, 170
    chips, x = [], 24
    for s in stack:
        cw = 16 + round(len(s) * 6.4)
        chips.append(
            f'<rect x="{x}" y="128" width="{cw}" height="22" rx="11" fill="{t["chip"]}"/>'
            f'<text x="{x + cw / 2}" y="143" text-anchor="middle" font-size="11.5" fill="{t["accent"]}">{escape(s)}</text>')
        x += cw + 6
    desc_svg = "".join(
        f'<text x="24" y="{84 + i * 19}" font-size="13" fill="{t["muted"]}">{escape(line)}</text>'
        for i, line in enumerate(desc))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>
<rect x="0.5" y="22" width="3" height="40" rx="1.5" fill="{t["accent"]}"/>
<g font-family="{FONT}">
  <text x="24" y="40" font-family="{MONO}" font-size="15" font-weight="700" fill="{t["text"]}">{escape(slug)}</text>
  <text x="{w - 24}" y="38" text-anchor="end" font-size="20" font-weight="700" fill="{t["accent2"]}">{escape(value)}</text>
  <text x="{w - 24}" y="56" text-anchor="end" font-size="11" fill="{t["muted"]}">{escape(label)}</text>
  {desc_svg}
  {"".join(chips)}
</g>
</svg>
'''


for name, t in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(t))
    for p in PROJECTS:
        (OUT / f"{p[0]}-{name}.svg").write_text(card(t, *p))
