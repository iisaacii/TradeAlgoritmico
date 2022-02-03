from pushbullet import Pushbullet
from binance import depthcache
from binance.client import Client
from binance.depthcache import DepthCache
from binance import AsyncClient, DepthCacheManager
from binance.enums import *
from numpy import double
import pandas as pd
import time
import asyncio
import threading

def conectando():
    
    global client
    global Intervalobinance
    global Tiempobinance
    global Intervalo
    global Tiempo
    global TotalVelas
    global Vactual
    
    try:
        client = Client('9zT6cjcxJjKo9Cd7IPQjZ2zOhSfLs2aEBmgDiw1twVuUPPWB8P7KpEqPb23EARKD', 'QuRFVdI9c818CgnD94Xl0qADUImZiiucuzILrbpFEPAOOXk36GSbJEFJ2C4qV2mm')
        #Modificar 4 parametros de abajo para hacer cambios en velas
        Intervalobinance="5m"
        Tiempobinance="10 hour ago UTC"
        Intervalo=5
        Tiempo=10

        TotalVelas=int((60/Intervalo)*Tiempo)
        Vactual=(TotalVelas-1)
    except:
        pass
    time.sleep(1)


def notificacion(notify):
    try:
        pb = Pushbullet("o.YwzjfelaOrgn9SvAEoxx1s4KVaHBO6WI")
        pb.push_note("Jarvis",notify)
    except:
        pass
        
def archivo(texto,nombre):
    archivo1=open(nombre,'a')
    archivo1.write(texto)


def liquidez():
    #FUNCIÓN PARA OBTENER LIQUIDEZ EN LISTAS
    #sacar depth de la función si no quieres actualizar la función cada que llames la fx
    while 1:
        global pbids
        global lbids
        global pasks
        global lasks
        global Tlbids
        global Tlasks
        global Indexbid1
        global Indexbid2
        global Indexbid3
        global Indexbid4
        global Indexbid5
        global Indexbid6
        global Indexbid7
        global Indexbid8
        global Indexbid9
        global Indexbid10
        pbids=[]
        lbids=[]
        pasks=[]
        lasks=[]
        try:
            
            depth = pd.DataFrame(client.get_order_book(symbol='DOGEUSDT',limit=500))#Limite máximo 1000

            #Rellenando listas
            for i in range(300): #Modificar sólo esto para un rango menor, debe ser menor al limite en depth 
                bids=pd.DataFrame(depth.iloc[i,1])
                asks=pd.DataFrame(depth.iloc[i,2])
            
                pbids.append(double(bids.iloc[0,0]))
                lbids.append(double(bids.iloc[1,0]))

                pasks.append(double(asks.iloc[0,0]))
                lasks.append(double(asks.iloc[1,0]))

            #Imprimiendo listas
            """print("\n\n\nPrecio bids:\n",pbids)
            print("Liquidez bids:\n",lbids)

            print("\n\n\nPrecio asks:\n",pasks)
            print("Liquidez asks:\n",lasks)"""

            #Ordenando listas
            Tlbids=sorted(lbids,reverse=True)
            Tlasks=sorted(lasks,reverse=True)


            #Imprimiendo listas ordenadas
            """print("\n\nORDENANDO DE MAYOR A MENOR\n")

            print("Liquidez en bids:\n",Tlbids)
            print("\n\nLiquidez en asks:\n",Tlasks)

            print("\nTop 1 bids:",Tlbids[0])
            print("\nTop 1 asks:",Tlasks[0])"""

            #Buscar el precio del top de liquidez
            
            Indexbid1=lbids.index(Tlbids[0])
            Indexask1=lasks.index(Tlasks[0])

            Indexbid2=lbids.index(Tlbids[1])
            Indexask2=lasks.index(Tlasks[1])

            Indexbid3=lbids.index(Tlbids[2])
            Indexask3=lasks.index(Tlasks[2])

            Indexbid4=lbids.index(Tlbids[3])

            Indexbid5=lbids.index(Tlbids[4])

            Indexbid6=lbids.index(Tlbids[5])

            Indexbid7=lbids.index(Tlbids[6])

            Indexbid8=lbids.index(Tlbids[7])

            Indexbid9=lbids.index(Tlbids[8])

            Indexbid10=lbids.index(Tlbids[9])

            
            """"
            print("\n\n")
            print("           ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            print("Top1 B: ",Tlbids[0]," Precio: ",pbids[Indexbid1])
            print("Top1 A: ",Tlasks[0]," Precio: ",pasks[Indexask1])
            print("\n")

            print("Top2 B: ",Tlbids[1]," Precio: ",pbids[Indexbid2])
            print("Top2 A: ",Tlasks[1]," Precio: ",pasks[Indexask2])
            print("\n")

            print("Top3 B: ",Tlbids[2]," Precio: ",pbids[Indexbid3])
            print("Top3 A: ",Tlasks[2]," Precio: ",pasks[Indexask3])
            print("\n")
            """
        except:
            pass
        time.sleep(2400)


def velas():
    #Obteniendo datos de velas
    while 1:
        global precioDOGE
        global low2_
        global low_
        global high_
        global close_
        global volume_
        global volumebuy_
        global volumesell_
        global open_
        open_=[]
        high_=[]
        low2_=[]
        low_=[]
        close_=[]
        volume_=[]
        volumebuy_=[]
        volumesell_=[]
        try:
            klines =pd.DataFrame(client.get_historical_klines("DOGEUSDT", Intervalobinance, Tiempobinance)).astype(float)
            priceD = pd.Series(client.get_symbol_ticker(symbol='DOGEUSDT'))
            precioDOGE=double(priceD[1])
            
            #print("Open        High        Low        Close      Volume")
            #Rellenando datos de velas en listas separadas
            for i in range(TotalVelas):
                open_.append(klines.iloc[i,1])
                high_.append(klines.iloc[i,2])
                low_.append(klines.iloc[i,3])
                close_.append(klines.iloc[i,4])
                volume_.append(klines.iloc[i,5])
                volumebuy_.append(klines.iloc[i,9])
                volumesell_.append(klines.iloc[i,5]-klines.iloc[i,9])
                #print(i," ",open_[i],"  ",high_[i],"  ",low_[i],"  ",close_[i],"  ",volume_[i],"\n")
            
            for i in range(100):
                low2_.append(klines.iloc[i,3])    
        except:
            pass    
        time.sleep(2)       
        
def bajada():
    #Verificando que se encuentre en una bajada.
    while 1:
        global ba
        ba=0
        try:
            for i in range(TotalVelas):
                if(low_[Vactual]<=high_[i]*0.9725):
                    #print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                    #print("Bajada detectada respecto a ",Vactual-i," velas anteriores")
                    ba=1
                    texto2=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+":  Bajada detectada\n"
                    nombre2="bajada.txt"
                    archivo(texto2,nombre2)
                    break
        except:
            pass   
        time.sleep(10)    
    
def minimosuperado():    
    #Verificando que rompa minimo anterior
    while 1:
        global mini
        global superlow
        mini=0
        try:
            superlow=sorted(low2_)
            for i in range(100):
                if((low_[i]==superlow[0]) & (low_[Vactual]<=superlow[0])):#1.3% if((low_[Vactual]/0.987)<low_[i]):
                    for j in range(i+1,i+20):
                        if (high_[j]>low_[i]/0.99):#0.98039
                            mini=1
                            texto3=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+":  Minimo superado\n"
                            nombre3="minimo.txt"
                            archivo(texto3,nombre3)
                            break 
        except:
            pass  
        time.sleep(10)

def ordenes():
    #Verificando que toque la liquidez
    while 1:
        global order
        order=0

        try:
            text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+"\nTop1 B:"+str(Tlbids[0])+" Precio: "+str(pbids[Indexbid1])+"\nTop2 B:"+str(Tlbids[1])+" Precio: "+str(pbids[Indexbid2])+"\nTop3 B:"+str(Tlbids[2])+" Precio: "+str(pbids[Indexbid3])+"\nTop4 B:"+str(Tlbids[3])+" Precio: "+str(pbids[Indexbid4])+"\nTop5 B:"+str(Tlbids[4])+" Precio: "+str(pbids[Indexbid5])+"\nTop6 B:"+str(Tlbids[5])+" Precio: "+str(pbids[Indexbid6])+"\nTop7 B:"+str(Tlbids[6])+" Precio: "+str(pbids[Indexbid7])+"\nTop8 B:"+str(Tlbids[7])+" Precio: "+str(pbids[Indexbid8])+"\nTop9 B:"+str(Tlbids[8])+" Precio: "+str(pbids[Indexbid9])+"\nTop10 B:"+str(Tlbids[9])+" Precio: "+str(pbids[Indexbid10])+"\nPA: "+str(low_[Vactual])+"\n\n"
            nombre="ordenes.txt"
            archivo(text,nombre)

            if ((low_[Vactual]<=pbids[Indexbid1] and Tlbids[0]>1500000) or (low_[Vactual]<=pbids[Indexbid2] and Tlbids[1]>1500000) or (low_[Vactual]<=pbids[Indexbid3] and Tlbids[2]>1500000) or (low_[Vactual]<=pbids[Indexbid4] and Tlbids[3]>1500000) or (low_[Vactual]<=pbids[Indexbid5] and Tlbids[4]>1500000)
            or (low_[Vactual]<=pbids[Indexbid6] and Tlbids[5]>1500000) or (low_[Vactual]<=pbids[Indexbid7] and Tlbids[6]>1500000) or (low_[Vactual]<=pbids[Indexbid8] and Tlbids[7]>1500000) or (low_[Vactual]<=pbids[Indexbid9] and Tlbids[8]>1500000) or (low_[Vactual]<=pbids[Indexbid10] and Tlbids[9]>1500000)):
            
                archivo("\t\t\t\t\t\t\t\t\t\t\t\tTocó la liquidez",nombre)
                """
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())) 
                print("Top1 B: ",Tlbids[0]," Precio: ",pbids[Indexbid1])
                print("Top2 B: ",Tlbids[1]," Precio: ",pbids[Indexbid2])
                print("Top3 B: ",Tlbids[2]," Precio: ",pbids[Indexbid3])
                print("Top4 B: ",Tlbids[3]," Precio: ",pbids[Indexbid4])
                print("Top5 B: ",Tlbids[4]," Precio: ",pbids[Indexbid5])
                print("Top6 B: ",Tlbids[5]," Precio: ",pbids[Indexbid6])
                print("Top7 B: ",Tlbids[6]," Precio: ",pbids[Indexbid7])
                print("Top8 B: ",Tlbids[7]," Precio: ",pbids[Indexbid8])
                print("Top9 B: ",Tlbids[8]," Precio: ",pbids[Indexbid9])
                print("Top10 B: ",Tlbids[9]," Precio: ",pbids[Indexbid10])
                print("PA: ",low_[Vactual],"\n")
                """
                #notificacion(text)
                order=1       
        except:
            pass
        time.sleep(2)    



def volumen():
    switch=0
    while 1:   
        if (cambio==1):
            """if((volume_[Vactual]>=volume_[Vactual-1]) & (volume_[Vactual]>=volume_[Vactual-2]) & (volume_[Vactual]>=volume_[Vactual-3])
            &  (volume_[Vactual]>=volume_[Vactual-4]) & (volume_[Vactual]>=volume_[Vactual-5]) & (volume_[Vactual]>=volume_[Vactual-6])):"""
            texto4=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+":  Evaluando volumen\n"
            nombre4="volumen.txt"
            archivo(texto4,nombre4)
            while switch==0:
                minutos=int(time.strftime('%M', time.localtime()))
                segundos=int(time.strftime('%S', time.localtime()))
                try:
                    if (minutos%5==0)&(segundos==00)&(precioDOGE<_precioDOGE):
                        if (volumebuy_[Vactual]/volumesell_[Vactual] >= 1.5):
                            compra(1)
                            switch=1
                except:
                    pass
                time.sleep(1)
            """time.sleep(1200)
            try:
                if((volume_[Vactual]<volume_[Vactual-4]) & (volume_[Vactual-1]<volume_[Vactual-4]) & (volume_[Vactual-2]<volume_[Vactual-4]) & (volume_[Vactual-3]<volume_[Vactual-4])):
                    archivo(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+":  Comprado\n",nombre4)
                    compra(1)
                              
                else:
                    texto4_1=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+":  Bajará más\n"
                    archivo(texto4_1,nombre4)               
            except:
                time.sleep(2)
                if((volume_[Vactual]<volume_[Vactual-4]) & (volume_[Vactual-1]<volume_[Vactual-4]) & (volume_[Vactual-2]<volume_[Vactual-4]) & (volume_[Vactual-3]<volume_[Vactual-4])):
                    archivo(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+":  Comprado\n",nombre4)
                    compra(1)
                              
                else:
                    texto4_1=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+":  Bajará más\n"
                    archivo(texto4_1,nombre4)"""
        time.sleep(3)


def condiciones():
    global cambio
    global _precioDOGE
    while 1:
        try:
            if (ba==1)&(mini==1)&(order==1):
                cambio=1
                _precioDOGE=precioDOGE
                print(_precioDOGE,"1:::::::")
                break
                #trades(1,) #Pasar argumentos con hilos, la "," indica que acepta tuplas de datos o listas "[]"
        except:   
            pass
        else:
            cambio=0
        time.sleep(2)


def trades(rebote):
    global STradesum
    global STradesum2
    STradesum=[]
    STradesum2=[]
    while 1:
        global qtybuy
        global qtysell
        global Tradebuy
        global Tradesell
        global Tradediferencia
        global suma
        minutos=int(time.strftime('%M', time.localtime()))
        segundos=int(time.strftime('%S', time.localtime()))
        try:
            if (minutos%5==0)&(segundos==00)&(rebote==0):
                agg_trades = pd.DataFrame(client.aggregate_trade_iter(symbol='DOGEUSDT', start_str='5 minutes ago UTC'))

                qtybuy=agg_trades[agg_trades['m']==False]
                qtysell=agg_trades[agg_trades['m']==True]

                Tradebuy=round((qtybuy['q'].astype(float).sum())/1000)
                Tradesell=round((qtysell['q'].astype(float).sum())/1000)
                if (Tradebuy>Tradesell):
                    Tradediferencia=round(Tradebuy/Tradesell,1)

                if(Tradebuy<Tradesell):
                    Tradediferencia=round(-Tradesell/Tradebuy,1)
            
                texto5=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+": R:                 "+str(Tradediferencia)+"                 B: "+str(Tradebuy)+"          S: "+str(Tradesell)+"\n"
                nombre5="trades.txt"
                archivo(texto5,nombre5)

                STradesum.append(Tradediferencia)
                if (len(STradesum)==4):
                    suma=round(sum(STradesum),1)
                    STradesum.clear()
                    #texto5_1=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+"                         "+str(suma)+"\n"
                    #archivo(texto5_1,nombre5)
            """
            if (minutos%5==0)&(segundos==00)&(rebote==1):
                agg_trades = pd.DataFrame(client.aggregate_trade_iter(symbol='DOGEUSDT', start_str='5 minutes ago UTC'))
               
                qtybuy=agg_trades[agg_trades['m']==False]
                qtysell=agg_trades[agg_trades['m']==True]

                Tradebuy=round((qtybuy['q'].astype(float).sum())/1000)
                Tradesell=round((qtysell['q'].astype(float).sum())/1000)
                if (Tradebuy>Tradesell):
                    Tradediferencia=round(Tradebuy/Tradesell,1)

                if(Tradebuy<Tradesell):
                    Tradediferencia=round(-Tradesell/Tradebuy,1)


                STradesum2.append(Tradediferencia)
                if(len(STradesum2)==4):
                    if (STradesum2[0]<STradesum2[1])&(STradesum2[0]<STradesum2[2])&(STradesum2[0]<STradesum2[3]):
                        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+"  Entrada Tradess")
                    STradesum2.clear()
                    break
            """
        except:
            pass
        time.sleep(1)

def sombra():
    while 1:
        minutos=int(time.strftime('%M', time.localtime()))
        segundos=int(time.strftime('%S', time.localtime()))
        try:
            if (minutos%5==0)&(segundos==5)&(cambio==1):
                extension=high_[Vactual-1] - low_[Vactual-1]
                if open_[Vactual-1]<close_[Vactual-1]:
                    
                    if open_[Vactual-1] >= (low_[Vactual-1] + (extension*0.50)):
                        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+" Entrada por vela ")
                        
                if open_[Vactual-1]>close_[Vactual-1]:
                    
                    if close_[Vactual-1] >= (low_[Vactual-1] + (extension*0.50)):
                        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+" Entrada por vela ")
                        
        except:
            time.sleep(2)
            extension=high_[Vactual-1] - low_[Vactual-1]
            if open_[Vactual-1]<close_[Vactual-1]:
                
                if open_[Vactual-1] >= (low_[Vactual-1] + (extension*0.40)):
                    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+" Entrada por vela ")
                if open_[Vactual-1]>close_[Vactual-1]:
                    
                    if close_[Vactual-1] >= (low_[Vactual-1] + (extension*0.40)):
                        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())+" Entrada por vela ")
        time.sleep(1)


def compra(Done): 
    global comprado
    global comprasalvada
    comprado=0      
    comprasalvada=0
    
    while 1:
        try:
            if (Done==1)&(comprado==0):
                comprasalvada=precioDOGE
                comprado=1
                

                notificacion(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+"\nCompra a : "+str(comprasalvada))
                
                
            if(comprado==1) & (precioDOGE >= comprasalvada/0.989):
                comprado=0
                Done=0

                notificacion(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+"\nVendido :\nSe compró a: "+str(comprasalvada)+"\nSe vendió a: "+str(precioDOGE))
             
        except:
            pass
        time.sleep(1)  
           
         
#Con una vez que se ejcute conectando está bien
conectando()
#Ejecutando hilos

hliquidez=threading.Thread(target=liquidez).start()
hvelas=threading.Thread(target=velas).start()
time.sleep(1)
hbajada=threading.Thread(target=bajada).start()
hminimo=threading.Thread(target=minimosuperado).start()
hordenes=threading.Thread(target=ordenes).start()
hcambio=threading.Thread(target=condiciones).start()
hvolumen=threading.Thread(target=volumen).start()
htrades=threading.Thread(target=trades,args=(0,)).start()
#hsombra=threading.Thread(target=sombra).start()


#*************++**COMPRAR**************************************
#balance = client.get_asset_balance(asset='USDT')
#TotalUSDT=double(balance['free'])
#CantidadBuy=round((TotalUSDT*0.995)/precioDOGE)

#orderbuy = client.order_market_buy(
#    symbol='DOGEUSDT',
#    quantity=CantidadBuy,


#*************++**VENDER**************************************
#balance = client.get_asset_balance(asset='DOGE')
#TotalDOGE=double(balance['free'])
#CantidadSell=round(TotalDOGE*0.995)

#order = client.order_market_sell(
#    symbol='DOGEUSDT',
#    quantity=CantidadSell)

   

    








