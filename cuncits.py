#!/usr/bin/python
  
import sys
import re

curlemma = ''
cuncits = {}
cunlemmas = {}

for w in sys.stdin.readlines():
        if( re.search("cunliffe-",w)):
          newent =1
        if( re.search('textpart" n="',w)):
         m=re.search('textpart" n="([^"]+)',w)
 #        print(m[1])
         curlemma = m[1]
         curlemma = re.sub("†", "",curlemma)
         cunlemmas[curlemma] = 1
         print("lemsrc",curlemma,w)
        #for cit in re.finditer(r'<bibl n=.([IO][^"]+',w):
        for cit in re.finditer('<bibl[ ]+n=.([HIO][^>]+)">',w):
         if(curlemma):
          newcit = re.sub("Hom\. ","",cit.group(1))
          newcit = re.sub("Il\. ","urn:cts:greekLit:tlg0012.tlg001:",newcit)
          newcit = re.sub("Od\. ","urn:cts:greekLit:tlg0012.tlg002:",newcit)
#          print(newcit,curlemma)
          citlem = newcit + "@" + curlemma
          cuncits[citlem] = 1
          #print(citlem)

     
tbfile = "/Users/gcrane/github/gAGDT/data/xml/tlg0012.tlg001.perseus-grc1.tb.xml"
with open(tbfile) as f:
 for w in f:
  curcite = ''
  curlemma = ''
  if( re.search('cite="([^"]+)"',w)):
    m=re.search('cite="([^"]+)"',w)
    curcite = m[1]
  if( re.search('lemma="([^"]+)"',w)):
    m=re.search('lemma="([^"]+)"',w)
    curlemma = m[1]
  if( re.search('form="([^"]+)"',w)):
    m=re.search('form="([^"]+)"',w)
    curform = m[1]
  if( curlemma == "," or curlemma == "." or curlemma == ";" or curlemma == "·"):
    continue
  if(  curlemma and curlemma not in cunlemmas ):
   print(curform,"lemmafail",curcite,curlemma)
   
  if( curcite and curlemma ):
   if( curcite+'@'+curlemma in cuncits ):
     print(curform,"hit",curcite,curlemma)
   else:
     print(curform,"citefail",curcite,curlemma)

