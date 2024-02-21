def PozitifBolenler(x):
    sayac=1
    PozitifBolenler =[]
    while(sayac<x):
        if((x % sayac) == 0):
            PozitifBolenler +=[sayac]
        sayac +=1
    print(x,"Sayısının Pozitif Bolenleri: ", PozitifBolenler)
    return PozitifBolenler

def DiziToplami(dizi):
    toplam=0
    for x in dizi:
        toplam+=x
    return toplam

def CizgiPrint():
    print("------------------------------------------------------")

sayi1=int(input("LÜTFEN 1.SAYIYI GİRİNİZ : "))
sayi2=int(input("LÜTFEN 2.SAYIYI GİRİNİZ : "))

CizgiPrint()

toplam1=DiziToplami(PozitifBolenler(sayi1))

CizgiPrint()

toplam2=DiziToplami(PozitifBolenler(sayi2))

CizgiPrint()

sonuc = toplam1 == sayi2 and toplam2 == sayi1

if(sonuc):
    print(sonuc,"--->BUNLAR ARKADAŞ SAYILARDIR.")
else:
    print(sonuc,"--->BUNLAR ARKADAŞ SAYILAR DEĞİLDİR.")
    
