import MetaTrader5 as mt5
import random as rnd
import datetime
from dateutil.relativedelta import relativedelta

TP=300
SL=300
Lot=0.01
deviation=20
magic=777
symbol="EURUSD"

def OnLot():
    l=Lot
    from_date=datetime.datetime(2020,1,1)
    to_date=datetime.datetime.today()+relativedelta(days=+1)
    pos=None
    pos=mt5.history_deals_get(from_date, to_date)
    if pos!=None:
        p=len(pos)
        while(p>0):
            p=p-1
            ps=pos[p].type
            print(pos[p])
            if ps==0 or ps==1:
                if pos[p].profit<0.0:
                    l=pos[p].volume*2
                break
    return l

def OnTick():
    print("OnTick")
    if mt5.positions_total()==0:
        n=rnd.random()
        if n>0.5:
            print("Buy")
            point = mt5.symbol_info(symbol).point
            price = mt5.symbol_info_tick(symbol).ask
            request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": symbol,
                        "volume": OnLot(),
                        "type": mt5.ORDER_TYPE_BUY,
                        "price": price,
                        "sl": price - SL * point,
                        "tp": price + TP * point,
                        "deviation": deviation,
                        "magic": magic,
                        "comment": "python script open",
                        "type_time": mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_FOK,
                    }
            result = mt5.order_send(request)
            print("Error ",result.retcode)
        else:
            print("Sell")
            point = mt5.symbol_info(symbol).point
            price = mt5.symbol_info_tick(symbol).bid
            request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": symbol,
                        "volume": OnLot(),
                        "type": mt5.ORDER_TYPE_SELL,
                        "price": price,
                        "sl": price + SL * point,
                        "tp": price - TP * point,
                        "deviation": deviation,
                        "magic": magic,
                        "comment": "python script open",
                        "type_time": mt5.ORDER_TIME_GTC,
                        "type_filling": mt5.ORDER_FILLING_FOK,
                    }
            result = mt5.order_send(request)
            print("Error ",result.retcode)
    return

mt5.initialize()
v=mt5.version()
print(v)

rnd.seed()
d=mt5.symbol_info_tick(symbol).time_msc;
while(True):
    tick=mt5.symbol_info_tick(symbol)
    if tick.time_msc!=d:
        d=tick.time_msc
        OnTick()
