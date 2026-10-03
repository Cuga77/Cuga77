#!/usr/bin/env python3
"""Генерирует SVG для профиля: шапку и карточки проектов, RU и EN, светлая и тёмная темы.

Шрифт Onest (SIL OFL) встраивается в каждый SVG: картинки в README не могут
подгружать внешние шрифты. Google Fonts отдаёт подмножество только с нужными
символами, поэтому файл весит несколько килобайт.

Запуск: python3 assets/gen.py  (нужен доступ в интернет)
"""
import base64
import re
import urllib.parse
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

ACCENT = "#2b5cff"
THEMES = {
    "light": dict(card="#f3f4f6", title="#16171a", text="#5e626b", muted="#8b8f97"),
    "dark": dict(card="#232428", title="#f5f5f7", text="#b4b7bd", muted="#80848c"),
}

FONT = "Onest,'Segoe UI',Helvetica,Arial,sans-serif"

# slug и стек одинаковы для обоих языков
PROJECTS = [
    ("food-delivery-platform", ["Go", "PostgreSQL", "OpenAPI", "k6"]),
    ("comix_search", ["Go", "gRPC", "NATS", "PostgreSQL"]),
    ("reviewer_assignment", ["Go", "PostgreSQL", "k6"]),
    ("CIS-engine", ["Go", "PostgreSQL", "Kubernetes"]),
    ("loglinter", ["Go", "golangci-lint"]),
    ("codecrafters-shell-go", ["Go"]),
]

# язык -> slug -> (описание в 2 строки, значение, подпись)
TEXT = {
    "ru": {
        "food-delivery-platform": (["B2C + B2B API, вебхуки, Transactional Outbox,", "идемпотентность, ноль перепродаж"],
                                   "1600/с", "заказов, p99 ≤ 17 мс"),
        "comix_search": (["Поиск на микросервисах: gRPC, события через", "NATS, стемминг и инвертированный индекс"],
                         "37 мс", "p95 под нагрузкой"),
        "reviewer_assignment": (["Назначение ревьюеров для PR, фоновая очередь", "на FOR UPDATE SKIP LOCKED"],
                                "141 RPS", "p95 = 83 мс, 0 % ошибок"),
        "CIS-engine": (["Краулер, индексатор и поисковый API,", "CLI с релизами под Windows, macOS, Linux"],
                       "3 ОС", "релизы через GoReleaser"),
        "loglinter": (["Плагин golangci-lint: проверяет вызовы slog / zap", "и ловит утечки секретов в логах"],
                      "4 правила", "на go/analysis и go/types"),
        "codecrafters-shell-go": (["POSIX-оболочка: конвейеры, перенаправления,", "история и автодополнение по Tab"],
                                  "POSIX", "pipes и redirects"),
    },
    "en": {
        "food-delivery-platform": (["B2C + B2B API, webhooks, transactional outbox,", "idempotency, zero overselling"],
                                   "1600/s", "orders, p99 ≤ 17 ms"),
        "comix_search": (["Microservice search: gRPC, NATS events,", "stemming and an in-memory inverted index"],
                         "37 ms", "p95 under load"),
        "reviewer_assignment": (["Assigns PR reviewers, background job queue", "on FOR UPDATE SKIP LOCKED"],
                                "141 RPS", "p95 = 83 ms, 0% errors"),
        "CIS-engine": (["Crawler, indexer and search API,", "CLI released for Windows, macOS and Linux"],
                       "3 OSes", "released with GoReleaser"),
        "loglinter": (["golangci-lint plugin that checks slog / zap calls", "and catches secrets leaking into logs"],
                      "4 rules", "built on go/analysis"),
        "codecrafters-shell-go": (["POSIX shell: pipelines, redirections,", "history and Tab completion"],
                                  "POSIX", "pipes and redirects"),
    },
}

# имя, роль, подпись
HEADER = {
    "ru": ("Илья Богатов", "Backend-разработчик на Go и Rust", "Санкт-Петербург · магистратура ЛЭТИ"),
    "en": ("Ilya Bogatov", "Backend developer, Go and Rust", "Saint Petersburg · ETU LETI"),
}
PILLS = ["Go", "Rust", "PostgreSQL"]
ARROW = "→"


def all_chars():
    chars = set(ARROW + "".join(PILLS))
    for lang, items in TEXT.items():
        chars.update("".join(HEADER[lang]))
        for desc, value, label in items.values():
            chars.update("".join(desc) + value + label)
    for slug, stack in PROJECTS:
        chars.update(slug + " · ".join(stack))
    return "".join(sorted(chars))


def font_face():
    url = ("https://fonts.googleapis.com/css2?family=Onest:wght@400;500;700&text="
           + urllib.parse.quote(all_chars()))
    # без браузерного User-Agent Google Fonts отдаёт TTF вместо woff2
    ua = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
    css = urllib.request.urlopen(urllib.request.Request(url, headers=ua)).read().decode()
    font_url = re.search(r"url\((\S+?)\) format\('woff2'\)", css).group(1)
    data = base64.b64encode(urllib.request.urlopen(font_url).read()).decode()
    return (f"@font-face{{font-family:Onest;font-weight:400 700;"
            f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")


def text_width(s, size):
    # грубая оценка ширины гротеска для плашек в шапке
    return sum(0.64 if c.isupper() or c.isdigit() else 0.54 for c in s) * size


def header(lang, face):
    w, h = 880, 240
    name, role, sub = HEADER[lang]
    pills, y = [], 44
    for i, p in enumerate(PILLS):
        pw = text_width(p, 22) + 48
        x = w - 48 - pw - (0, 56, 20)[i]
        pills.append(
            f'<rect x="{x:.0f}" y="{y}" width="{pw:.0f}" height="48" rx="24" fill="#ffffff"/>'
            f'<text x="{x + pw / 2:.0f}" y="{y + 32}" text-anchor="middle" font-size="22" font-weight="500" fill="#16171a">{p}</text>')
        y += 48 + 10
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{face}</style>
<rect width="{w}" height="{h}" rx="28" fill="{ACCENT}"/>
<g font-family="{FONT}" fill="#ffffff">
  {"".join(pills)}
  <text x="48" y="104" font-size="54" font-weight="700" letter-spacing="-1.5">{escape(name)}</text>
  <text x="48" y="148" font-size="24" font-weight="500">{escape(role)}</text>
  <text x="48" y="196" font-size="17" fill="#ffffff" fill-opacity="0.75">{escape(sub)}</text>
</g>
</svg>
'''


def card(t, face, slug, stack, desc, value, label):
    w, h = 430, 228
    desc_svg = "".join(
        f'<text x="28" y="{108 + i * 21}" font-size="14.5" fill="{t["text"]}">{escape(line)}</text>'
        for i, line in enumerate(desc))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>{face}</style>
<rect width="{w}" height="{h}" rx="24" fill="{t["card"]}"/>
<g font-family="{FONT}">
  <text x="28" y="44" font-size="13" fill="{t["muted"]}">{escape(" · ".join(stack))}</text>
  <text x="28" y="76" font-size="21" font-weight="700" letter-spacing="-0.3" fill="{t["title"]}">{escape(slug)}</text>
  {desc_svg}
  <text x="28" y="162" font-size="13.5" fill="{t["muted"]}">{escape(label)}</text>
  <text x="28" y="196" font-size="34" font-weight="700" letter-spacing="-0.8" fill="{t["title"]}">{escape(value)}</text>
  <circle cx="{w - 48}" cy="{h - 46}" r="22" fill="{ACCENT}"/>
  <text x="{w - 48}" y="{h - 39}" text-anchor="middle" font-size="20" font-weight="500" fill="#ffffff">{ARROW}</text>
</g>
</svg>
'''


face = font_face()
for lang in TEXT:
    suffix = "" if lang == "ru" else f"-{lang}"
    # шапка одинаковая в обеих темах; оба файла остаются, чтобы не менять README
    for name, t in THEMES.items():
        (OUT / f"header-{name}{suffix}.svg").write_text(header(lang, face))
        for slug, stack in PROJECTS:
            (OUT / f"{slug}-{name}{suffix}.svg").write_text(card(t, face, slug, stack, *TEXT[lang][slug]))
