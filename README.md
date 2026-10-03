### Илья Богатов

Backend / systems-разработчик · **Go** и **Rust** · Санкт-Петербург

Пишу сервисы, которые остаются корректными под конкурентной нагрузкой, и серверы реального времени.
Сейчас — авторитетный сервер модульной платформы симуляции на Rust (Bevy ECS, UDP, Wasm-компоненты с транзакционным откатом).
Магистратура СПбГЭТУ «ЛЭТИ».

---

#### Избранные проекты

| | |
|---|---|
| [**food-delivery-platform**](https://github.com/Cuga77/food-delivery-platform) | Доставка еды: B2C + B2B API, вебхуки, Transactional Outbox, идемпотентность. **1600 заказов/с, p99 ≤ 17 мс**, ноль перепродаж при 200 параллельных клиентах.<br><sub>Go · PostgreSQL · OpenAPI · k6</sub> |
| [**comix_search**](https://github.com/Cuga77/comix_search) | Поиск на микросервисах: gRPC, события через NATS, полнотекстовый поиск с лемматизацией. **p95 = 37 мс**, краулер в 6 раз быстрее последовательного.<br><sub>Go · gRPC · NATS · PostgreSQL · Vue</sub> |
| [**reviewer_assignment**](https://github.com/Cuga77/reviewer_assignment) | Назначение ревьюеров для PR, фоновая очередь на `FOR UPDATE SKIP LOCKED`. **~141 RPS при p95 = 83 мс**, 0 % ошибок.<br><sub>Go · PostgreSQL · k6</sub> |
| [**loglinter**](https://github.com/Cuga77/loglinter) | Плагин golangci-lint: проверяет вызовы `slog` / `zap` и ищет утечки секретов в логах.<br><sub>Go · go/analysis · go/types</sub> |
| [**CIS-engine**](https://github.com/Cuga77/CIS-engine) | Поисковый движок: краулер, индексатор и API, CLI с релизами под три ОС.<br><sub>Go · PostgreSQL · GoReleaser · testcontainers</sub> |
| [**codecrafters-shell-go**](https://github.com/Cuga77/codecrafters-shell-go) | POSIX-совместимая оболочка: конвейеры, перенаправления, история, автодополнение.<br><sub>Go</sub> |

---

#### Стек

**Go** — net/http, chi, Gin, gRPC, pgx, go/analysis  
**Rust** — Bevy (ECS), Lightyear, Wasmtime / WIT, Rapier  
**Данные** — PostgreSQL, NATS, MongoDB  
**Инфраструктура** — Docker, GitHub Actions, GitLab CI, k6, Tracy

---

[Telegram](https://t.me/ibogatov999) · [bigatov2021@yandex.ru](mailto:bigatov2021@yandex.ru)
