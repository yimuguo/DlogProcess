####Write Data to File
#filename=raw_input("Enter test plan file name:\n")
import os
import glob

tp_txt=open('out.txt','w+')
tp_txt.write("Min Values:\tMax Values\t:\n")
###Find Test Num and filter out float
def keyword_limit(keyword,dlog,tp_txt):
    import re
    test=filter(lambda x: keyword in x, dlog)
    splitlimit=[]
    for x in test:
        x=re.split("\s+",x)
        splitlimit.append(x)
    tmin=[]
    tmax=[]
    for x in splitlimit:
        if x[2]=='0' and len(x)>12:
            if x[4]!=('OutputLeakage' or 'InputLeadkage') and (x[8]=='uA' or x[8]=='mV'):
                x[7]=str(float(x[7])/1000) 
            tmin.append(x[7])
            if x[4]!=('OutputLeakage' or 'InputLeadkage') and (x[12]=='uA' or x[12]=='mV'):
                x[11]=str(float(x[11])/1000)
            tmax.append(x[11])
        elif len(x)<=17:
            tmin.append('')
            tmax.append('')
    del re
    i=0
    for x in range(0,len(tmin)):
        if not (tmin[i]==tmin[i-1] and tmax[i]==tmax[i-1]):
            tp_txt.write(tmin[i]+'\t'+tmax[i]+'\n')
        i+=1
###Read into Datalog
#filename=raw_input("Enter dlog full path:\n")

os.chdir("S://Test_Eng//J750_HW_SW//VC5//AK652_008_748//doc//")

for file in glob.glob("*QA*.txt"):
    filename = file
with open(filename) as data:
    dlog=data.read().splitlines()

keyword_limit('IDD18_dynamic',dlog,tp_txt)
keyword_limit('IDD18_3s',dlog,tp_txt)
keyword_limit('IDD18_SD',dlog,tp_txt)
keyword_limit('IOS_LVDS18',dlog,tp_txt)
keyword_limit('OutputLeadkage',dlog,tp_txt)

#keyword_limit('IDD',dlog,tp_txt)
#tmin1,tmax1=keyword_limit('LDO
#writetp(tmin,tmax,tp_txt)
