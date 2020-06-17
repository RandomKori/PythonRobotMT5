import MetaTrader5 as mt5

def OnTick():
    print("OnTick")
    return

mt5.initialize()
v=mt5.version()
print(v)

d=mt5.symbol_info_tick("EURUSD").time_msc;
while(True):
    tick=mt5.symbol_info_tick("EURUSD")
    print(tick)
    if tick.time_msc!=d:
        d=tick.time_msc
        OnTick()
