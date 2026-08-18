# Prime T Genesis v4.1.3 Recovery Report

Recovered the requested modular architecture from the v2.1 baseline on `recover-v4`.

## Implemented

- Modular market snapshot, entry decision, score, execution, and signal orchestration.
- Confirmed swing structure, BOS, CHoCH, MSS, liquidity pools/sweeps, FVG, order blocks, supply/demand, support/resistance, price action, premium/discount, EMA slope, and MTF confluence.
- BOT_MAGIC-scoped break-even, partial close persistence, ATR trailing, smart exits, time exits, and close-all behavior.
- SQLite `OPEN -> CLOSED` lifecycle, safe migrations, deal synchronization, and performance analysis.
- Telegram v4.1.3 commands, inline callbacks, stale-update/chat validation, confirmation menu, and UTF-8 messages.
- Realized-deal daily target calculation; floating P/L is excluded.
- Continuous fault-isolated runner with the requested 900-second default.

## Preserved

Versioned `*_before_v413.py` backups preserve the important v2.1 sources. Existing risk sizing, position limits, equity guard, sessions, news/ForexFactory, dashboards, journal, backtest, optimizer, portfolio, launcher, logging, and environment-based Telegram credentials remain available.

## Validation

- Recursive compileall: passed (external `.venv` excluded).
- Focused imports and score/MTF/Telegram assertions: passed.
- Statistics database migration and analyzer CLI: passed.
- `main.py` safe one-cycle smoke test: passed without order execution; local MT5 returned IPC timeout, which is handled as `NO_TRADE`.

## Environment note

The repository venv points to a missing Python installation. Validation used an available Python 3.12 runtime with the project dependencies. Recreate the local venv before deployment. No LIVE mode or test order was enabled.
