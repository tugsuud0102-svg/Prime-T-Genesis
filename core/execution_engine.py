from core.order_manager import place_order
def execute_decision(decision,volume,context=None):
    return place_order(decision.signal,decision.entry,decision.sl,decision.tp,volume=volume,context=context or {}) if decision.signal in ("BUY","SELL") else None
