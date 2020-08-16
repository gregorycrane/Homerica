#!/usr/bin/env python3
  
import sys
import re
import operator


endingkeys = ['nu_movable','iterative']
from greek_accentuation.characters import *
from greek_accentuation.syllabify import *
from greek_accentuation.accentuation import *



missedstemtypes = {}
paradlist = {}

sawkeys = {}
infact = {}
infmp = {}
vocsg = {}
nomsg = {}
gensg = {}
datsg = {}
accsg = {}

vocd = {}
nomd = {}
gend = {}
datd = {}
accd = {}

vocpl = {}
nompl = {}
genpl = {}
datpl = {}
accpl = {}

sg1 = {}
sg2 = {}
sg3 = {}

du1 = {}
du2 = {}
du3 = {}

pl1 = {}
pl2 = {}
pl3 = {}

homertot = 0
homerlems = {}
homerfreq = {}

iltot = 0
illems = {}
ilfreq = {}

odtot = 0
odlems = {}
odfreq = {}

numcasedbase = {}
numcasedbase['s\ta'] = ''
enddbase = {}
#verbals = {}
#verbalcounts= {}
#verbalcounts_il01 = {}

#nominals = {}
#nominalcounts= {}
#nominalcounts_il01 = {}
tokens = []
postable = {}
wordids = {}
sentids = {}
lemmas = {}
rawforms = {}
postags = {}
depids = {}
syntags = {}
parads = {}
savelines = {}

sawkeys = {}

def addunit(s,l):
  if( s in l):
   l[s] = l[s] + 1
  else:
   l[s] = 1

lexfile = "../Wolf1807/grcwork/tlg0557-tbankplus.txt"
lexfile = "tlg0012-tbankplus.txt"
with open(lexfile) as f:
  for line in f:
    line = re.sub('ᾱ/','ᾱ́',line)
    line = re.sub('ᾱ\|','ᾱͅ',line)  
    if( re.search(r'^#',line)):
     continue
    if( not re.search(r'tbx',line)):
     continue
    line = re.sub('\s*$','',line)
    fields = line.split('\t') 


    curkey = fields[1]
    if( curkey in sawkeys):
     continue
    sawkeys[curkey] = 1
    tokens.append(curkey)

    wordids[curkey] = curkey
    sentids[curkey] = fields[2]
    lemmas[curkey] = fields[3]
    rawforms[curkey] = fields[4]
    postags[curkey] = fields[5]
    depids[curkey] = fields[6]
    syntags[curkey] = fields[7]
    parads[curkey] = fields[8]
    savelines[curkey] = line
    addunit(lemmas[curkey],homerlems)
    homertot = homertot + 1
   
    if( re.search('tlg001:',wordids[curkey])):
     iltot = iltot + 1
     addunit(lemmas[curkey],illems)
     ilfreq[lemmas[curkey]] = str((10000*illems[lemmas[curkey]])/iltot)
     ilfreq[lemmas[curkey]] = re.sub(r'(\.[0-9][0-9]).+','\g<1>',ilfreq[lemmas[curkey]])
    else:
     odtot = odtot + 1
     addunit(lemmas[curkey],odlems)
     odfreq[lemmas[curkey]] = str((10000*odlems[lemmas[curkey]])/odtot)
     odfreq[lemmas[curkey]] = re.sub(r'(\.[0-9][0-9]).+','\g<1>',odfreq[lemmas[curkey]])

    p = parads[curkey].split('@')
    stemtype = p[2]
    ekey = ''
    if( len(p) == 4 and p[3]):
     keys = p[3]
     for foo in p[3].split('-'):
      if( foo in endingkeys):
         if( ekey ):
          ekey = ekey + '-' + foo
         else:
           ekey = foo
     #print("haskeys",p[3])
     #keys = 'haskeys'
    else:
     keys = ''

    if( re.search(r'^v...na',postags[curkey])): 
      addunit(endkey,infact)

    #m = re.search('^[v]([123][sdp])(.[^p].)...',postags[curkey])
    m = re.search('^[v](..)(.[^p].)...',postags[curkey])
    if( m ):
      if( re.search("\-end",p[1])):
         tmpend = re.sub(r".*\-([^\-]+)$",'\g<1>',p[0])
         endkey = tmpend + "\t" + postags[curkey]  + "\t" + stemtype + "\t" + ekey
         addunit(endkey,enddbase)
         #print("endkey",endkey)
         if( re.search(r'^v...na',postags[curkey])): addunit(endkey,infact)

         if( re.search(r'^v1s',postags[curkey])): addunit(endkey,sg1)
         if( re.search(r'^v2s',postags[curkey])): addunit(endkey,sg2)
         if( re.search(r'^v3s',postags[curkey])): addunit(endkey,sg3)

         if( re.search(r'^v1d',postags[curkey])): addunit(endkey,du1)
         if( re.search(r'^v2d',postags[curkey])): addunit(endkey,du2)
         if( re.search(r'^v3d',postags[curkey])): addunit(endkey,du3)

         if( re.search(r'^v1p',postags[curkey])): addunit(endkey,pl1)
         if( re.search(r'^v2p',postags[curkey])): addunit(endkey,pl2)
         if( re.search(r'^v3p',postags[curkey])): addunit(endkey,pl3)


    #m = re.search('^([napv]).([sdp])(...)([mfn])([vngda])[^cs]',postags[curkey])
    m = re.search('^([napv]).([sdp])(...)([mfn])([vngda])(.)',postags[curkey])
    if( m ):
        numcase = m.group(2) + "\t" +  m.group(5)
        gender = m.group(4)
        degree = m.group(6)
        if( re.search(r'^[a-z]+$',m.group(3))):
          stemtype= stemtype + '-' + m.group(3)
          #print("participal",stemtype)
        #nominals[curkey] = rawforms[curkey] + "\t" + numcase + "\t" + lemmas[curkey] + "\t" + gender + "\t" + stemtype + "\t" + keys
        #addunit(nominals[curkey],nominalcounts)
        if( re.search("\-end",p[1])):
            tmpend = re.sub(r".*\-([^\-]+)$",'\g<1>',p[0])
            endkey = tmpend + "\t" + numcase + "\t" + gender + "\t" +degree + "\t" + stemtype + "\t" + ekey
            pos = re.sub(r'^.','.',postags[curkey])
            endkey = tmpend + "\t" + pos + "\t" + stemtype
            addunit(endkey,enddbase)

            if( numcase == 's\tv'): addunit(endkey,vocsg)
            if( numcase == 's\tn'): addunit(endkey,nomsg)
            if( numcase == 's\tg'): addunit(endkey,gensg)
            if( numcase == 's\td'): addunit(endkey,datsg)
            if( numcase == 's\ta'): addunit(endkey,accsg)

            if( numcase == 'd\tv'): addunit(endkey,vocd)
            if( numcase == 'd\tn'): addunit(endkey,nomd)
            if( numcase == 'd\tg'): addunit(endkey,gend)
            if( numcase == 'd\td'): addunit(endkey,datd)
            if( numcase == 'd\ta'): addunit(endkey,accd)

            if( numcase == 'p\tv'): addunit(endkey,vocpl)
            if( numcase == 'p\tn'): addunit(endkey,nompl)
            if( numcase == 'p\tg'): addunit(endkey,genpl)
            if( numcase == 'p\td'): addunit(endkey,datpl)
            if( numcase == 'p\ta'): addunit(endkey,accpl)

    #    if( re.search('tlg001:1\.',wordids[curkey] )):
          #addunit(nominals[curkey],nominalcounts_il01)
    else:
        gennumcase = ''
        #nominals[curkey] = "missing data"


      
f.close()
  
def printpnum(stemtype,tensemoodvoice,pnum,persnum,label):
   sawit = 0
   for foo in dict(sorted(pnum.items(), key=operator.itemgetter(1),reverse=True)):
    p = foo.split('\t')
    if( p[2] == stemtype and re.search(tensemoodvoice,foo)):
     print(foo,pnum[foo],label)
     sawit = 1
   if( sawit): print()

def printtensemoodvoice(stemtype,tensemoodvoice,label):
  paradlist['v'+'@' + stemtype + '@' + tensemoodvoice + '@' + label] = 1
  printpnum(stemtype,tensemoodvoice,sg1,"1st sg",label)
  printpnum(stemtype,tensemoodvoice,sg2,"2nd sg",label)
  printpnum(stemtype,tensemoodvoice,sg3,"3rd sg",label)

  printpnum(stemtype,tensemoodvoice,du1,"1st du",label)
  printpnum(stemtype,tensemoodvoice,du2,"2nd du",label)
  printpnum(stemtype,tensemoodvoice,du3,"3rd du",label)
    
  printpnum(stemtype,tensemoodvoice,pl1,"1st pl",label)
  printpnum(stemtype,tensemoodvoice,pl2,"2nd pl",label)
  printpnum(stemtype,tensemoodvoice,pl3,"3rd pl",label)


def showverbs(stemtype,tensemoodvoice,label):
  for curkey in tokens:
    p = parads[curkey].split('@')
    if( not p[2] == stemtype):
     continue
    if( not re.search('^v..'+tensemoodvoice,postags[curkey])):
     continue
    if( not lemmas[curkey] in illems):
           illems[lemmas[curkey]] = 0
           ilfreq[lemmas[curkey]] = '0.00'
    if( not lemmas[curkey] in odlems):
           odlems[lemmas[curkey]] = 0
           odfreq[lemmas[curkey]] = '0.00'
    print(label,"verbal",str(homerlems[lemmas[curkey]]),str(illems[lemmas[curkey]]),str(odlems[lemmas[curkey]]),ilfreq[lemmas[curkey]],odfreq[lemmas[curkey]],savelines[curkey])
    continue



    if( not re.search('^v[123][sdp]',postags[curkey])):
     continue
    if( not re.search(stemtype,parads[curkey])):
     continue
    if( not re.search('^v..'+tensemoodvoice,postags[curkey])):
     continue
    if( re.search('^v...p',postags[curkey])):
     continue
    m = re.search('(tlg00[12]:[0-9]+\.[0-9]+)',wordids[curkey])
    if(m):
     cit = m.group(1)
    else:
     cit = "nocit"
    #print("verbkey",label,cit,sentids[curkey],cit,verbals[curkey],verbalcounts[verbals[curkey]])
    
    
def printnumcase(stemtype,nparad,ncase,numcase,label):
   sawit = 0
   if( nparad == '' ):
     nparad = '[^cs]$'
   if( ncase == {}): return
   for foo in dict(sorted(ncase.items(), key=operator.itemgetter(1),reverse=True)):
    p = foo.split('\t')
    if( not re.search(nparad,p[1])):
      continue
    #if( re.search(stemtype,foo)):
    if( stemtype == p[2]):
     p = foo.split('\t')
     #print(p[4],numcase,p[3],p[0],ncase[foo],label)
     print(foo,ncase[foo],label)
     sawit = 1
   if( sawit): print()

def nounparad(stemtype,nparad,label):
   paradlist['n'+'@' + stemtype + '@' + nparad + '@' + label] = 1
   printnumcase(stemtype,nparad,vocsg,"voc sg",label)
   printnumcase(stemtype,nparad,nomsg,"nom sg",label)
   printnumcase(stemtype,nparad,gensg,"gen sg",label)
   printnumcase(stemtype,nparad,datsg,"dat sg",label)
   printnumcase(stemtype,nparad,accsg,"acc sg",label)

   printnumcase(stemtype,nparad,vocd,"voc du",label)
   printnumcase(stemtype,nparad,nomd,"nom du",label)
   printnumcase(stemtype,nparad,gend,"gen du",label)
   printnumcase(stemtype,nparad,datd,"dat du",label)
   printnumcase(stemtype,nparad,accd,"acc du",label)

   printnumcase(stemtype,nparad,vocpl,"voc pl",label)
   printnumcase(stemtype,nparad,nompl,"nom pl",label)
   printnumcase(stemtype,nparad,genpl,"gen pl",label)
   printnumcase(stemtype,nparad,datpl,"dat pl",label)
   printnumcase(stemtype,nparad,accpl,"acc pl",label)


def pickforms():
   for curkey in tokens:
     paradinfo = parads[curkey]
     pfields = paradinfo.split('@')
#     if(pfields[2] == stemtype):

def checkform(curkey):
  paradinfo = parads[curkey]
  pfields = paradinfo.split('@')
  stemtype = pfields[2]
  if( not lemmas[curkey] in illems):
       illems[lemmas[curkey]] = 0
       ilfreq[lemmas[curkey]] = '0.00'
  if( not lemmas[curkey] in odlems):
       odlems[lemmas[curkey]] = 0
       odfreq[lemmas[curkey]] = '0.00'

  for foo in paradlist:
    pmatch = foo.split('@')
    #print("comp",pmatch[1],"stem",stemtype,"para",pmatch[2])
    if(not pmatch[1] == stemtype):
      continue
    if( pmatch[0] == 'v' and not re.search(pmatch[2],postags[curkey])):
      continue
        
    if( pmatch[0] == 'n' and not pmatch[2] and re.search(r'[cs]$',postags[curkey])): #skip comp and superl by def
      continue

    print(pmatch[3],pmatch[0],str(homerlems[lemmas[curkey]]),str(illems[lemmas[curkey]]),str(odlems[lemmas[curkey]]),ilfreq[lemmas[curkey]],odfreq[lemmas[curkey]],savelines[curkey])
    return(1)
  addunit(stemtype,missedstemtypes)
  print("nomatch",pmatch[0],str(homerlems[lemmas[curkey]]),str(illems[lemmas[curkey]]),str(odlems[lemmas[curkey]]),ilfreq[lemmas[curkey]],odfreq[lemmas[curkey]],savelines[curkey])


def filterforms():
   for curkey in tokens:
     print("line",savelines[curkey])
     if( wordids[curkey] in sawkeys):
       continue
     else:
       print("keep going")
     sawkeys[wordids[curkey]] = 1
     checkform(curkey)



def pharr03():
  nounparad("h_hs",'',"pharr03")

def pharr04():
  nounparad("a_hs",'',"pharr04")

def pharr05():
  printtensemoodvoice("w_stem","pia",'pharr05')
  printtensemoodvoice("ew_pr","pia",'pharr05')
  printtensemoodvoice("aw_pr","pia",'pharr05')
  printtensemoodvoice("ow_pr","pia",'pharr05')

def pharr06():
  nounparad("os_ou",'',"pharr06")
  nounparad("eos_eou",'',"pharr06")
  nounparad("oos_oou",'',"pharr06")
  nounparad("os_h_on",'',"pharr06")
  nounparad("eos_eh_eon",'',"pharr06")
  nounparad("oos_oh_oon",'',"pharr06")
  nounparad("os_on",'',"pharr06") 
  nounparad("oos_oon",'',"pharr06") 

def pharr08():
  nounparad("art_adj",'',"pharr08")

def pharr09():
  printtensemoodvoice("w_stem","iia",'pharr09')
  printtensemoodvoice("ew_pr","iia",'pharr09')
  printtensemoodvoice("aw_pr","iia",'pharr09')
  printtensemoodvoice("ow_pr","iia",'pharr09')

def pharr10():
  printtensemoodvoice("reg_fut","fia",'pharr10')
  printtensemoodvoice("aor1","aia",'pharr10')

def pharr11():
  nounparad("hs_ou",'',"pharr11")
  nounparad("ehs_eou",'',"pharr11")
  printtensemoodvoice("aor2","aia",'pharr11')
  printtensemoodvoice("ath_h_aor","aia",'pharr11')

def pharr13():
  nounparad("eus_ews",'',"pharr12")
  nounparad("is_ews",'',"pharr12")
  nounparad("hs_eos",'',"pharr12")
  nounparad("c_ktos",'',"pharr12")

def pharr16():
 printtensemoodvoice("w_stem","pie",'pharr16')
 printtensemoodvoice("w_stem","pip",'pharr16')
 printtensemoodvoice("w_stem","pim",'pharr16')

 printtensemoodvoice("ew_pr","pie",'pharr16')
 printtensemoodvoice("ew_pr","pip",'pharr16')
 printtensemoodvoice("ew_pr","pim",'pharr16')
 printtensemoodvoice("reg_fut","fie",'pharr16')
 printtensemoodvoice("reg_fut","fim",'pharr16')

def pharr17():
 printtensemoodvoice("aor1","aie",'pharr17')
 printtensemoodvoice("aor1","aip",'pharr17')
 printtensemoodvoice("aor1","aim",'pharr17')
 printtensemoodvoice("aor2","aie",'pharr17')
 printtensemoodvoice("aor2","aim",'pharr17')
 printtensemoodvoice("w_stem","iie",'pharr17')
 printtensemoodvoice("w_stem","iim",'pharr17')
 printtensemoodvoice("w_stem","iip",'pharr17')
 printtensemoodvoice("aw_pr","iie",'pharr17')
 printtensemoodvoice("aw_pr","iim",'pharr17')
 printtensemoodvoice("aw_pr","iip",'pharr17')
 printtensemoodvoice("ew_pr","iie",'pharr17')
 printtensemoodvoice("ew_pr","iim",'pharr17')
 printtensemoodvoice("ew_pr","iip",'pharr17')

def pharr18():
 printtensemoodvoice("perf_act","",'pharr18')
 printtensemoodvoice("perf2_act","",'pharr18')

def pharr19():
 printtensemoodvoice("w_stem","pna",'pharr19')
 printtensemoodvoice("w_stem","pnp",'pharr19')
 printtensemoodvoice("w_stem","pne",'pharr19')
 printtensemoodvoice("w_stem","pnm",'pharr19')

 printtensemoodvoice("ew_pr","pna",'pharr19')
 printtensemoodvoice("ew_pr","pnp",'pharr19')
 printtensemoodvoice("ew_pr","pne",'pharr19')
 printtensemoodvoice("ew_pr","pnm",'pharr19')

 printtensemoodvoice("aw_pr","pna",'pharr19')
 printtensemoodvoice("aw_pr","pnp",'pharr19')
 printtensemoodvoice("aw_pr","pne",'pharr19')
 printtensemoodvoice("aw_pr","pnm",'pharr19')

 printtensemoodvoice("ow_pr","pna",'pharr19')
 printtensemoodvoice("ow_pr","pnp",'pharr19')
 printtensemoodvoice("ow_pr","pne",'pharr19')
 printtensemoodvoice("ow_pr","pnm",'pharr19')

 printtensemoodvoice("aor1","ana",'pharr19')
 printtensemoodvoice("aor1","anp",'pharr19')
 printtensemoodvoice("aor1","ane",'pharr19')
 printtensemoodvoice("aor1","anm",'pharr19')

 printtensemoodvoice("aor2","ana",'pharr19')
 printtensemoodvoice("aor2","anp",'pharr19')
 printtensemoodvoice("aor2","ane",'pharr19')
 printtensemoodvoice("aor2","anm",'pharr19')

 printtensemoodvoice("reg_fut","fna",'pharr19')
 printtensemoodvoice("reg_fut","fnp",'pharr19')
 printtensemoodvoice("reg_fut","fne",'pharr19')
 printtensemoodvoice("reg_fut","fnm",'pharr19')

 printtensemoodvoice("perf_act","lna",'pharr19')
 printtensemoodvoice("perf2_act","lna",'pharr19')

def pharr20():
 printtensemoodvoice("w_stem","ppa","pharr20")
 printtensemoodvoice("ow_pr","ppa","pharr20")
 printtensemoodvoice("ew_pr","ppa","pharr20")
 printtensemoodvoice("aw_pr","ppa","pharr20")
 printtensemoodvoice("reg_fut","fpa","pharr20")
 printtensemoodvoice("aor1","apa","pharr20")
 printtensemoodvoice("aor2","apa","pharr20")
 printtensemoodvoice("perf_act",'rpa',"pharr20")

def pharr21():
 printtensemoodvoice("w_stem","ppe","pharr21")
 printtensemoodvoice("w_stem","ppm","pharr21")
 printtensemoodvoice("ow_pr","ppe","pharr21")
 printtensemoodvoice("ow_pr","ppm","pharr21")
 printtensemoodvoice("ew_pr","ppe","pharr21")
 printtensemoodvoice("ew_pr","ppm","pharr21")
 printtensemoodvoice("aw_pr","ppe","pharr21")
 printtensemoodvoice("aw_pr","ppm","pharr21")
 printtensemoodvoice("reg_fut","fpe","pharr21")
 printtensemoodvoice("aor1","ape","pharr21")
 printtensemoodvoice("aor1","apm","pharr21")
 printtensemoodvoice("aor2","ape","pharr21")
 printtensemoodvoice("aor2","apm","pharr21")
 printtensemoodvoice("perf_act",'rpe',"pharr21")

def pharr22():
 printtensemoodvoice("fut_perf","tie",'pharr22')
 printtensemoodvoice("perfp_vow","",'pharr22')
 printtensemoodvoice("perfp_d","",'pharr22')
 printtensemoodvoice("perfp_p","",'pharr22')
 printtensemoodvoice("perfp_r","",'pharr22')
 printtensemoodvoice("perfp_s","",'pharr22')

def pharr23():
 printtensemoodvoice("w_stem","psa",'pharr23')
 printtensemoodvoice("w_stem","pse",'pharr23')
 printtensemoodvoice("w_stem","psp",'pharr23')
 printtensemoodvoice("w_stem","psm",'pharr23')

 printtensemoodvoice("ew_pr","psa",'pharr23')
 printtensemoodvoice("ew_pr","pse",'pharr23')
 printtensemoodvoice("ew_pr","psp",'pharr23')
 printtensemoodvoice("ew_pr","psm",'pharr23')

 printtensemoodvoice("aw_pr","psa",'pharr23')
 printtensemoodvoice("aw_pr","pse",'pharr23')
 printtensemoodvoice("aw_pr","psp",'pharr23')
 printtensemoodvoice("aw_pr","psm",'pharr23')

 printtensemoodvoice("ow_pr","psa",'pharr23')
 printtensemoodvoice("ow_pr","pse",'pharr23')
 printtensemoodvoice("ow_pr","psp",'pharr23')
 printtensemoodvoice("ow_pr","psm",'pharr23')

 printtensemoodvoice("reg_fut","fsa",'pharr23')
 printtensemoodvoice("reg_fut","fse",'pharr23')
 printtensemoodvoice("reg_fut","fsp",'pharr23')
 printtensemoodvoice("aor1","asa",'pharr23')
 printtensemoodvoice("aor1","ase",'pharr23')
 printtensemoodvoice("aor1","asp",'pharr23')
 printtensemoodvoice("aor1","asm",'pharr23')
 printtensemoodvoice("aor2","asa",'pharr23')
 printtensemoodvoice("aor2","ase",'pharr23')
 printtensemoodvoice("aor2","asp",'pharr23')
 printtensemoodvoice("aor2","asm",'pharr23')
 printtensemoodvoice("perf_act","lsa",'pharr23')

def pharr24():
 printtensemoodvoice("w_stem","pma",'pharr24')
 printtensemoodvoice("w_stem","pma",'pharr24')
 printtensemoodvoice("w_stem","pme",'pharr24')
 printtensemoodvoice("w_stem","pmm",'pharr24')

 printtensemoodvoice("ew_pr","pma",'pharr24')
 printtensemoodvoice("ew_pr","pma",'pharr24')
 printtensemoodvoice("ew_pr","pme",'pharr24')
 printtensemoodvoice("ew_pr","pmm",'pharr24')

 printtensemoodvoice("aw_pr","pma",'pharr24')
 printtensemoodvoice("aw_pr","pma",'pharr24')
 printtensemoodvoice("aw_pr","pme",'pharr24')
 printtensemoodvoice("aw_pr","pmm",'pharr24')

 printtensemoodvoice("ow_pr","pma",'pharr24')
 printtensemoodvoice("ow_pr","pma",'pharr24')
 printtensemoodvoice("ow_pr","pme",'pharr24')
 printtensemoodvoice("ow_pr","pmm",'pharr24')

 printtensemoodvoice("reg_fut","fma",'pharr24')
 printtensemoodvoice("reg_fut","fme",'pharr24')
 printtensemoodvoice("reg_fut","fmm",'pharr24')
 printtensemoodvoice("reg_fut","fmp",'pharr24')

 printtensemoodvoice("aor1","ama",'pharr24')
 printtensemoodvoice("aor1","ame",'pharr24')
 printtensemoodvoice("aor1","amp",'pharr24')
 printtensemoodvoice("aor1","amm",'pharr24')

 printtensemoodvoice("aor2","ama",'pharr24')
 printtensemoodvoice("aor2","ame",'pharr24')
 printtensemoodvoice("aor2","amp",'pharr24')
 printtensemoodvoice("aor2","amm",'pharr24')

 printtensemoodvoice("perf_act","lma",'pharr24')

def pharr25():
 printtensemoodvoice("w_stem","ppe",'pharr25')
 printtensemoodvoice("w_stem","ppm",'pharr25')
 printtensemoodvoice("reg_fut","fpe",'pharr25')
 printtensemoodvoice("reg_fut","fpp",'pharr25')
 printtensemoodvoice("reg_fut","fpm",'pharr25')
 printtensemoodvoice("aor1","ape",'pharr25')
 printtensemoodvoice("aor1","app",'pharr24')

def pharr26():
 printtensemoodvoice("w_stem","poa",'pharr26')
 printtensemoodvoice("w_stem","poe",'pharr26')
 printtensemoodvoice("w_stem","pop",'pharr26')

 printtensemoodvoice("ew_pr","poa",'pharr26')
 printtensemoodvoice("ew_pr","poe",'pharr26')
 printtensemoodvoice("ew_pr","pop",'pharr26')

 printtensemoodvoice("ow_pr","poa",'pharr26')
 printtensemoodvoice("ow_pr","poe",'pharr26')
 printtensemoodvoice("ow_pr","pop",'pharr26')

 printtensemoodvoice("aw_pr","poa",'pharr26')
 printtensemoodvoice("aw_pr","poe",'pharr26')
 printtensemoodvoice("aw_pr","pop",'pharr26')

 printtensemoodvoice("reg_fut","foa",'pharr26')
 printtensemoodvoice("reg_fut","foe",'pharr26')
 printtensemoodvoice("reg_fut","fop",'pharr26')
 printtensemoodvoice("aor1","aoa",'pharr26')
 printtensemoodvoice("aor1","aoe",'pharr26')
 printtensemoodvoice("aor1","aop",'pharr26')
 printtensemoodvoice("aor1","aom",'pharr26')
 printtensemoodvoice("aor2","aoa",'pharr26')
 printtensemoodvoice("aor2","aoe",'pharr26')
 printtensemoodvoice("aor2","aop",'pharr26')
 printtensemoodvoice("aor2","aom",'pharr26')
 printtensemoodvoice("perf_act","loa",'pharr26')

def pharr27():
 printtensemoodvoice("aor_pass","",'pharr27')
 printtensemoodvoice("aor2_pass","",'pharr27')

def pharr28():
  nounparad("wn_on_comp",'c',"pharr28")
  print("pastcomp")
  nounparad("wn_on",'',"pharr28")
  nounparad("eis_essa",'',"pharr28")
  nounparad("oeis_oessa",'',"pharr28")
  nounparad("heis_hessa",'',"pharr28")
  nounparad("hs_es",'',"pharr28")
  nounparad("as_aina_an",'',"pharr28")

def pharr32():
  printtensemoodvoice("ami_pr","",'pharr32')
  printtensemoodvoice("emi_pr","",'pharr32')
  printtensemoodvoice("omi_pr","",'pharr32')

  printtensemoodvoice("ami_aor","",'pharr32')
  printtensemoodvoice("emi_aor","",'pharr32')
  printtensemoodvoice("omi_aor","",'pharr32')

  printtensemoodvoice("ath_h_aor","",'pharr32')

def pharr38():
  nounparad("os_h_on",'cs',"pharr38")
  nounparad("os_on",'cs',"pharr38")
  nounparad("hs_es",'cs',"pharr38")

def nopharr():
  nounparad("aos_aou",'',"nopharr")
  nounparad("ar_atos",'',"nopharr")
  nounparad("as_antos",'',"nopharr")
  nounparad("as_asa_an",'',"nopharr")
  nounparad("as_aos",'',"nopharr")
  nounparad("c_gos",'',"nopharr")
  nounparad("c_kos",'',"nopharr")
  nounparad("hr_eros",'',"nopharr")
  nounparad("hn_enos",'',"nopharr")
  nounparad("is_idos",'',"nopharr")
  nounparad("is_iCdos",'',"nopharr")
  nounparad("klehs_kleous",'',"nopharr")
  nounparad("ma_matos",'',"nopharr")
  nounparad("n_nos",'',"nopharr")
  nounparad("ous_ontos",'',"nopharr")
  nounparad("pous_podos",'',"nopharr")
  nounparad("qric_trixos",'',"nopharr")
  nounparad("r_ros",'',"nopharr")
  nounparad("s_dos",'',"nopharr")
  nounparad("s_nos",'',"nopharr")
  nounparad("s_os",'',"nopharr")
  nounparad("s_qos",'',"nopharr")
  nounparad("s_sos",'',"nopharr")
  nounparad("s_tos",'',"nopharr")
  nounparad("t_tos",'',"nopharr")
  nounparad("us_ews",'',"nopharr")
  nounparad("us_uos",'',"nopharr")
  nounparad("uLs_uos",'',"nopharr")
  nounparad("us_eia_u",'',"nopharr")
  nounparad("verb_adj2",'',"nopharr")
  nounparad("w_oos",'',"nopharr")
  nounparad("wn_onos",'',"nopharr")
  nounparad("wn_ontos",'',"nopharr")
  nounparad("wn_ousa_on",'',"nopharr")
  nounparad("wr_oros",'',"nopharr")
  nounparad("ws_w",'',"nopharr")
  nounparad("ws_w_long",'',"nopharr")
  nounparad("ws_wos",'',"nopharr")
  nounparad("ws_oos",'',"nopharr")
  nounparad("y_pos",'',"nopharr")

  printtensemoodvoice("ami_short","",'nopharr')
  printtensemoodvoice("ath_primary","",'nopharr')
  printtensemoodvoice("ath_secondary","",'nopharr')
  printtensemoodvoice("ath_u_aor","",'nopharr')
  printtensemoodvoice("ath_w_aor","",'nopharr')
  printtensemoodvoice("ajw_pr","",'nopharr')
  printtensemoodvoice("aw_fut","",'nopharr')
  printtensemoodvoice("aw_pr","iim",'nopharr')
  printtensemoodvoice("aw_pr","iip",'nopharr')
  printtensemoodvoice("evw_pr","",'nopharr')
  printtensemoodvoice("w_stem","iie",'nopharr')
  printtensemoodvoice("w_stem","iip",'nopharr')
  printtensemoodvoice("ew_fut","",'nopharr')
  printtensemoodvoice("umi_pr","",'nopharr')
  printtensemoodvoice("umi_aor","",'nopharr')

pharr03()
pharr04()
pharr05()
pharr06()
pharr08()
pharr09()
pharr10()
pharr11()
pharr13()
pharr16()
pharr17()
pharr18()
pharr19()
pharr20()
pharr21()
pharr22()
pharr23()
pharr24()
pharr25()
pharr26()
pharr27()
pharr28()
pharr32()
pharr38()
nopharr()

for foo in paradlist:
  print("parad",foo.split('@'))

filterforms()
for foo in dict(sorted(missedstemtypes.items(), key=operator.itemgetter(1),reverse=True)):
  print("missed",foo,missedstemtypes[foo])

for foo in infact:
   print("infact",foo,infact[foo])
