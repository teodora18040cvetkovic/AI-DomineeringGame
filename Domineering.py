import copy
import string

def drawTable(m,n,matrica): 
    slova=" "
    razmak=" "
    red=m
    for l in range(n):
       slova=slova + " " + (string.ascii_uppercase[l])
    for v in range(2*m + 3): 
        if(v == 0 or v==2*m+2):
            print(razmak+slova)
        elif(v >= 2 and v <= 2*m):
            if(v%2 == 0):
                print(str(red) +"||",end="")
                for i in range(0,n):
                   print(str(matrica[(v//2)-1][i])+"|",end="")
                print("|"+ str(red))
                red=red-1 
            else:
                print(razmak+" "+" -"*n)
        elif(v == 1 or v == 2*m+1):
            print(razmak+" " +" ="*n,end=" ")
            print()
def validanPotez(potez,row,column,koIgra,matrica):
    brojSlova =  potez[1]
    if(koIgra == False):
        pV = potez[0] 
        if(pV<1 or matrica[pV][brojSlova] != " "):
            print("Nevalidan potez")
            return False
        if(matrica[pV-1][brojSlova] != " "):
            print("Nevalidan potez")
            return False
        else:
            print("Validan potez")
            return True
    elif(koIgra==True):
        pV = potez[0]
        if(brojSlova+1 > column-1 or matrica[pV][brojSlova] != " " ):
            print("Nevalidan potez")
            return False
        if(matrica[pV][brojSlova+1] != " "):
            print("Nevalidan potez")
            return False
        else:
            print("Validan potez")
            return True
def postavi(potez,matrica,koIgra,undo=False):
    brojSlova = potez[1] 
    potezV=potez[0]
    if(koIgra==False):
        c="X" if undo==False else " "
        matrica[potezV][brojSlova]=c
        matrica[potezV-1][brojSlova]=c
    elif(koIgra==True):
        c="O" if undo==False else " "
        matrica[potezV][brojSlova]=c
        matrica[potezV][brojSlova+1]=c
def uzmiPotez(row,column) -> list[int,int]:
    while(True):
        try:
            potezRow = int(input("Unesite u kojoj vrsti je potez:"))
            pr=row-potezRow
            if pr >= row or pr < 0:
                print("Broj mora biti manji od  "+ str(row))
                continue
        except ValueError:
            print("Mora biti broj")
            continue
        while(True):
            potezColumn = str(input("Unesite u kojoj koloni je potez:"))
            brojSlova = ord(potezColumn) - 65
            if(brojSlova > 31 and brojSlova < 58): 
                brojSlova = brojSlova - 32
            if(brojSlova < 0 or brojSlova > 32 or len(potezColumn) > 1 or brojSlova > column):
                print("Mora jedno slovo koje je u opsegu od A do " + string.ascii_uppercase[column-1])
                continue
            else:
                break
        return [pr,brojSlova]
def moguciPotezi(matrica,koIgra,row,column):
    rez=[]
    for i in range(row):
        for j in range(column):
            if(((i>0  if koIgra==False else j<column-1)) and matrica[i][j]==" " and matrica[i if koIgra==True else i-1][j if koIgra==False else j+1]==" "):
                rez.append([i,j])
    return rez
def kraj(brStanja,koIgra):
    if(not brStanja):
        if koIgra:
            print("Pobednik O")
            return True
        else:
            print("Pobednik X")
            return True
    return False

def proceniPotez(matrica,row,column):
    procenjen=len(moguciPotezi(matrica,False,row,column))-len(moguciPotezi(matrica,True,row,column))
    return procenjen

def minimax(matrica,row,column,potezi,dubina,maxIgrac,alfa,beta):
    pBeskonacnost=float('inf')
    nBeskonacnost=float('-inf')
    najboljiPotez=[]
    if dubina==0 or len(potezi)==0:
        return[najboljiPotez,proceniPotez(matrica,row,column)]
    if maxIgrac:
        #igra X
        maxEval=nBeskonacnost
        for cvor in potezi:
            deca=moguciPotezi(matrica,True,row,column)
            
            postavi(cvor,matrica,False)
            evaluation=minimax(matrica,row,column,deca,dubina-1,False,alfa,beta)
            postavi(cvor,matrica,False,True)
            if(maxEval<evaluation[1]):
                maxEval=evaluation[1]
                najboljiPotez=cvor
            alfa = max(alfa, evaluation[1])
            if beta<=alfa:
                break
        
        return [najboljiPotez,maxEval]
    else:
        minEval=pBeskonacnost
        for cvor in potezi:
            deca=moguciPotezi(matrica,False,row,column)
            postavi(cvor,matrica,True)
            evaluation=minimax(matrica,row,column,deca,dubina-1,True,alfa,beta)
            postavi(cvor,matrica,True,True)
            if(minEval>evaluation[1]):
                minEval=evaluation[1]
                najboljiPotez=cvor
            beta=min(beta,evaluation[1])
            if beta<=alfa:
                break
        return [najboljiPotez,minEval]      

def igracVsRacunar(modeRacunar,matrica,row,column,koIgra):
    pBeskonacnost=float('inf')
    nBeskonacnost=float('-inf')
    if not modeRacunar:
        #ako je tacno da je racunar igrac X
        if koIgra:
            koIgra=igracevPotez(row,column,koIgra,matrica)
        else:
            potezi=moguciPotezi(matrica,koIgra,row,column)
            dobijenPotez=minimax(matrica,row,column,potezi,3,True,nBeskonacnost,pBeskonacnost)
            postavi(dobijenPotez[0],matrica,koIgra)
            koIgra=not koIgra
        drawTable(row,column,matrica)
    else:
        #ako je racunar igrac O
        if koIgra:
            potezi=moguciPotezi(matrica,koIgra,row,column)
            dobijenPotez=minimax(matrica,row,column,potezi,4,False,nBeskonacnost,pBeskonacnost)
            postavi(dobijenPotez[0],matrica,koIgra)
            koIgra=not koIgra
        else:
            koIgra=igracevPotez(row,column,koIgra,matrica)
        drawTable(row,column,matrica)
    
    return koIgra      
    
def igraj(mode,modeRacunar,koIgra,matrica,row,column,pobeda):
    while(not pobeda): 
        lista = moguciPotezi(matrica,koIgra,row,column)
        if koIgra:
            if(lista):
                print("Na potezu O:")
        else:
            if(lista):
                print("Na potezu X:") 
        pobeda =  kraj(lista,not koIgra) 
        if(pobeda):
            break
        else:
            if mode=="C":
                #igraju dva coveka
                koIgra=igracevPotez(row,column,koIgra,matrica)
                drawTable(row,column,matrica)
            elif mode=="R":
                if modeRacunar=="R":
                    #igramo protiv racunara, racunar je igrac X
                    koIgra=igracVsRacunar(False,matrica,row,column,koIgra)
                elif modeRacunar=="C":
                    #igramo protiv racunara, racunar je igrac O
                    koIgra=igracVsRacunar(True,matrica,row,column,koIgra)

def igracevPotez(row,column,koIgra,matrica):
    potez = uzmiPotez(row,column)
    validan=validanPotez(potez,row,column,koIgra,matrica)
    while(not validan):
        potez = uzmiPotez(row,column)
        validan=validanPotez(potez,row,column,koIgra,matrica)
    postavi(potez,matrica,koIgra)
    koIgra = not koIgra
    return koIgra          
     
def main():
    row = int(input("Unesite broj vrsta:")) 
    column = int(input("Unesite broj kolona:"))
    matrica=[[" " for i in range(row)]for j in range(column)]
    drawTable(row,column,matrica)
    koIgra = False # igra X
    pobeda = False
    mode=input("Igrate protiv racunara ili coveka? R - racunar, C - covek ")
    if mode=="R":
        modeRacunar=input("Ko igra prvi: R - racunar, C - covek ")
        if modeRacunar=="R":
            print("Racunar je igrac X:")
        elif modeRacunar=="C":
            print("Covek je igrac X")  
    elif mode=="C":
        modeRacunar=None
        print("Igrate dvoje!")
    igraj(mode,modeRacunar,koIgra,matrica,row,column,pobeda)
  
main()


