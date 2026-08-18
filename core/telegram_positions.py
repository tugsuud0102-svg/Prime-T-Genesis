"""Read-only Telegram dashboard for Prime T Genesis MT5 positions."""
from datetime import datetime, timezone

import MetaTrader5 as mt5

from config.settings import BOT_MAGIC
from core.mt5_connection import initialize_mt5


def _original_sl_by_position():
    """Load the entry-time SL recorded after execution, never the moved MT5 SL."""
    try:
        from trade_stats.database import connect, initialize_database

        initialize_database()
        with connect() as db:
            rows = db.execute(
                "SELECT position_id, ticket, sl FROM trades "
                "WHERE status='OPEN' AND sl IS NOT NULL AND sl != 0"
            ).fetchall()
        result = {}
        for position_id, ticket, sl in rows:
            if position_id is not None:
                result[int(position_id)] = float(sl)
            if ticket is not None:
                result[int(ticket)] = float(sl)
        return result
    except Exception as exc:
        print("Positions original-risk lookup skipped:", exc)
        return {}


def read_prime_positions():
    """Return BOT_MAGIC positions plus symbol digits, or None if MT5 is unavailable."""
    if not initialize_mt5():
        print("Positions MT5 connection unavailable:", mt5.last_error())
        return None
    try:
        positions = [
            position
            for position in (mt5.positions_get() or [])
            if getattr(position, "magic", None) == BOT_MAGIC
        ]
        digits = {}
        for position in positions:
            info = mt5.symbol_info(position.symbol)
            digits[position.symbol] = int(getattr(info, "digits", 2) or 2)
        return positions, digits, _original_sl_by_position()
    finally:
        mt5.shutdown()


def _age_text(open_timestamp, now=None):
    now = now or datetime.now(timezone.utc)
    opened = datetime.fromtimestamp(float(open_timestamp), timezone.utc)
    minutes = max(0, int((now - opened).total_seconds() // 60))
    days, remainder = divmod(minutes, 1440)
    hours, mins = divmod(remainder, 60)
    if days:
        return f"{days}d {hours}h {mins}m"
    if hours:
        return f"{hours}h {mins}m"
    return f"{mins}m"


def _r_text(position, current_price, original_sl):
    if original_sl is None:
        return "N/A"
    entry = float(position.price_open)
    risk = abs(entry - float(original_sl))
    if risk <= 0:
        return "N/A"
    is_buy = position.type == mt5.POSITION_TYPE_BUY
    reward = current_price - entry if is_buy else entry - current_price
    return f"{reward / risk:+.2f}R"


def render_positions_dashboard(
    positions,
    digits_by_symbol=None,
    original_sl_by_ticket=None,
    now=None,
):
    digits_by_symbol = digits_by_symbol or {}
    original_sl_by_ticket = original_sl_by_ticket or {}
    lines = ["📈 PRIME T POSITIONS", ""]
    if not positions:
        return "\n".join(lines + ["No open Prime T positions."])

    total_profit = 0.0
    for number, position in enumerate(positions, 1):
        digits = digits_by_symbol.get(position.symbol, 2)
        current = float(getattr(position, "price_current", 0) or 0)
        direction = "BUY" if position.type == mt5.POSITION_TYPE_BUY else "SELL"
        profit = float(getattr(position, "profit", 0) or 0)
        total_profit += profit
        original_sl = original_sl_by_ticket.get(int(position.ticket))
        lines.extend(
            [
                f"#{number} {position.symbol} {direction}",
                f"Ticket: {position.ticket}",
                f"Volume: {float(position.volume):.2f}",
                f"Entry: {float(position.price_open):.{digits}f}",
                f"Current: {current:.{digits}f}",
                f"SL: {float(getattr(position, 'sl', 0) or 0):.{digits}f}",
                f"TP: {float(getattr(position, 'tp', 0) or 0):.{digits}f}",
                f"P/L: {profit:+.2f} USD",
                f"R: {_r_text(position, current, original_sl)}",
                f"Age: {_age_text(position.time, now)}",
                f"Magic: {position.magic}",
                "",
            ]
        )
    lines.extend(
        [
            f"Open positions: {len(positions)}",
            f"Total floating P/L: {total_profit:+.2f} USD",
        ]
    )
    return "\n".join(lines)


def build_live_positions_dashboard():
    result = read_prime_positions()
    if result is None:
        return "⚠️ MT5 connection unavailable.\nPlease try Refresh again."
    positions, digits, original_sl = result
    return render_positions_dashboard(positions, digits, original_sl)
