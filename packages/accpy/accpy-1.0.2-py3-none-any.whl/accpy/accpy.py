#本程式提供多種以函式設計的會計應用功能，由[台灣.屏東大學.周國華老師]設計

import numpy as np

def LoanPayment(a,b,c):
    d=a/((1-pow((1+(c/1200)),(-b*12)))/(c/1200))
    return d

'''
LoanPayment函式在計算銀行貸款每月應償付之本息金額
參數a是貸款總金額，
參數b是貸款總年數，
參數c是貸款年利率(例如，3.5%，要輸入3.5)。

'''

def isave(a,b,c):
    d=a*(((1+(c/1200))**(b+1)-1)/(c/1200))-a
    return d

'''
isave函式(isave是InstallmentSavings的簡稱)在計算以每月存款方式進行零存整付的到期本利合
參數a是每月存款金額，
參數b是存款次數(例如一年期就是12次)，
參數c是存款的年利率(例如，3.5%，要輸入3.5)。

'''

def BondPrice(a,b,c,d,e):
    f=a/(1+(c/100)/d)**(d*e)+a*(b/100)/d*(1-(1+(c/100)/d)**(-d*e))/((c/100)/d)
    return f

'''
BondPrice函式在計算公司債發行總價格
參數a是公司債票面總金額，
參數b是公司債票面年利率(例如，3.5%，要輸入3.5)，
參數c是公司債市場有效利率(例如，3.75%，要輸入3.75)，
參數d是公司債每年付息次數，
參數e是公司債存續年數。

'''

def CapitalBudgeting(a,b,c):
    IRR=np.irr(a)
    MIRR=np.mirr(a,b,c)
    NPV=np.npv(b,a)
    return IRR,MIRR,NPV

'''
CapitalBudgeting函式在計算投資方案IRR、MIRR及NPV
參數a是投資方案期初及各期期末淨現金流入(出)金額，以串列方式輸入，
參數b是資金成本率(例如，3.5%，要輸入3.5)，
參數c是各期淨現金流入再投資報酬率(例如，3.75%，要輸入3.75)，
本函式執行完畢會依序回傳IRR、MIRR及NPV等三個資本預算關鍵數據，
在使用本函式時，需要以類似 x,y,z=accpy.CapitalBudgeting(a,b,c)的結構來取得數據。

'''

def FPDB(a,b,c):
    r=1-(c/a)**(1/b)
    i=1
    while i<=b:
        print()
        print('第',i,'期：')
        d=a*r
        print('  借：折舊費用  ',format(d,',.2f'))
        print('      貸：累計折舊  ',format(d,',.2f'))
        a=a-d
        i += 1

'''
FPDB函式(FPDB是fixed percentage of declining balance的簡稱)在產生定率遞減法下各期的折舊分錄
參數a是設備資產的購置成本，
參數b是設備資產的估計耐用年限，
參數c是設備資產的估計殘值。

'''

def SYD(a,b,c):
    s=(1+b)*b/2
    i=1
    while b>=1:
        print()
        print('第',i,'期：')
        d=(a-c)*(b/s)
        print('  借：折舊費用  ',format(d,',.2f'))
        print('      貸：累計折舊  ',format(d,',.2f'))
        i += 1
        b -= 1

'''
SYD函式(SYD是sum of years' digits的簡稱)在產生年數合計法下各期的折舊分錄
參數a是設備資產的購置成本，
參數b是設備資產的估計耐用年限，
參數c是設備資產的估計殘值。

'''

def DDB(a,b,c,m):
    r=1/b*m
    i=1
    while (i<=b) and (a>c):
        print()
        print('第',i,'期：')
        d=a*r
        if (a-d)<c:
            d=a-c
        print('  借：折舊費用  ',format(d,',.2f'))
        print('      貸：累計折舊  ',format(d,',.2f'))
        a=a-d
        i += 1

'''
DDB函式(DDB是double declining balance的簡稱)在產生倍數餘額遞減法下各期的折舊分錄
參數a是設備資產的購置成本，
參數b是設備資產的估計耐用年限，
參數c是設備資產的估計殘值，
參數m是直線法折舊率的倍數，通常是2或1.5倍。

'''

def SLN(a,b,c):
    i=1
    while i<=b:
        print()
        print('第',i,'期：')
        d=(a-c)/b
        print('  借：折舊費用  ',format(d,',.2f'))
        print('      貸：累計折舊  ',format(d,',.2f'))
        i += 1

'''
SLN函式(SLN是straight line method的簡稱)在產生直線法下各期的折舊分錄
參數a是設備資產的購置成本，
參數b是設備資產的估計耐用年限，
參數c是設備資產的估計殘值。

'''

def BondEntry(a,b,c,d,e):
    #計算發行價格
    f=a/(1+(c/100)/d)**(d*e)+a*(b/100)/d*(1-(1+(c/100)/d)**(-d*e))/((c/100)/d)
    #計算每期現金利息
    g=a*(b/100)/d
    if c>b:
        h=a-f
        print('按照您輸入的相關數據，本項公司債為折價發行，總發行價格是新台幣',format(f,',.2f'),'元')
        print('發行折價是新台幣',format(h,',.2f'),'元')
        print()
        print('本項公司債的發行及付息還本攤銷分錄如下：')
        print('發行時：')
        print('  借：現金        ',format(f,'>15,.2f'))
        print('  借：公司債折價  ',format(h,'>15,.2f'))
        print('      貸：應付公司債  ',format(a,'>15,.2f'))
        i=1
        while i<= d*e:
            print()
            #計算利息費用
            j=f*(c/100)/d
            #計算折價攤銷
            k=j-g
            print('第',i,'期末(付息及攤銷折價)：')
            print('  借：利息費用  ',format(j,'>15,.2f'))
            print('      貸：現金        ',format(g,'>15,.2f'))
            print('      貸：公司債折價  ',format(k,'>15,.2f'))
            f=f+k
            i+=1
    elif b>c:
        m=f-a
        print('按照您輸入的相關數據，本項公司債為溢價發行，總發行價格是新台幣',format(f,',.2f'),'元')
        print('發行溢價是新台幣',format(m,',.2f'),'元')
        print()
        print('本項公司債的發行及攤銷分錄如下：')
        print('發行時：')
        print('  借：現金  ',format(f,'15,.2f'))
        print('      貸：應付公司債  ',format(a,'>15,.2f'))
        print('      貸：公司債溢價  ',format(m,'>15,.2f'))
        i=1
        while i<= d*e:
            print()
            #計算利息費用
            j=f*(c/100)/d
            #計算溢價攤銷
            n=g-j
            print('第',i,'期末(付息及攤銷折價)：')
            print('  借：利息費用    ',format(j,'>15,.2f'))
            print('  借：公司債溢價  ',format(n,'>15,.2f'))
            print('      貸：現金        ',format(g,'15,.2f'))
            f=f-n
            i+=1
    else:
        print('按照您輸入的相關數據，本項公司債為平價發行，總發行價格是新台幣',format(f,',.2f'),'元')
        print()
        print('本項公司債的發行及攤銷分錄如下：')
        print('發行時：')
        print('  借：現金  ',format(f,',.2f'))
        print('      貸：應付公司債  ',format(a,',.2f'))    
        i=1
        while i<= d*e:
            print()
            print('第',i,'期末(付息)：')
            print('  借：利息費用    ',format(g,',.2f'))
            print('      貸：現金        ',format(g,',.2f'))
            i+=1  
    print('  到期還本：')
    print('  借：應付公司債  ',format(f,',.2f'))
    print('      貸：現金        ',format(f,',.2f'))
    print()

'''
BondEntry函式在產生公司債發行及付息還本的攤銷分錄
參數a是公司債票面總金額，
參數b是公司債票面年利率(例如，3.5%，要輸入3.5)，
參數c是公司債市場有效利率(例如，3.75%，要輸入3.75)，
參數d是公司債每年付息次數，
參數e是公司債存續年數。

'''

def BreakEven(a,b):
    tpm=0
    te=0
    i=1
    while i<=b:
        print()
        print('請輸入第',i,'種產品的單位售價、單位變動成本及營收占比。')
        c=eval(input('單位售價：'))
        d=eval(input('單位變動成本：'))
        e=eval(input('營收占比(例如，第N種產品營收占總營收比率為25%，則輸入0.25)：'))
        pm=(c-d)/c*e
        tpm=tpm+pm
        te=te+e
        i+=1
    be=a/tpm
    print()
    if te!=1:
        print('您輸入的各項產品營收占比數據有誤，下次請輸入正確數據。')
    else:
        print('根據您輸入的數據，個案公司的損益兩平銷售總金額是新台幣',format(be,',.2f'),'元')
    print()

'''
BreakEven函式在計算多種產品組合下的損益兩平銷售金額
參數a是個案公司固定成本總額，
參數b是個案公司銷售的產品共有幾種。

'''


    

    

