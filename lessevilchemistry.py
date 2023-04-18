import random

def genChem(dif=1):
    global chems
    run=True
    ochems=chems[:]
    while run:
        o={}
        ck=-1+dif+random.randint(2,3+dif)
        cs=random.choices(atns,k=ck)
        for c in cs:
            o[c]=random.randint(1,2+dif)
        cm=(set(o.keys()),o)
        chems.append(cm)
        tt=react({repr(cm):1})
        if tt==[(cm,1)]:
            run=False
        else:
            del chems[-1]
    chems=ochems
    chems.append(cm)
    
    

def react(bank):
    o=[]
    bb={}
    bbs=set()
    for tc in bank.keys():
        keys=eval(tc)[1]
        v=bank[tc]
        for key in keys:
            bb[key]=bb.get(key,0)+keys[key]*v
            bbs.add(key)
    for chem in chems:
        if chem[0].issubset(bbs):
            l=1000000
            for cc in chem[1]:
                vv=chem[1][cc]
                ll=bb[cc]/vv
                if ll<l:
                    l=ll
            for cc in chem[1]:
                vv=chem[1][cc]
                mm=vv*l
                bb[cc]-=mm
##                bb[cc]=round(bb[cc],5)
                if bb[cc]<.000001:
                    del bb[cc]
                    bbs.remove(cc)
            o.append((chem,l))
    for it in bbs:
        o.append(((set(it),{it:1}),bb[it]))
    return([(x[0],round(x[1],5)) for x in o])
def wreact(bank):
    d={}
    for a,b in bank:
        d[repr(als[a])]=b
    rr=react(d)
    oo=[]
    for o,v in rr:
        k=list(als.keys())[list(als.values()).index(o)]
        oo.append((k,v))
    return(oo)
def recipe(goal,inc=[]):
    if als.get(goal)!=None:
        while True:
            aa=random.choices(list(als.keys()),k=random.randint(2,4))
            cc=[(x,1) for x in aa+inc]
            c=sorted(cc)
            if goal not in [x[0] for x in c]:
                d=sorted(wreact(c))
                if c!=d:
                    if goal in [x[0] for x in d]:
                        return(c)
    else:
        return(None)
##def krecipe(goal):
##    while True:
##        aa=random.choices(list(als.keys()),k=random.randint(2,4))
##        cc=[(x,random.uniform(0,1)) for x in aa]
##        c=sorted(cc)
##        if goal not in [x[0] for x in c]:
##            d=sorted(wreact(c))
##            if c!=d:
##                if goal in [x[0] for x in d]:
##                    return(c)

chems=[]
als={}

atns=list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
random.seed(1)
with open("alchemy.txt") as f:
    txt=f.read()
R1,R2=txt.split("\n\n")
for line in R1.split("\n"):
    n,d=line.split("::")
    als[n]=(set(d),{d:1})
##for c in atns:
##    if als.get(c)==None:
##        als[c+"?"]=(set(c),{c:1})
for line in R2.split("\n"):
    n,d=line.split("-")
    genChem(int(d))
    als[n]=chems[-1]
##    print(n,chems[-1],als[n])
