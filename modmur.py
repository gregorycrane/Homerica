#!/usr/bin/python
  
import sys
import re

ethtable = {}
curlemma = ''

simpsub = {}
simpsub['abide'] = "remain"
simpsub['anigh'] = "near"
simpsub['bade'] = "commanded"
simpsub['badest'] = "commanded"
simpsub['bid'] = "command"
simpsub['bids'] = "commands"
simpsub['dravest'] = "drove"
simpsub['folk'] = "people"
simpsub['gainsay'] = "deny"
simpsub['hadst'] = "had"
simpsub['hath'] = "had"
simpsub['hast'] = "have"
simpsub['hearken'] = "listen"
simpsub['hearkened'] = "listened"
simpsub['hither'] = "here"
simpsub['thee'] = "you"
simpsub['thou'] = "you"
simpsub['thy'] = "your"
simpsub['thyself'] = "yourself"
simpsub['ye'] = "you"
simpsub['haply'] = "by chance"
simpsub['kinsfolk'] = "family"
simpsub['loathly'] = "disgusting"
simpsub['nigh'] = "near"
simpsub['perchance'] = "perchance"
simpsub['shew'] = "show"
simpsub['shouldst'] = "should"
simpsub['smitest'] = "strike"
simpsub['smiting'] = "striking"
simpsub['smitten'] = "struck"
simpsub['spake'] = "spoke"
simpsub['succour'] = "help"
simpsub['thine'] = "your"
simpsub['twain'] = "two"
simpsub['ween'] = "believe"
simpsub['whenso'] = "whenever"
simpsub['Wherefore'] = "For which reason"
simpsub['wherefore'] = "for which reason"

compsub = {}
compsub['art'] = 'a'
compsub['baneful'] = 'a'
compsub['Nay'] = 'a'
compsub['nay'] = 'a'
compsub['pratest'] = 'a'
compsub['wrought'] = 'a'

f = open("eth-3rd-pers.txt","r")
for l in f:
  args = l.split('\t')
  ethtable[args[0]] = args[1]
  #print(args[0],ethtable[args[0]])
f.close()

f = open("est-2nd-pers.txt","r")
for l in f:
  args = l.split('\t')
  ethtable[args[0]] = args[1]
  #print(args[0],ethtable[args[0]])
f.close()

def do_eth(s):
   t = re.sub("<[^>]+>"," ",s)
   t = re.sub('[\.,;:"!,\s]+'," ",t)
   checkedwords = {}
   args = t.split(" ")
   for a in args:
     if(a in checkedwords):
      continue
     if(a in ethtable):
  #     print("eth-s",a,ethtable[a])
       s = re.sub('\\b' + a + "\\b","<mod n='" + a + "'>" + ethtable[a] + "</mod>",s)
     if(a in compsub):
       s = re.sub('\\b' + a + "\\b","<sic>" + a + "</sic>",s)
     if(a in simpsub and a  not in checkedwords):
       s = re.sub('\\b' + a + "\\b","<mod n='" + a + ":simpsub'>" +  simpsub[a] + "</mod>",s)
     checkedwords[a] = 1

   return(s)


intext = 0
for w in sys.stdin.readlines():
    if( re.search("<text",w) ):
      intext = 1
    if( intext ):
     w = re.sub("<s\\b","\n\n<s",w)
     w = re.sub("^[ \t]+","",w)
     w = re.sub("\\be'en\\b","even",w) # I hate this form and I am not even leving a race of it.
    w = do_eth(w)
    print(w,end='')
     
