import MetaTrader5 as mt5
from config.settings import BOT_MAGIC,ORDER_DEVIATION
FILLINGS=lambda:[getattr(mt5,"ORDER_FILLING_FOK",0),getattr(mt5,"ORDER_FILLING_IOC",1),getattr(mt5,"ORDER_FILLING_RETURN",2)]
def own_positions(symbol=None):
    positions=mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()
    return [p for p in (positions or []) if getattr(p,"magic",None)==BOT_MAGIC]
def modify_sl(position,new_sl,comment):
    result=mt5.order_send({"action":mt5.TRADE_ACTION_SLTP,"position":position.ticket,"symbol":position.symbol,"sl":new_sl,"tp":position.tp,"magic":BOT_MAGIC,"comment":comment})
    return result if result and result.retcode==mt5.TRADE_RETCODE_DONE else None
def close_position(position,volume=None,comment="Prime T close"):
    tick=mt5.symbol_info_tick(position.symbol)
    if not tick:return None
    is_buy=position.type==mt5.POSITION_TYPE_BUY; request={"action":mt5.TRADE_ACTION_DEAL,"position":position.ticket,"symbol":position.symbol,"volume":volume or position.volume,"type":mt5.ORDER_TYPE_SELL if is_buy else mt5.ORDER_TYPE_BUY,"price":tick.bid if is_buy else tick.ask,"deviation":ORDER_DEVIATION,"magic":BOT_MAGIC,"comment":comment,"type_time":mt5.ORDER_TIME_GTC}
    for filling in FILLINGS():
        request["type_filling"]=filling; result=mt5.order_send(request)
        if result and result.retcode==mt5.TRADE_RETCODE_DONE:return result
    return None
