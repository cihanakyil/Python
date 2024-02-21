def Fibo(baslangicSayisi,bitisSayisi):
    sayi1=0
    sayi2=1
    toplam=0
    fibo=[]
    if(sayi1>=baslangicSayisi and sayi1<=bitisSayisi):
        fibo +=[sayi1]
    if(sayi2>=baslangicSayisi and sayi2<=bitisSayisi):
        fibo +=[sayi2]
        
    while(True):
        toplam = sayi1 + sayi2
        if(toplam>=baslangicSayisi and toplam<=bitisSayisi):
            fibo +=[toplam]
        sayi1 = sayi2 
        sayi2 = toplam
        if(toplam>bitisSayisi):
            break
    print(fibo)
    

startValue=int(input("BAŞLANGIÇ SAYISI: "))
endValue=int(input("BİTİŞ SAYISI: "))


Fibo(startValue,endValue)
    