#!/usr/bin/env python3
  
import sys
import re
import operator


endingkeys = ['nu_movable','iterative']
from greek_accentuation.characters import *
from greek_accentuation.syllabify import *
from greek_accentuation.accentuation import *

h_hs_lemmas = {}
h_hs_lemmas_il01 = {}
h_hs_forms = {}
h_hs_forms_il01 = {}

os_h_on_f_forms_il01 = {}

a_hs_lemmas = {}
a_hs_lemmas_il01 = {}
a_hs_forms = {}
a_hs_forms_il01 = {}

os_h_on_lemmas = {}
os_h_on_lemmas_il01 = {}
os_h_on_forms = {}
os_h_on_forms_il01 = {}

os_ou_lemmas = {}
os_ou_lemmas_il01 = {}
os_ou_forms = {}
os_ou_forms_il01 = {}
lemmalist = {}
lemmalist_il01 = {}


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

numcasedbase = {}
numcasedbase['s\ta'] = ''
enddbase = {}
verbals = {}
verbalcounts= {}
verbalcounts_il01 = {}

nominals = {}
nominalcounts= {}
nominalcounts_il01 = {}
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

sawkeys = {}

def addunit(s,l):
  if( s in l):
   l[s] = l[s] + 1
  else:
   l[s] = 1

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

    m = re.search('^[v]([123][sdp])(.[^p].)...',postags[curkey])
    if( m ):
      vparad = m.group(2)
      pnum = m.group(1)
      verbals[curkey] = rawforms[curkey] + "\t" + vparad + "\t" + pnum + "\t" + lemmas[curkey] + "\t" + stemtype + "\t" + keys

      addunit(verbals[curkey],verbalcounts)
      if( re.search("\-end",p[1])):
         tmpend = re.sub(r".*\-([^\-]+)$",'\g<1>',p[0])
         endkey = tmpend + "\t" + vparad + "\t" + pnum + "\t" + stemtype + "\t" + ekey
         addunit(endkey,enddbase)
         #print("endkey",endkey)
         if( pnum == '1s'): addunit(endkey,sg1)
         if( pnum == '2s'): addunit(endkey,sg2)
         if( pnum == '3s'): addunit(endkey,sg3)

         if( pnum == '1d'): addunit(endkey,du1)
         if( pnum == '2d'): addunit(endkey,du2)
         if( pnum == '3d'): addunit(endkey,du3)

         if( pnum == '1p'): addunit(endkey,pl1)
         if( pnum == '2p'): addunit(endkey,pl2)
         if( pnum == '3p'): addunit(endkey,pl3)

    m = re.search('^([napv]).([sdp])(...)([mfn])([vngda])[^cs]',postags[curkey])
    if( m ):
        numcase = m.group(2) + "\t" +  m.group(5)
        gender = m.group(4)
        if( re.search(r'^[a-z]+$',m.group(3))):
          stemtype= stemtype + '-' + m.group(3)
          #print("participal",stemtype)
        nominals[curkey] = rawforms[curkey] + "\t" + numcase + "\t" + lemmas[curkey] + "\t" + gender + "\t" + stemtype + "\t" + keys
        addunit(nominals[curkey],nominalcounts)
        #print(nominals[curkey])
        if( re.search("\-end",p[1])):
            tmpend = re.sub(r".*\-([^\-]+)$",'\g<1>',p[0])
            endkey = tmpend + "\t" + numcase + "\t" + gender + "\t" + stemtype + "\t" + ekey
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

        if( re.search('tlg001:1\.',wordids[curkey] )):
          addunit(nominals[curkey],nominalcounts_il01)
        #print("nominals",curkey,nominals[curkey],nominalcounts[nominals[curkey]])
    else:
        gennumcase = ''
        nominals[curkey] = "missing data"


      


    addunit(fields[3],lemmalist)
    if( re.search('tlg001:1\.',curkey)):
      addunit(fields[3],lemmalist_il01)
    
    m = re.search(r'^([a-z])',postags[curkey])
    if( m ):
     if( m.group(1) in postable):
      postable[m.group(1)] = 1 +  postable[m.group(1)]
     else:
      postable[m.group(1)] = 1
    if (0):
     print("wordids",wordids[curkey])
     print("sentids",sentids[curkey])
     print("lemmas",lemmas[curkey])
     print("rawforms",rawforms[curkey])
     print("postags",postags[curkey])
     print("depids",depids[curkey])
     print("syntags",syntags[curkey])
     print("parads",parads[curkey])
   
    paradinfo = parads[curkey].split('@')

  
def printpnum(stemtype,tensemoodvoice,pnum,label):
   sawit = 0
   for foo in dict(sorted(pnum.items(), key=operator.itemgetter(1),reverse=True)):
    if( re.search(stemtype,foo) and re.search(tensemoodvoice,foo)):
     p = foo.split('\t')
     print(p[3],label,foo,pnum[foo])
     sawit = 1
   if( sawit): print()

def printtensemoodvoice(stemtype,tensemoodvoice,label):
  printpnum(stemtype,tensemoodvoice,sg1,"1st sg")
  printpnum(stemtype,tensemoodvoice,sg2,"2nd sg")
  printpnum(stemtype,tensemoodvoice,sg3,"3rd sg")

  printpnum(stemtype,tensemoodvoice,du1,"1st du")
  printpnum(stemtype,tensemoodvoice,du2,"2nd du")
  printpnum(stemtype,tensemoodvoice,du3,"3rd du")
    
  printpnum(stemtype,tensemoodvoice,pl1,"1st pl")
  printpnum(stemtype,tensemoodvoice,pl2,"2nd pl")
  printpnum(stemtype,tensemoodvoice,pl3,"3rd pl")
  for curkey in tokens:
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
    print("verbkey",label,cit,sentids[curkey],cit,verbals[curkey],verbalcounts[verbals[curkey]])
    
    
def printnumcase(curparad,ncase,label):
   sawit = 0
   if( ncase == {}): return
   for foo in dict(sorted(ncase.items(), key=operator.itemgetter(1),reverse=True)):
    if( re.search(curparad,foo)):
     p = foo.split('\t')
     print(p[4],label,p[3],p[0],ncase[foo])
     sawit = 1
   if( sawit): print()

def nounparad(stemtype,vparad,label):
   printnumcase(stemtype,vocsg,"voc sg")
   printnumcase(stemtype,nomsg,"nom sg")
   printnumcase(stemtype,gensg,"gen sg")
   printnumcase(stemtype,datsg,"dat sg")
   printnumcase(stemtype,accsg,"acc sg")

   printnumcase(stemtype,vocd,"voc du")
   printnumcase(stemtype,nomd,"nom du")
   printnumcase(stemtype,gend,"gen du")
   printnumcase(stemtype,datd,"dat du")
   printnumcase(stemtype,accd,"acc du")

   printnumcase(stemtype,vocpl,"voc pl")
   printnumcase(stemtype,nompl,"nom pl")
   printnumcase(stemtype,genpl,"gen pl")
   printnumcase(stemtype,datpl,"dat pl")
   printnumcase(stemtype,accpl,"acc pl")

   for curkey in tokens:
     paradinfo = parads[curkey]
#skip preps like antion
     if( re.search(r'^r',postags[curkey])):
      continue
# skip comparative and superlatives for now
     if( re.search('[cs]$',postags[curkey])):
      continue
     m = re.search('([vdanp]).([sdp])(...)([mfn])([vngda]).$',postags[curkey])
     if( m ):
       if(m.group(1) == 'd'):
         continue
       if( vparad and not vparad == m.group(3)):
          continue
       numcase = m.group(2) + "\t" + m.group(5)
       gender = m.group(4)
     else:
       continue
       numcase = 'nonumcase'
       gender = "nogender"
     if( not re.search(stemtype,paradinfo)):
      continue
     #print("alive",curkey,paradinfo)
     m = re.search('(tlg00[12]:[0-9]+\.[0-9]+)',wordids[curkey])
     if(m):
      cit = m.group(1)
     else:
      cit = "nocit"
     if( re.search(stemtype,paradinfo)):
       p = paradinfo.split('@')
       if( len(p) == 4 and p[3]):
         keys = p[3]
         #print("haskeys",p[3])
         #keys = 'haskeys'
       else:
         keys = ''
       if( vparad ):
        nomkey = rawforms[curkey] + "\t" + numcase + "\t" + lemmas[curkey] + "\t" + gender + "\t" + stemtype + '-' + vparad + "\t" + keys
       else:
        nomkey = rawforms[curkey] + "\t" + numcase + "\t" + lemmas[curkey] + "\t" + gender + "\t" + stemtype + "\t" + keys
       if( nomkey in nominalcounts_il01):
         il1cnt = str(nominalcounts_il01[nomkey])
       else:
         il1cnt = 0

       if( lemmas[curkey] in lemmalist_il01):
         il1lem = str(lemmalist_il01[lemmas[curkey]])
       else:
         il1lem = 0
       print("nomkey",label,cit,sentids[curkey],nomkey,il1cnt,str(nominalcounts[nomkey]),lemmas[curkey],il1lem,str(lemmalist[lemmas[curkey]]))


def pharr03():
  nounparad("h_hs",'',"pharr04")

def pharr04():
  nounparad("a_hs",'',"pharr04")

def pharr05():
  printtensemoodvoice("w_stem","pia",'pharr05')

def pharr06():
  nounparad("os_ou",'',"pharr06")
  nounparad("os_h_on",'',"pharr06")

def pharr08():
  nounparad("art_adj",'',"pharr08")

def pharr09():
  printtensemoodvoice("w_stem","iia",'pharr09')

def pharr10():
  printtensemoodvoice("w_stem","fia",'pharr10')
  printtensemoodvoice("aor1","aia",'pharr10')

def pharr11():
  nounparad("hs_ou",'',"pharr11")

def pharr12():
  nounparad("eus_ews",'',"pharr12")
  nounparad("is_ews",'',"pharr12")
  nounparad("hs_eos",'',"pharr12")

def pharr20():
 nounparad("w_stem","ppa","pharr20")
 nounparad("ow_pr","ppa","pharr20")
 nounparad("ew_pr","ppa","pharr20")
 nounparad("reg_fut","fpa","pharr20")
 nounparad("aor1","apa","pharr20")
 nounparad("perf_act",'rpa',"pharr20")

printtensemoodvoice("aor1","aie",'pharr17')
printtensemoodvoice("aor1","aip",'pharr17')

printtensemoodvoice("w_stem","pie",'pharr16')
printtensemoodvoice("w_stem","pip",'pharr16')
printtensemoodvoice("reg_fut","pie",'pharr16')

printtensemoodvoice("w_stem","iie",'pharr17')
printtensemoodvoice("w_stem","iip",'pharr17')

printtensemoodvoice("perf_act","lia",'pharr18')
printtensemoodvoice("perf2_act","lia",'pharr18')
printtensemoodvoice("perf_act","ria",'pharr18')
printtensemoodvoice("perf2_act","ria",'pharr18')
pharr03()
pharr04()
pharr05()
pharr06()
pharr08()
pharr09()
pharr10()
pharr11()
pharr12()

