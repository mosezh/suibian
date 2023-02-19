

'''backtest
start: 2022-01-18 00:00:00
end: 2022-02-02 05:20:00
period: 1h
basePeriod: 1m
exchanges: [{"eid":"Futures_Binance","currency":"ETH_USDT","balance":800}]
args: [["gang",10],["zhou",49],["zhou2",0.1],["zengfu",0.05],["jizhun",7],["cankao",81],["qujianbeilv1",1.3],["shijian",0]]
'''

import sys
import json
import talib
import cmath
from numpy import *
from datetime import *
import time
#from datetime import datetime
#from datetime import datetime, date
#from datetime import timedelta
import time, datetime
基准线=jizhun
参考线=cankao
ChartCfg = {
    '__isStock': True,#Highstocks图表：开启后更平滑，统一显示节点
    'title': {
        'text': '区间范围图标'
    },
    'yAxis': [{
        'title': {'text': 'K线'},
        'style': {'color': '#4572A7'},
        'opposite': False
    }, {
        'title': {'text': '指标轴'},
        'opposite': True #异步
    }],
    'series': [{
        'type': 'candlestick',#意思是k线类型的数据
        'name': 'K线',
        'id': 'primary',
        'data': []
    }, {
        'type': 'line',#线
        'id': 'jz',
        'name': '游动线',
        "yAxis" : 0,
        'data': []
    }, {
        'type': 'line',
        'id': 'ck',
        'name': '参考线',
        "yAxis" : 0,
        'data': []
    }, {
        'type': 'line',
        'id': 'gao',
        'name': '顶部线',
        "yAxis" : 0,
        'data': []
    }, {
        'type': 'line',
        'id': 'di',
        'name': '底部线',
        "yAxis" : 0,
        'data': []
    }, {
        'type': 'line',
        'id': 'd',
        'name': '基础动量',
        "yAxis" : 1,
        'data': []
    }, {
        'type': 'line',
        'id': 'd4',
        'name': '辅助动量',
        "yAxis" : 1,
        'data': []
    }, {
        'type': 'line',
        'id': 'd15',
        'name': '敏感动量',
        "yAxis" : 1,
        'data': []
    }]
}
账户状态值 = {'空仓':0,'买入':0,'出售':0,'区间钝化结束时间':'','区间可执行':0,'异动止盈': yidong}
首位挂单 = {'买单id':-1,'卖单id':-1}
账户状态值['买入'] = mai
账户状态值['出售'] = shou
持仓信息 = {'历史持仓百分比':0,'持仓百分比':0,'历史持仓时间':''}
订单池状态 = {}
杠杆 = gang #对接fmz策略参数
卖出的比例 = {
    0:0.1,1:0.11,2:0.13,3:0.14,4:0.17,5:0.2,6:0.25,7:0.33,8:0.5,9:1
}
止盈点位 = {}
总充入 = 0
充入 = 0

def main():
    账户状态值['区间钝化结束时间'] = _D(0)
    global ChartCfg
    LogProfitReset()
    preTime = 0
    chart = Chart(ChartCfg)
    chart.reset()
    正数差=[]
    负数差=[]
    交易量=[]
    交易量补正倍率 = 0
    顶部线 = None
    底部线 = None
    exchange.SetContractType("swap")#设定合约类型
    #exchange.SetMarginLevel(5)#杠杆倍数
    #exchange.SetDirection("buy")#开仓方向
    #exchange.Buy(5000, 0.01)#挂单价格，货币数量
    #position = exchange.GetPosition()
    Log('策略正常启动') 
    Account = _C(exchange.GetAccount)
    position = _C(exchange.GetPosition)
    if len(position) > 0:
        position = position
    else:
        position = {0:{'Margin':0}}    
    Log('当前账户可用资产',Account['Balance'],'冻结金额',Account['FrozenBalance'],'仓位占用保证金',position[0]['Margin'])
    初始资产 = Account['Balance'] + Account['FrozenBalance'] + position[0]['Margin']
    Log('初始资产',初始资产)
    总充入 = 0
    充入 = 0
    周期 = zhou
    回存 = zhou2
    if buchang1 != 0:
        for i in range(int(周期*回存)):
            正数差.append(buchang1)
    if buchang2 != 0:
        for i in range(int(周期*回存)):
            负数差.append(buchang2)             
    打印={'打印利润时间套娃':0}
    打印['初始化时间'] = _D()
    打印['初始化时间'] = datetime.datetime.strptime(打印['初始化时间'],'%Y-%m-%d %H:%M:%S')   
    k线计数 = 0   
    kd数据 = {'k': None, 'd': None, 'k4': None, 'd4': None, 'k15': None, 'd15': None, '对应时间': 0}
    while True:
        if k线计数 == 1:
            K线长度 = _N(参考线*2.5,0)
            K线长度 = int(K线长度)            
            exchange.SetMaxBarLen(K线长度)#正常运行后的k线长度
            r = _C(exchange.GetRecords)
            kd参考时间 = kdzhouqi*60*60
            r4 = _C(exchange.GetRecords,kd参考时间)
            敏感kd参考时间 = 60/kdzhouqi*60
            r15 = _C(exchange.GetRecords,敏感kd参考时间)
            while  len(r) > K线长度 :
                r.pop(0)
            while  len(r4) > K线长度 :
                r4.pop(0)
            while  len(r15) > K线长度 :
                r15.pop(0)        
            #Log(len(r),1,参考线+基准线)
            k线计数 = 2
        elif k线计数 == 0 :
            K线长度 = _N(参考线*2.5,0)
            K线长度 = int(K线长度)             
            exchange.SetMaxBarLen(K线长度)#首次获取k线长度  
            kd参考时间 = kdzhouqi*60*60
            r4 = _C(exchange.GetRecords,kd参考时间)
            r = _C(exchange.GetRecords)
            敏感kd参考时间 = 60/kdzhouqi*60
            r15 = _C(exchange.GetRecords,敏感kd参考时间)
            #Log(len(r),0,参考线*2+基准线)   
        elif k线计数 == 2 :
            K线长度 = _N(参考线*2.5,0)
            K线长度 = int(K线长度)             
            r = _C(exchange.GetRecords)
            kd参考时间 = kdzhouqi*60*60
            r4 = _C(exchange.GetRecords,kd参考时间)
            敏感kd参考时间 = 60/kdzhouqi*60
            r15 = _C(exchange.GetRecords,敏感kd参考时间)
            while  len(r) > K线长度 :
                r.pop(0)
            while  len(r4) > K线长度 :
                r4.pop(0)
            while  len(r15) > K线长度 :
                r15.pop(0)      
        
        position = _C(exchange.GetPosition)
        ticker = _C(exchange.GetTicker)
        Account = _C(exchange.GetAccount)
        #Log(position)
        #boom(position)#回测的时候这个要激活，实盘反正交易所自动会给你爆仓
        持仓信息 = onTick(position,ticker,Account,交易量补正倍率,账户状态值)
        #onTick(position,ticker,Account)
        
        
        #ema(9)
        
        #exchange.SetMaxBarLen(参考线*2+基准线) #首次获取k线长度 
        #获取行情数据
        #kd参考时间 = kdzhouqi*60*60
        #r4 = _C(exchange.GetRecords,kd参考时间)
        #r = _C(exchange.GetRecords)
        #敏感kd参考时间 = 60/kdzhouqi*60
        #r15 = _C(exchange.GetRecords,敏感kd参考时间)
        # 计算指标
        #Log(len(r),1,参考线+基准线)
        EMA5 = TA.EMA(r,基准线)
        EMA60 = TA.EMA(r,参考线)
        #Sleep(50)
        #交易规则(正数差,负数差,EMA5,position,账户状态值,持仓信息,ticker,杠杆) 
        #交易规则要放到画完图后面，不然数组没数据
        #rsi = TA.KDJ(r, 14, 1, 3)#取用D指标小于20时可以买入建仓
        rsi = talib.STOCH(r.High, r.Low, r.Close,5,3,0,3,0)
        rsi4 = talib.STOCH(r4.High, r4.Low, r4.Close,5,3,0,3,0)#取用d指标小于25时可以买入建仓#取用指标小于20时可以买入建仓
        rsi15 = talib.STOCH(r15.High, r15.Low, r15.Close,5,3,0,3,0)
        kd = 处理kd数据(rsi,r)
        kd4 = 处理kd数据(rsi4,r4)
        kd15 = 处理kd数据(rsi15,r15)
        kdzong = kd整合(kd,kd4,kd15)
        
        #K线时间 = _D()
        #r = _C(exchange.GetRecords)
        #K线时间 = datetime.strptime(K线时间,'%Y-%m-%d %H:%M:%S')
        #Log(K线时间)
        #Log(_D(r[len(r)-1]['Time']))
        #sys.exit()  
        #LogStatus(_D(), len(r))
        #Log (总充入,初始资产)
        总充入 = 按钮信息(总充入,初始资产)
        #Log (总充入,初始资产)
        打印时间间隔 = timedelta(hours=1)
        if 打印['打印利润时间套娃'] == 0:
            打印['打印利润时间套娃'] = 打印['初始化时间'] + 打印时间间隔
            打印['打印利润时间套娃'] = str(打印['打印利润时间套娃'])
        打印当前时间 = _D()
        打印当前时间 = int(time.mktime(time.strptime(打印当前时间,'%Y-%m-%d %H:%M:%S')))
        ty = type(打印['打印利润时间套娃']) 
        if ty != int :
            打印['打印利润时间套娃'] = int(time.mktime(time.strptime(打印['打印利润时间套娃'],'%Y-%m-%d %H:%M:%S')))
        if 打印['打印利润时间套娃'] <= 打印当前时间:
            总充入 = 打印利润(总充入,初始资产,充入)
            打印当前时间 = _D()
            打印当前时间 = datetime.datetime.strptime(打印当前时间,'%Y-%m-%d %H:%M:%S') 
            打印['打印利润时间套娃'] = 打印当前时间 + 打印时间间隔 
            打印['打印利润时间套娃'] = str(打印['打印利润时间套娃'])
            if k线计数 == 0 :
                k线计数 = 1

        #Log(区间可执行)     
        #sys.exit()                 
        # 画图
        for i in range(len(r)):
           

            负数差=检查数组长度(负数差)
            正数差=检查数组长度(正数差)
            if r[i]["Time"] == preTime:
                chart.add(0, [r[i]["Time"], r[i]["Open"], r[i]["High"], r[i]["Low"], r[i]["Close"]], -1)
                chart.add(1, [r[i]["Time"], EMA5[i]], -1)
                chart.add(2, [r[i]["Time"], EMA60[i]], -1)  
                if EMA60[i] is not None and EMA60[i] is not None:
                    顶部线 = EMA60[i]+获取列表平均数(正数差)*qujianbeilv
                    底部线 = EMA60[i]+获取列表平均数(负数差)*qujianbeilv1
                else:
                    顶部线 = None
                    底部线 = None
                时间戳 = kd[2][i]    
                kd数据 = 从时间戳取对应参数(时间戳,kd,kd4,kd15,kd数据)    
                
                chart.add(3, [r[i]["Time"], 顶部线], -1)
                chart.add(4, [r[i]["Time"], 底部线], -1 )
                chart.add(5, [r[i]["Time"], kd数据['d']],-1) 
                chart.add(6, [r[i]["Time"], kd数据['d4']],-1)            
                chart.add(7, [r[i]["Time"], kd数据['d15']],-1)   
                #Log(1)
                #sys.exit()              
            elif r[i]["Time"] > preTime: 
                chart.add(0, [r[i]["Time"], r[i]["Open"], r[i]["High"], r[i]["Low"], r[i]["Close"]])
                chart.add(1, [r[i]["Time"], EMA5[i]])
                chart.add(2, [r[i]["Time"], EMA60[i]])
                最近成交量 = r[i-1]["Volume"]               
                交易量.append(最近成交量)
                #交易量.append(获取列表平均数(交易量))
                交易量=检查数组长度(交易量)
                交易量补正倍率 = 最近成交量 / 获取列表平均数(交易量) 
                jxcz=均线差值运算(EMA5[i],EMA60[i],交易量补正倍率)
            #Log(len(r),len(负数差),len(正数差))
                if jxcz is not None and jxcz > 0:
                    正数差.append(jxcz)
                    正数组平均数 = 获取列表平均数(正数差)
                    正数差.append(正数组平均数)
                elif jxcz is not None and jxcz < 0:
                    负数差.append(jxcz)
                    负数组平均数 = 获取列表平均数(负数差)
                    负数差.append(负数组平均数)
                负数差=检查数组长度(负数差)
                正数差=检查数组长度(正数差)
                if EMA5[i] is not None and EMA60[i] is not None:
                    顶部线 = EMA60[i]+获取列表平均数(正数差)*qujianbeilv
                    底部线 = EMA60[i]+获取列表平均数(负数差)*qujianbeilv1
                else:
                    顶部线 = None
                    底部线 = None
                时间戳 = kd[2][i]    
                kd数据 = 从时间戳取对应参数(时间戳,kd,kd4,kd15,kd数据)    
                   
                chart.add(3, [r[i]["Time"], 顶部线])
                chart.add(4, [r[i]["Time"], 底部线])
                chart.add(5, [r[i]["Time"], kd数据['d']]) 
                chart.add(6, [r[i]["Time"], kd数据['d4']])            
                chart.add(7, [r[i]["Time"], kd数据['d15']])         
                preTime = r[i]["Time"]
                遍历并取消所有订单(2)

                #sys.exit()     
        交易规则(正数差,负数差,EMA5,EMA60,position,账户状态值,持仓信息,ticker,杠杆,交易量补正倍率,kdzong,kd,kd4,kd15)
        持仓信息 = onTick(position,ticker,Account,交易量补正倍率,账户状态值)
        
        #Log(mean(正数差),mean(负数差))
        
        Sleep(500)
def 均线差值运算(a,b,交易量补正倍率):

    if a is None or b is None:
         return None
    else:
        c=a-b
        c=c*交易量补正倍率
        return c     
def 检查数组长度(a):
    周期 = zhou
    while  len(a) >= 周期 :
        
        a.pop(0)
        a.pop(0)
        return a
    if len(a) < 周期 :
        return a
                      
def 获取列表平均数(a):
    if a is None:
        
        return 0
    elif len(a) > 0:
        
        b = mean(a)
        return b
    else:
        return 0
def boom(position):#止损/爆仓判断函数
    #position = exchange.GetPosition()
    if position is not None and len(position) > 0 :
        a = position[0]["Margin"]
        b = position[0]["Profit"]
        if a + b <= 0 and len(position) > 0 :    #止损判断保证金加浮动盈亏等于零，持有仓位回落大于50%
            Log("止损触发,#ff7f00")
            Log("本次盈亏",position[0]["Profit"] ,'持仓均价',position[0]["Price"])
            exchange.SetDirection("closebuy")
            ticker = _C(exchange.GetTicker)
            position = _C(exchange.GetPosition)
            持仓量 = position[0]["Amount"] 
            现价 = ticker["Sell"]
            遍历并取消所有订单(2)
            #实盘要改
            只减仓Sell(_N(现价-hua1,1),0,持仓量)
            #exchange.Sell(_N(现价-hua1,1),持仓量)
            账户状态值['出售'] = 0
            账户状态值['买入'] = 0
            账户状态值['空仓'] = 1       
def onTick(position,ticker,Account,交易量补正倍率,账户状态值): #显示持仓信息
    账户状态值['区间钝化结束时间'] = str(账户状态值['区间钝化结束时间'])
    账户状态值['区间钝化结束时间'] = datetime.datetime.strptime(账户状态值['区间钝化结束时间'],'%Y-%m-%d %H:%M:%S')  
    if len(position) > 0 and len(ticker) > 0 and len(Account) > 0:      
        持仓信息['持仓量'] = position[0]["Amount"]  
        持仓信息['持仓均价'] = position[0]["Price"]
        持仓信息['杠杆倍数'] = position[0]["MarginLevel"]
        持仓信息['现价'] = ticker["Last"]
        持仓信息['持仓金额'] = _N(position[0]["Amount"] * ticker["Last"],2)
        持仓信息['持仓金额显示'] = str(持仓信息['持仓量'])+'ETH  约等于'+str(持仓信息['持仓金额'])+'USDT'
        #持仓信息['爆仓价'] = _N((position[0]["Margin"]-position[0]["Margin"]*position[0]["MarginLevel"])*position[0]["Price"]/position[0]["Margin"]/position[0]["MarginLevel"]*-1,2)
        持仓信息['保证金'] = Account['Balance']
        持仓信息['挂单冻结'] = _N(Account['FrozenBalance'],2)       
        #if position[0]["Profit"] >= 0:
        #    持仓信息['仓位占用的保证金'] = position[0]["Margin"] - position[0]["Profit"]
        #else:
        持仓信息['仓位占用的保证金'] = position[0]["Margin"]      
        #实盘要改 模拟盘不用减浮盈
        持仓信息['爆仓价'] = _N((持仓信息['仓位占用的保证金']-持仓信息['仓位占用的保证金']*position[0]["MarginLevel"])*position[0]["Price"]/持仓信息['仓位占用的保证金']/position[0]["MarginLevel"]*-1,2) 
        持仓信息['浮动盈亏'] = _N(position[0]["Profit"],2)
        钱包余额 = _N(持仓信息['保证金'] + 持仓信息['仓位占用的保证金'] + 持仓信息['挂单冻结'],2)        
        #if 持仓信息['浮动盈亏'] <= 0:
        #    钱包余额 = _N(持仓信息['保证金'] + 持仓信息['仓位占用的保证金'] + 持仓信息['挂单冻结'] + 持仓信息['浮动盈亏'],2)
        #实盘要改 模拟盘逻辑不一样
        钱包余额超零分母 = _N(持仓信息['保证金'] + 持仓信息['仓位占用的保证金'] + 持仓信息['挂单冻结']- position[0]["Profit"],2)
        持仓信息['持仓百分比'] = _N(持仓信息['仓位占用的保证金']/钱包余额超零分母*100,2)     
        if 钱包余额 <= 0:
            #钱包余额超零分母 = _N(持仓信息['保证金'] + position[0]["Margin"] + 持仓信息['挂单冻结'],2)
            #持仓信息['持仓百分比'] = _N((持仓信息['仓位占用的保证金']-钱包余额)/钱包余额超零分母*100,2)
            #Log(钱包余额超零分母,钱包余额,持仓信息['持仓百分比'],持仓信息['仓位占用的保证金'])
            持仓信息['爆仓'] = '爆仓'
            #sys.exit()
        else:   
            #持仓信息['持仓百分比'] = _N(持仓信息['仓位占用的保证金']/钱包余额*100,2) 
            持仓信息['爆仓'] = ''
        if 持仓信息['历史持仓百分比'] < 持仓信息['持仓百分比']:
            持仓信息['历史持仓百分比'] = 持仓信息['持仓百分比']
            持仓信息['历史持仓时间'] = _D()
        指标状态 = str(账户状态值['区间可执行']) +"结束"+ str(账户状态值['区间钝化结束时间']) + "当前时间" + str(_D())  
        持仓百分比历史最高 = str(持仓信息['持仓百分比']) + '% / ' + str(持仓信息['历史持仓百分比']) + '%  ' + 持仓信息['历史持仓时间'] + 持仓信息['爆仓'] 
        table = {"type": "table", "title": "持仓信息", "cols": ["持仓量", "持仓均价","指标状态","现价","持仓百分比/历史最高","浮动盈亏"],
                 "rows": [[持仓信息['持仓金额显示'],_N(持仓信息['持仓均价'],2),指标状态,持仓信息['现价'],持仓百分比历史最高,持仓信息['浮动盈亏']],
                 ['保证金余额','仓位占用的保证金','挂单冻结','账户状态值[买入]','账户状态值[出售]','交易量补正倍率'],
                 [_N(钱包余额,2),_N(持仓信息['仓位占用的保证金'],2),持仓信息['挂单冻结'],
                 _N(账户状态值['买入'],2),_N(账户状态值['出售'],2),_N(交易量补正倍率,2)]]
                 }
        #type=类型 title=标题 cols=列称 rows=内容 同一行用[]表示 逗号分行
        LogStatus('`' + json.dumps(table) + '`')
        #if 钱包余额 <= 0:
            #sys.exit()#实盘要改
        return 持仓信息 
    elif len(ticker) > 0 and len(Account) > 0:
        持仓信息['持仓量'] = 0 #position[0]["Amount"]  
        持仓信息['持仓均价'] = 0 #position[0]["Price"]
        持仓信息['杠杆倍数'] = 0 #position[0]["MarginLevel"]
        持仓信息['现价'] = ticker["Last"]
        持仓信息['持仓金额'] = 0 #_N(position[0]["Amount"] * ticker["Last"],2)
        持仓信息['持仓金额显示'] = str(0)+'ETH  约等于'+str(0)+'USDT'
        持仓信息['爆仓价'] = 0 #_N((position[0]["Margin"]-position[0]["Margin"]*position[0]["MarginLevel"])*position[0]["Price"]/position[0]["Margin"]/position[0]["MarginLevel"]*-1,2)
        持仓信息['保证金'] = Account['Balance']
        持仓信息['挂单冻结'] = Account['FrozenBalance']
        持仓信息['仓位占用的保证金'] = 0 #position[0]["Margin"] - position[0]["Profit"]   
        持仓信息['爆仓价'] = 0 #_N((持仓信息['仓位占用的保证金']-持仓信息['仓位占用的保证金']*position[0]["MarginLevel"])*position[0]["Price"]/持仓信息['仓位占用的保证金']/position[0]["MarginLevel"]*-1,2) 
        持仓信息['浮动盈亏'] = 0 #_N(position[0]["Profit"],2)
        持仓百分比历史最高 = str(0) + '% / ' + str(持仓信息['历史持仓百分比']) + '%  ' + 持仓信息['历史持仓时间']
        指标状态 = str(账户状态值['区间可执行']) +"结束"+ str(账户状态值['区间钝化结束时间']) + "当前时间" + str(_D())
        table = {"type": "table", "title": "持仓信息", "cols": ["持仓量", "持仓均价","指标状态","现价","持仓百分比/历史最高","浮动盈亏"],
                 "rows": [[持仓信息['持仓金额显示'],_N(持仓信息['持仓均价'],2),指标状态,持仓信息['现价'],持仓百分比历史最高,持仓信息['浮动盈亏']],
                 ['保证金余额','仓位占用的保证金','挂单冻结','账户状态值[买入]','账户状态值[出售]','交易量补正倍率'],
                 [_N(持仓信息['保证金'] + 持仓信息['仓位占用的保证金'] + 持仓信息['挂单冻结'] + 持仓信息['浮动盈亏'],2),_N(持仓信息['仓位占用的保证金'],2),持仓信息['挂单冻结'],
                 账户状态值['买入'],账户状态值['出售'],_N(交易量补正倍率,2)]]
                 }
        #type=类型 title=标题 cols=列称 rows=内容 同一行用[]表示 逗号分行
        LogStatus('`' + json.dumps(table) + '`')
        return 持仓信息 

def ema(a):
    r = _C(exchange.GetRecords)
    if r and len(r) > a:
        ema = TA.EMA(r, a)
        Log(ema)           
def 交易规则(正数差,负数差,游动线,参考线,position,账户状态值,持仓信息,ticker,杠杆,交易量补正倍率,kdzong,kd,kd4,kd15):   
    #买入点逻辑:(无仓位时开始执行)
    #第一次接触到底部线买入，做状态记录。设置分批卖出接触到ema5，半仓卖出，接触到顶部线全仓卖出。每10%或最低交易量出售一次。做状态记录。
    #每个点位只触发一次
    #防守逻辑:(现价跌破买入点后执行)
    #现价跌破买入点一定比例后，买入补仓拉低均价，反弹一定比例后卖出减轻仓位。
    #储存买入的数量，反弹后定量卖出。
    k = kdzong[0]
    d = kdzong[1]                  
    强弱指数 = _N(d[len(d)-1],1)
    k3 = k[len(k)-1]
    d3 = d[len(d)-1]
    随机量能指标交叉 =  _Cross(k, d)
    趋势走势 = _Cross(游动线, 参考线)
    k33 = kd[0][len(kd[0])-1]
    d33 = kd[1][len(kd[1])-1]
    k34 = kd4[0][len(kd4[0])-1]
    d34 = kd4[1][len(kd4[1])-1]
    k315 = kd15[0][len(kd15[0])-1]
    d315 =kd15[1][len(kd15[1])-1]
    if d33 >= 80 and d34 >= 80 and d315 >= 80:
        超买 = 5
    elif d33 >= 80 and d34 >= 80:
        超买 = 4
    elif d315 >= 90 and d34 >= 70: 
        超买 = 3    
    elif d315 >= 80 and d34 >= 70 :
        超买 = 2.5
    elif d34 >= 80 :
        超买 = 2.3
    elif d33 >= 70 and d315 >= 80:
        超买 = 2   
    elif d33 >= 80:
        超买 = 1.2        
    elif d315 >= 80 :
        超买 = 1
    else:
        超买 = 0
        #账户状态值['异动止盈'] = 0    
    if d315 <= 20 and d33 <= 20 and d34 <= 20:
        超卖 = 1+zengfu*4
    elif d315 <= 20 and d33 <= 20 and d34 <= 50:
        超卖 = 1 + zengfu
    elif d33 <= 20 and d34 <= 20:
        超卖 = 1+zengfu*3  
    elif d34 <= 20 and d315 <= 20 and d33 <= 50:
        超卖 = 1+zengfu*2
    elif d33 <= 30 and d34 <= 50 and d315 <= 50 or d34 <= 30 and d33 <= 50 and d315 <= 50 or d315 <= 30 and d34 <= 50 and d33 <= 50:
        超卖 = 1 
        账户状态值['异动止盈'] = 0
        #Log('异动止盈:',账户状态值['异动止盈'])
    else:
        超卖 = 0       

    #d = _N(kdj[1][len(kdj[1])-1],1)
    顶部线 = _N(参考线[len(参考线)-1] + 获取列表平均数(正数差)*qujianbeilv,3)
    底部线 = _N(参考线[len(参考线)-1] + 获取列表平均数(负数差)*qujianbeilv1,3)
    Account=_C(exchange.GetAccount)
    保证金 = Account['Balance']
    游动线最后 = _N(游动线[len(游动线)-1],1)
    参考线最后 = _N(参考线[len(参考线)-1],1)
    现价 = ticker["Buy"]
    #Log(现价,底部线)

    if 持仓信息 is None:
        持仓量 = 0
        持仓均价 = 0
        #Log(持仓量)
    elif 持仓信息 is not None:
        持仓量 = 持仓信息['持仓量']
        持仓均价=持仓信息['持仓均价']      
    if 持仓量 == 0:
        账户状态值['空仓'] = 1
        账户状态值['出售'] = 0
        账户状态值['买入'] = 0
        账户状态值['异动止盈'] = 0
        #Log('异动止盈:',账户状态值['异动止盈'])
    elif  持仓量 > 0:
        账户状态值['空仓'] = 0     
    #判断当前区间范围是否达标，防止在指标钝化时买入。
    不可执行区间范围的 = 参考线最后*0.05 #复数分为 real 实数部分 + imag 虚数部分
    当前区间范围 = 顶部线 - 底部线
    #范围补偿 = cmath.sqrt(杠杆)
    #范围补偿 = 1 + (范围补偿.real *0.01*交易量补正倍率)
    #范围补偿 = 杠杆 * qujianbeilv1
    #不可执行区间范围的 = 不可执行区间范围的 * 范围补偿 
    时间间隔 = timedelta(hours=shijian)
    if 不可执行区间范围的 > 当前区间范围:
        #区间可执行 = 0         #区间范围太小策略指标钝化不卖买
        #账户状态值['区间钝化结束时间'] = _D(kdzong[2][len(kdzong)-1]/1000)
        账户状态值['区间钝化结束时间'] = _D()
        账户状态值['区间钝化结束时间'] = datetime.datetime.strptime(账户状态值['区间钝化结束时间'],'%Y-%m-%d %H:%M:%S') 
        账户状态值['区间可执行'] = 0
        持仓信息 = onTick(position,ticker,Account,交易量补正倍率,账户状态值)
        #Log(不可执行区间范围的,当前区间范围)     
        #sys.exit()     
    else:
        #区间可执行 = 1
        #Log(区间钝化结束时间)
        #Log(当前时间)
        账户状态值['区间钝化结束时间'] = str(账户状态值['区间钝化结束时间'])
        账户状态值['区间钝化结束时间'] = datetime.datetime.strptime(账户状态值['区间钝化结束时间'],'%Y-%m-%d %H:%M:%S')
        释放时间 = 账户状态值['区间钝化结束时间'] + 时间间隔
        释放时间=str(释放时间)
        当前时间 = _D()
        #当前时间=str(当前时间)
        释放时间 = int(time.mktime(time.strptime(释放时间,'%Y-%m-%d %H:%M:%S')))
        当前时间 = int(time.mktime(time.strptime(当前时间,'%Y-%m-%d %H:%M:%S')))
        if 释放时间 <= 当前时间:
            账户状态值['区间可执行'] = 1
            #Log(账户状态值['区间可执行'])
            #Log(_D(释放时间))
            #Log(_D())
            持仓信息 = onTick(position,ticker,Account,交易量补正倍率,账户状态值)
            #sys.exit()  
        else:
            账户状态值['区间可执行'] = 0 #指标正常状态可以买卖  
            持仓信息 = onTick(position,ticker,Account,交易量补正倍率,账户状态值)
        #Log(区间可执行)     
        #sys.exit()     
    #sys.exit()   
    #买入建仓规则 
    if 账户状态值['空仓'] == 1 and 账户状态值['买入'] == 0 and 现价 <= 底部线 and 超卖 > 1 and  账户状态值['区间可执行'] == 1 and 4>=交易量补正倍率>=0.8  : #买入建仓规则  游动线最后 > 底部线 and and 交易量补正倍率>=1 
        
        ticker = _C(exchange.GetTicker)
        现价 = ticker["Sell"]
        exchange.SetMarginLevel(杠杆)#杠杆倍数
        exchange.SetDirection("buy")#开仓方向
        买入币数=_N(保证金/现价*jiancang*杠杆*超卖,3)
        if 买入币数 < 0.002:
            买入币数 = 0.002
        #Log(买入币数,ticker["Last"]+1,底部线,)
        Log('建仓：','买入价',_N(现价+hua1,1),'买入数量',买入币数,'现价',现价,'底部线',底部线,'强弱指数',强弱指数,'交易补正倍率',交易量补正倍率,'超卖',超卖,'#238e23')
        Log('不可执行范围',不可执行区间范围的,'当前范围',当前区间范围,'区间钝化结束时间:',账户状态值['区间钝化结束时间'],'释放时间:',_D(释放时间))
        Log('基础动量',d33,'辅助动量',d34,'快速动量',d315)
        账户状态值['买入'] = 1
        if 买入币数 <= _N(保证金/ticker["Sell"]*杠杆,3):
            exchange.Buy(_N(现价+hua1,1),买入币数)#挂单价格，货币数量
        else:
            Log('保证金不足开仓失败@')
        #sys.exit()        
    if 首位挂单 is not None: # 一位挂单是否成交
        卖单成交 = 判断最新的挂单是否成交了(首位挂单['卖单id'])
        #卖单成交 = 0
        买单成交 = 判断最新的挂单是否成交了(首位挂单['买单id'])
        if 卖单成交 == 1:
            遍历并取消所有订单(0)
            卖单成交 = -1
            首位挂单['卖单id'] = -1
            if 账户状态值['出售'] == 10:
                Log('第十次成交','#ff00ff')
                position = _C(exchange.GetPosition)
                if len(position) > 0:
                    position = position
                else:
                    position = {0:{"Amount":0}} 
                持仓量 = position[0]["Amount"] 
                exchange.SetDirection("closebuy")
                遍历并取消所有订单(2)
                if 持仓量 > 0:
                    exchange.SetDirection("closebuy")
                    ticker = _C(exchange.GetTicker)
                    position = _C(exchange.GetPosition)
                    持仓量 = position[0]["Amount"] 
                    现价 = ticker["Sell"]
                    遍历并取消所有订单(2)
                    #实盘要改
                    只减仓Sell(_N(现价-hua1,1),0,持仓量)
                    #exchange.Sell(_N(现价-hua1,1),持仓量)
                    账户状态值['出售'] = 0
                    账户状态值['买入'] = 0
                    账户状态值['空仓'] = 1 

                账户状态值['出售'] = 0
                账户状态值['买入'] = 0
                账户状态值['空仓'] = 1
                #sys.exit()   
            #Log(首位挂单 )
            if 账户状态值['买入'] > 1:
                减 =  (账户状态值['买入']) * 0.1 + (账户状态值['买入']*交易量补正倍率) * 0.001   
                账户状态值['买入'] = _N(账户状态值['买入'] - 减 ,3)
                #这一栏是用于平衡买和卖的比例
                if 账户状态值['买入'] <1 :
                    账户状态值['买入'] = 1  
                Log(账户状态值['买入'],减)
            else:
                Log(账户状态值['买入'])    
                #sys.exit()  
        
        if 买单成交 == 1:
            #Log(买单成交,首位挂单['买单id'])
            #sys.exit() 
            遍历并取消所有订单(1)
            买单成交 = -1
            #Log(账户状态值['出售'] )  
            首位挂单['买单id'] = -1
            账户状态值['出售'] = 0   
    空仓判断()
    持仓信息 = onTick(position,ticker,Account,交易量补正倍率,账户状态值)                  
    if 账户状态值['空仓'] == 0 and 账户状态值['买入'] >= 1 and 现价 <= 持仓均价: #防守规则        
        #持仓均价低于现价的时候开始防守
        下单补正 = (账户状态值['买入']) * 0.05 + (账户状态值['买入']*交易量补正倍率) * 0.3 + 1.5 + 杠杆 * 0.1
        下单间隔 = 参考线最后*0.01*(1+下单补正)
        #开单前检测一下是否已经有订单防止同一个位置多次开单
        订单池状态=订单簿分析()
        买单未完成 = 订单池状态['买单未完成'] #=0表示无未完成买单       
        if 买单未完成 == 0 :
            position = _C(exchange.GetPosition)
            if position is None:
                持仓量 = 0
                持仓信息['持仓均价'] = 0
            elif position is not None:
                持仓量 = position[0]["Amount"] 
                持仓信息['持仓均价'] = position[0]["Price"]
            持仓均价=持仓信息['持仓均价']
            if 持仓均价 > 0 :             
                exchange.SetMarginLevel(杠杆)#杠杆倍数
                exchange.SetDirection("buy")#开仓方向
                买入币数 = _N(持仓量/账户状态值['买入']*(1+账户状态值['买入']*zengfu),3)
                if 买入币数 < 6/现价: #这步忘记是什么意思了，可能是最低开单数
                    买入币数 = _N(6/现价,3)
            #Log(买入币数,ticker["Last"]+1,底部线,)
                if 买入币数 <= _N(保证金/ticker["Sell"]*杠杆,3):
                    挂单价格=_N(持仓均价-下单间隔*账户状态值['买入'],1)
                    账户状态值['买入'] = 账户状态值['买入'] + 1
                    钱包余额 = _N(持仓信息['保证金'] + position[0]["Margin"] + 持仓信息['挂单冻结'],2)
                    if 持仓信息['浮动盈亏'] <= 0:
                        钱包余额 = _N(持仓信息['保证金'] + 持仓信息['仓位占用的保证金'] + 持仓信息['挂单冻结'] + 持仓信息['浮动盈亏'],2)
                    Log('防守：','持仓均价',_N(持仓均价,2),'下单间隔',_N(下单间隔,2),'*',_N(账户状态值['买入'],2),'现价:',现价,'挂单价:',挂单价格 + hua2,'持仓量',_N(持仓量,5),'交易量补正倍率:',_N(交易量补正倍率,2),'钱包余额:',钱包余额,'浮动盈亏:',持仓信息['浮动盈亏'],'持仓百分比:',持仓信息['持仓百分比'],'#32cd99')
                    #if 首位挂单['买单id'] != -1:
                    #    Log(exchange.GetOrder(首位挂单['买单id']))
                    首位挂单['买单id'] = exchange.Buy(挂单价格 + hua2,买入币数)#挂单价格，货币数量
                    #买单成交 = 判断最新的挂单是否成交了(首位挂单['买单id'])
                    #Log(买单成交,首位挂单['买单id'])
                    #sys.exit() 
    
    空仓判断()
    区间中位数 = (顶部线-底部线)/1.8+底部线
    if  趋势走势 >= 2 and 游动线最后 >= 区间中位数:
        趋势触发开关 = 1
    elif  趋势走势 <= -2 and 游动线最后 <= 区间中位数 :
        趋势触发开关 = 1
    else:
        趋势触发开关 = 0                            

    if 账户状态值['空仓'] == 0 and 超买 > 账户状态值['异动止盈'] :#or d3 >= 225 and 账户状态值['异动止盈'] > 0 and 账户状态值['空仓'] == 0 and 随机量能指标交叉 <= 0 and 趋势触发开关 == 1 and 游动线最后 >= 底部线 and 交易量补正倍率 <= 1.2: #异动止盈卖出规则
        #Log('触发异动止盈','现价',现价,'顶部线',顶部线,'区间中位数',区间中位数,'k:',k3,'d:',d3,'#ff00ff')
        账户状态值['异动止盈'] = 超买
        position = _C(exchange.GetPosition)
        ticker = _C(exchange.GetTicker)
        持仓量 = position[0]["Amount"] 
        现价=ticker["Buy"]
        exchange.SetDirection("closebuy")
        遍历并取消所有订单(2)
        卖出倍数 = 6 - 账户状态值['异动止盈']
        卖出币数 = _N(持仓量/卖出倍数,3)
        if d3 >= 225  and 账户状态值['空仓'] == 0 and 随机量能指标交叉 <= 0 and 趋势触发开关 == 1 and 游动线最后 >= 底部线 and 交易量补正倍率 <= 1.2:
            卖出币数 = 持仓量
            账户状态值['异动止盈'] = 超买 = 5
        #实盘要改    
        首位挂单['卖单id'] = 只减仓Sell(_N(现价-hua1,1),0,卖出币数)
        #首位挂单['卖单id'] = exchange.Sell(_N(现价-hua1,1),卖出币数)
        Log('触发异动止盈','现价',现价,'顶部线',顶部线,'超买',超买,'区间中位数',区间中位数,'卖出币数',_N(卖出币数,3),'#ff00ff')
        Log('基础动量',d33,'辅助动量',d34,'快速动量',d315)
        Log('异动止盈:',账户状态值['异动止盈'])
        减减 = (账户状态值['异动止盈'] - 账户状态值['出售']/2)/1
        if 减减 <0:
            减减 = 0
        账户状态值['买入'] = _N(账户状态值['买入'] - 减减,3)
        if 账户状态值['买入'] < 1 :
            账户状态值['买入'] = 1
        if 首位挂单 is not None:
            卖单成交 = 判断最新的挂单是否成交了(首位挂单['卖单id'])
        Sleep(1000)
        if 卖单成交 == 0:
            遍历并取消所有订单(2)
            ticker = _C(exchange.GetTicker)
            现价=ticker["Buy"]
            #实盘要改
            首位挂单['卖单id'] = 只减仓Sell(_N(现价-hua1,1),0,卖出币数)
            #首位挂单['卖单id'] = exchange.Sell(_N(现价-hua1,1),卖出币数)
            Sleep(500)
            卖单成交 = 判断最新的挂单是否成交了(首位挂单['卖单id'])
            
    空仓判断()    
    position = _C(exchange.GetPosition)
    ticker = _C(exchange.GetTicker)
    Account =  _C(exchange.GetAccount)  
    持仓信息 = onTick(position,ticker,Account,交易量补正倍率,账户状态值)    
    if 账户状态值['空仓'] == 0 and 持仓信息['浮动盈亏'] > -1 and 持仓信息['持仓百分比'] <= 1 : #尾巴仓位卖出规则
        Log('触发尾巴仓位处理','现价',现价,'顶部线',顶部线,'浮动盈亏:',持仓信息['浮动盈亏'],'持仓百分比:',持仓信息['持仓百分比'],'%','持仓量:',持仓信息['持仓量'],'#ff00ff')
        position = _C(exchange.GetPosition)
        ticker = _C(exchange.GetTicker)
        持仓量 = position[0]["Amount"] 
        现价=ticker["Buy"]
        exchange.SetDirection("closebuy")
        遍历并取消所有订单(2)
        #实盘要改
        首位挂单['卖单id'] = 只减仓Sell(_N(现价-hua1,1),0,持仓量)
        #首位挂单['卖单id'] = exchange.Sell(_N(现价-hua1,1),持仓量)
        if 首位挂单 is not None:
            卖单成交 = 判断最新的挂单是否成交了(首位挂单['卖单id'])
        Sleep(1000)
        if 卖单成交 == 0:
            遍历并取消所有订单(2)
            ticker = _C(exchange.GetTicker)
            现价=ticker["Buy"]
            #实盘要改
            只减仓Sell(_N(现价-hua1,1),0,持仓量)
            #exchange.Sell(_N(现价-hua1,1),持仓量)
            Sleep(500)
            
        账户状态值['出售'] = 0
        账户状态值['买入'] = 0
        账户状态值['空仓'] = 1         
    空仓判断()
    订单池状态=订单簿分析()
    卖单未完成 = 订单池状态['卖单未完成']

    if 账户状态值['空仓'] == 0  and 账户状态值['出售'] < 5 and 卖单未完成 == 0  : #止盈规则上半程 0表示无未完成卖单
        #计算出ema5下方五个止盈点位
        #每个点位卖出一次做状态记录
        position = _C(exchange.GetPosition)
        持仓均价 = position[0]["Price"]
        if 持仓均价 > 游动线最后:
            b = 游动线最后
        else:
            b = 持仓均价 
        for i in range(5):  
            a = (参考线最后-b)/5
            if a >= 0:      
                止盈点位[i]= _N(b + a*(i+1),1)
            elif a < 0:
                止盈点位[i]= _N(b + a*(5-i),1)

        position = _C(exchange.GetPosition)
        ticker = _C(exchange.GetTicker)        
        持仓量 = position[0]["Amount"] 
        现价=ticker["Buy"]
        卖出币数 =持仓量*卖出的比例[账户状态值['出售']]
        exchange.SetDirection("closebuy")
        Log(止盈点位)
        止盈价格 = 止盈点位[账户状态值['出售']]
        账户状态值['出售'] = 账户状态值['出售'] + 1 
        Log('止盈上','持仓均价',_N(持仓均价,2),'参考线',参考线最后,'游动线',游动线最后,'止盈价格',止盈价格 - hua2,'止盈次数',账户状态值['出售'],'卖单未完成:',卖单未完成,'持仓量',_N(持仓量,5),'#ff7f00')
        #实盘要改
        首位挂单['卖单id'] = 只减仓Sell(止盈价格,hua2,卖出币数)
        #首位挂单['卖单id'] = exchange.Sell(止盈价格 - hua2,卖出币数)
    空仓判断()
    订单池状态=订单簿分析()
    卖单未完成 = 订单池状态['卖单未完成']
    if 账户状态值['空仓'] == 0 and 账户状态值['出售'] >= 5 and 卖单未完成 == 0  : #止盈规则下半程 0表示无未完成卖单
        #计算出顶部到ema5五个止盈点位
        #每个点位卖出一次做状态记录
        position = _C(exchange.GetPosition)
        持仓均价 = position[0]["Price"]
        for i in range(5):
            if 参考线最后 >= 持仓均价:
                a = (顶部线-参考线最后)/5      
                止盈点位[i+5]= _N(参考线最后+ a*(i+1),1)
            else:
                a = (顶部线-持仓均价)/5      
                止盈点位[i+5]= _N(持仓均价+ a*(i+1),1)                    
        position = _C(exchange.GetPosition)
        ticker = _C(exchange.GetTicker)        
        持仓量 = position[0]["Amount"] 
        现价=ticker["Buy"]
        卖出币数 =持仓量*卖出的比例[账户状态值['出售']]
        exchange.SetDirection("closebuy")
        止盈价格 = 止盈点位[账户状态值['出售']]
        账户状态值['出售'] = 账户状态值['出售'] + 1 
        Log('止盈下','持仓均价',_N(持仓均价,2),'参考线',参考线最后,'游动线',游动线最后,'顶部线',顶部线,'止盈价格',止盈价格 - hua2,'止盈次数',账户状态值['出售'],'卖单未完成:',卖单未完成,'持仓量',_N(持仓量,5),'#ff7f00')        
        Log(止盈点位)
        #实盘要改
        首位挂单['卖单id'] = 只减仓Sell(止盈价格,hua2,卖出币数)
        #首位挂单['卖单id'] = exchange.Sell(止盈价格 - hua2,卖出币数)
          
def 订单簿分析():
    订单簿=_C(exchange.GetOrders)
    订单池状态['买单未完成数量'] = 0
    订单池状态['卖单未完成数量'] = 0
    订单池状态['买单未完成'] = 1
    订单池状态['卖单未完成'] = 1
    for i in range(len(订单簿)):
        订单状态 = 订单簿[i]["Status"] #0=未完成 1=已经完成 2=已经取消 3=其他状态
        订单类型 = 订单簿[i]["Type"] #0=买单 1=卖单

        if 订单状态 == 0 and 订单类型 == 0:
            订单池状态['买单未完成数量'] = 订单池状态['买单未完成数量'] + 1
        if 订单状态 == 0 and 订单类型 == 1:
            订单池状态['卖单未完成数量'] = 订单池状态['卖单未完成数量'] + 1     
    买单未完成数量 = 订单池状态['买单未完成数量']   
    卖单未完成数量 = 订单池状态['卖单未完成数量']
    if 买单未完成数量 > 0:
        订单池状态['买单未完成'] = 1
        #Log('有未完成订单')
    else:
        订单池状态['买单未完成'] = 0
    if 卖单未完成数量 > 0:
        订单池状态['卖单未完成'] = 1
    else:
        订单池状态['卖单未完成'] = 0 
    return 订单池状态   # 买单未完成=0 卖单未完成=0        
def 遍历并取消所有订单(a):      
    #0 取消所以买单 ， 1 取消所以卖单 ， 2取消所以订单。
    订单簿=_C(exchange.GetOrders)
    空仓判断()       
    for i in range(len(订单簿)):
        订单状态 = 订单簿[i]["Status"] #0=未完成 1=已经完成 2=已经取消 3=其他状态
        订单类型 = 订单簿[i]["Type"] #0=买单 1=卖单
        if 订单状态 == 0 and a == 2:
            exchange.CancelOrder(订单簿[i]["Id"])
            if 订单类型 == 0 :
                if 账户状态值['空仓'] == 1:
                    账户状态值['买入'] = 0
                elif  账户状态值['买入'] >=2 and 账户状态值['空仓'] == 0:
                    账户状态值['买入'] = _N(账户状态值['买入'] - 1,3)
                elif  2 > 账户状态值['买入'] > 1 and 账户状态值['空仓'] == 0:
                   账户状态值['买入'] = 账户状态值['买入']
            elif 订单类型 == 1 :  
                if 账户状态值['空仓'] == 1:
                    账户状态值['出售'] = 0
                elif  账户状态值['出售'] >=1 and 账户状态值['空仓'] == 0:
                    账户状态值['出售'] = _N(账户状态值['出售'] - 1,0)        

        if 订单状态 == 0 and a == 0 and 订单类型 == 0:         
            exchange.CancelOrder(订单簿[i]["Id"])
            if 账户状态值['空仓'] == 1:
                账户状态值['买入'] = 0
            elif  账户状态值['买入'] >=2 and 账户状态值['空仓'] == 0:
                账户状态值['买入'] = _N(账户状态值['买入'] - 1,3)
            elif  2 > 账户状态值['买入'] > 1 and 账户状态值['空仓'] == 0:
                账户状态值['买入'] = 1                
        if 订单状态 == 0 and a == 1 and 订单类型 == 1:
            exchange.CancelOrder(订单簿[i]["Id"])
            if 账户状态值['空仓'] == 1:
                账户状态值['出售'] = 0
            elif  账户状态值['出售'] >=1 and 账户状态值['空仓'] == 0:
                账户状态值['出售'] = _N(账户状态值['出售'] - 1,0)

def 判断最新的挂单是否成交了(a):
    if a is None:
        a = -1
    # 0=判断未成交 1=判断成交
    if a != -1:
        最新挂单 = _C(exchange.GetOrder,a)
        if len(最新挂单) <= 0:
            Sleep(1000)
            最新挂单 =  _C(exchange.GetOrder,a)
        if len(最新挂单) <= 0:
            Sleep(1000)
            最新挂单 =  _C(exchange.GetOrder,a)
        if  len(最新挂单) > 0:

            if  最新挂单["Status"] == 1:
                b = 1
                Log('已成交',最新挂单,'#ff0000')
                return b
            else:
                b = 0
                return b   
    else:
        b = 0
        return b
        
def 按钮信息(总充入,初始资产):
    按钮信息 = GetCommand()
     
    if 按钮信息:
        按钮信息 = 按钮信息.split(':')
        if 按钮信息[0] == '充':
            充入 = float(按钮信息[1])
            Log('触发按钮',按钮信息[0],'数量',按钮信息[1],'USDT')
            #Log (总充入,初始资产,充入)    
            总充入 = 打印利润(总充入,初始资产,充入) 
            return 总充入 
    return 总充入                      
def 打印利润(总充入,初始资产,充入):
    Account = _C(exchange.GetAccount)
    position = _C(exchange.GetPosition)
    if len(position) > 0:
        position = position
    else:
        position = {0:{'Margin':0}} 
    #Log (总充入,初始资产,充入)      
    总充入 = 总充入 + 充入
    利润 = (Account['Balance'] + Account['FrozenBalance'] + position[0]['Margin']) - (初始资产 + 总充入)
    LogProfit(利润,'&') 
    return 总充入     
def 空仓判断():
    position = _C(exchange.GetPosition)
    if len(position) > 0:
        持仓量 = position[0]["Amount"]  
    else:
        持仓量 = 0
          
    if 持仓量 == 0:
        账户状态值['空仓'] = 1
        账户状态值['出售'] = 0
        账户状态值['买入'] = 0
        账户状态值['异动止盈'] = 0
    elif  持仓量 > 0:
        账户状态值['空仓'] = 0  
def 只减仓Sell(止盈价格,hua2,卖出币数):
    价格 = _N(止盈价格 - hua2,1)
    卖出币数 = _N(卖出币数,3)
    basecurrency='ETHUSDT'
    quantity = str(卖出币数)
    price = str(价格)
    message = "symbol=" + basecurrency + "&quantity=" + quantity + "&price=" + price + "&side=SELL" + "&type=LIMIT"+"&timeInForce=GTC"+"&reduceOnly=true"
    Log('卖出价',价格,'数量',卖出币数)
    挂单ID = exchange.IO("api", "POST", "/fapi/v1/order",message)
    #挂单ID = exchange.IO("api", "POST", "/fapi/v1/order",
    #                   "symbol=ETHUSDT&side=SELL&type=LIMIT&reduceOnly=true&quantity=0.005&price=4000&timeInForce=GTC")
    #u = 挂单ID['orderId']
    if len(挂单ID) > 0:
        u = 挂单ID['orderId']
        return u
    else:
        u = -1
        return u

def 求差(a,b):
    if a > b:
        c = a-b
    elif a < b:
        c= b-a
    else:
        c=0
    return c               

def 处理kd数据(a,b):
    c={}
    T=[]
    k = a[0]              
    d = a[1]                   
    for i in range(len(b)):
        T.append(b[i]['Time'])        
    c[0] = k
    c[1] = d
    c[2] = T
    #0是快线，1是慢线，T是时间戳
    #sys.exit()
    return c

def kd整合(kd,kd4,kd15):
    a=[]
    b=[]
    c=[]
    kdzong={}
    
    for i in range(len(kd[2])):
        
        for i1 in range(len(kd4[2])):

            X = len(kd4[2]) - i1 - 1  
            if kd4[2][X] == kd[2][i]:
                k4 = kd4[0][X]
                d4 = kd4[1][X]
                break
            else:
                k4 = kd4[0][len(kd4[2])-1]
                d4 = kd4[1][len(kd4[2])-1]
        for i2 in range(len(kd15[2])):
            X = len(kd15[2]) - i2 - 1  
            if kd15[2][X] == kd[2][i]:
                k15 = kd15[0][X]
                d15 = kd15[1][X]
                break
            else:
                k15 = kd15[0][len(kd15[2])-1]
                d15 = kd15[1][len(kd15[2])-1]
        if kd[0][i] != kd[0][i]:
            k2 = None
        else:
            k2 = kd[0][i]           
        if kd[1][i] != kd[1][i]:
            d2 = None  
        else:
            d2 = kd[1][i]    
        if k4 != k4:
            k4 = None             
        if d4 != d4:
            d4 = None                                       
        if k15 != k15:
            k15 = None        
        if d15 != d15:
            d15 = None    
        if k2 is not None and k4 is not None and k15 is not None and d2 is not None and d4 is not None and d15 is not None:                       
            k2 = k2 + k4 + k15
            d2 = d2 + d4 + d15                       
        elif k2 is not None and k4 is not None and d2 is not None and d4 is not None :   
            k2 = k2*2 + k4 
            d2 = d2*2 + d4
        elif k2 is not None and d2 is not None:
            k2 = k2*3
            d2 = d2*3
        else:
            k2 = d2 = None
        a.append(k2)
        b.append(d2)
        c.append(kd[2][i])     
    kdzong[0]=a
    kdzong[1]=b
    kdzong[2]=c
    return kdzong

def 从时间戳取对应参数(时间戳,kd,kd4,kd15,kd数据):  
    kdzong=kd数据
    对应时间  = kdzong['对应时间']           
    k4 = kdzong['k4']
    d4 =kdzong['d4'] 
    k15 =kdzong['k15']
    d15 =kdzong['d15'] 

    for i1 in range(len(kd4[2])):

        X = len(kd4[2]) - i1 - 1  
        if kd4[2][X]== 时间戳:
            k4 = kd4[0][X]
            d4 = kd4[1][X]
            #对应时间 = kd4[2][X]
            break
        #else:
        #    k4 = kd4[0][len(kd4[2])-1]
        #    d4 = kd4[1][len(kd4[2])-1]
        #    对应时间 = kd4[2][X]
    for i2 in range(len(kd15[2])):
        X = len(kd15[2]) - i2 - 1  
        if kd15[2][X] == 时间戳:
            k15 = kd15[0][X]
            d15 = kd15[1][X]
        #    对应时间 = kd15[2][X]
            #sys.exit()
            break
        else:
            k15 = kd15[0][len(kd15[2])-1]
            d15 = kd15[1][len(kd15[2])-1]
        #    对应时间 = kd15[2][len(kd15[2])-1]
    for i in range(len(kd[2])):
        X = len(kd[2])- i - 1
        if kd[2][X] == 时间戳:
            k = kd[0][X]
            d = kd[1][X]
            #对应时间 = kd[2][X]
            break
        else:
            k = kd[0][len(kd[2])-1]
            d = kd[1][len(kd[2])-1]
            #对应时间 = kd[2][len(kd[2])-1]
    if d != d:
        d = None
        d4 = None
        d15 = None
    if d4 != d4 :
        d4 = None
    if d15 != d15 :
        d15 = None
    if k != k:
        k = None
        k4 = None
        k15 = None        
    if k4 != k4 :
        k4 = None
    if k15 != k15 :
        k15 = None                                   
    kdzong['k'] = k
    kdzong['d'] = d              
    kdzong['k4'] = k4
    kdzong['d4'] = d4  
    kdzong['k15'] = k15
    kdzong['d15'] = d15
    kdzong['对应时间'] = 对应时间 
    return kdzong 