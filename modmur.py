#!/usr/bin/python
  
import sys
import re

ethtable = {}
curlemma = ''

simpsub = {}
simpsub['abide'] = "remain"
simpsub['adread'] = "afraid"
simpsub['Albeit'] = "Although"
simpsub['albeit'] = "although"
simpsub['amid'] = "among"
simpsub['anigh'] = "near"
simpsub['anywise'] = "in any way"
simpsub['athrob'] = "throbbing"
simpsub['aught'] = "anything"
simpsub['bade'] = "commanded"
simpsub['badest'] = "commanded"
simpsub['bid'] = "command"
simpsub['bids'] = "commands"
simpsub['brake'] = "broke"
simpsub['builded'] = "built"
simpsub['car'] = "chariot"
simpsub['chine'] = "back-meat"
simpsub['coursing'] = "racing"
simpsub['deem'] = "think"
simpsub['deemed'] = "thought"
simpsub['didst'] = "did"
simpsub['doth'] = "does"
simpsub['dost'] = "do"
simpsub['drave'] = "drove"
simpsub['dravest'] = "drove"
simpsub['dykes'] = "bridges"
simpsub['ere'] = "before"
simpsub['essayed'] = "tried"
simpsub['folk'] = "people"
simpsub['fordone'] = "done in"
simpsub['froward'] = "willful"
simpsub['gainsay'] = "deny"
simpsub['gat'] = "got"
simpsub['hadst'] = "had"
simpsub['hath'] = "has"
simpsub['hast'] = "have"
simpsub['hasted'] = "hastened"
simpsub['Hearken'] = "Listen"
simpsub['hearken'] = "listen"
simpsub['hearkened'] = "listened"
simpsub['hither'] = "here"
simpsub['Howbeit'] = "However"
simpsub['howbeit'] = "however"
simpsub['kine'] = "cattle"
simpsub['thee'] = "you"
simpsub['thou'] = "you"
simpsub['thy'] = "your"
simpsub['thyself'] = "yourself"
simpsub['ye'] = "you"
simpsub['haply'] = "by chance"
simpsub['kinsfolk'] = "family"
simpsub['loathly'] = "disgusting"
simpsub['naught'] = "nothing"
simpsub['nigh'] = "near"
simpsub['nowise'] = "in no way"
simpsub['perchance'] = "perchance"
simpsub['reck'] = "care"
simpsub['rede'] = "counsel"
simpsub['saidst'] = "said"
simpsub['shalt'] = "shall"
simpsub['shew'] = "show"
simpsub['shewed'] = "showed"
simpsub['shouldst'] = "should"
simpsub['slay'] = "kill"
simpsub['slew'] = "killed"
simpsub['smite'] = "strike"
simpsub['smitest'] = "strike"
simpsub['smiting'] = "striking"
simpsub['smitten'] = "struck"
simpsub['smote'] = "struck"
simpsub['sooth'] = "truth"
simpsub['spake'] = "spoke"
simpsub['stinting'] = "lack"
simpsub['succour'] = "help"
simpsub['suspecting'] = "suspicious"
simpsub['tarried'] = "waited"
simpsub['tarry'] = "wait"
simpsub['thine'] = "your"
simpsub['Thrice'] = "Three times"
simpsub['thrice'] = "three times"
simpsub['twain'] = "two"
simpsub['unto'] = "to"
simpsub['uprose'] = "rose up"
simpsub['Verily'] = "Truly"
simpsub['verily'] = "truly"
simpsub['vouchsafe'] = "promise"
simpsub['vouchsafed'] = "promised"
simpsub['vouchsafes'] = "promises"
simpsub['ware'] = "aware"
simpsub['wast'] = "were"
simpsub['waxed'] = "became"
simpsub['ween'] = "believe"
simpsub['whatsoe\'er'] = "whatever"
simpsub['whenso'] = "whenever"
simpsub['Wherefore'] = "For which reason"
simpsub['wherefore'] = "for which reason"
simpsub['Wherefrom'] = "From which"
simpsub['wherefrom'] = "from which"
simpsub['Wherewith'] = "with which"
simpsub['wherein'] = "in which"
simpsub['Wherein'] = "In which"
simpsub['whereon'] = "on which"
simpsub['Whereon'] = "On which"
simpsub['Whither'] = "Where"
simpsub['whither'] = "where"
simpsub['whomsoever'] = "whoever"
simpsub['wilt'] = "will"
simpsub['wont'] = "accustomed"
simpsub['wroth'] = "angry"
simpsub['Ye'] = "You"
simpsub['ye'] = "you"

ngramsub = {}
ngramsub["for that"] = "for"
ngramsub["from out"] = "out of"
ngramsub["from out of"] = "out of"
ngramsub["gave ear"] = "listened"
ngramsub["give ear"] = "listen"
ngramsub["holden of"] = "held by"
ngramsub["like unto"] = "like"
ngramsub["make essay"] = "attempt"
ngramsub["make prayer"] = "pray"
ngramsub["mine own"] = "my own"
ngramsub["no wise"] = "no way"
ngramsub["of a surety"] = "surely"
ngramsub["is fain"] = "wants"
ngramsub["sate him"] = "sat"
ngramsub["was fain"] = "wanted"
ngramsub["this wise"] = "this way"

compsub = {}
compsub['abode'] = 'a'
compsub['baneful'] = 'a'
compsub['bethink'] = 'a'
compsub['dread'] = 'a'
compsub['demesne'] = 'τέμενος' #separate land, of gods and of kinds
compsub['essay'] = 'a'
compsub['forsooth'] = 'a'
compsub['Forthwith'] = 'a'
compsub['forthwith'] = 'a'
compsub['hie'] = 'a'
compsub['laden'] = 'a'
compsub['Lo'] = 'a'
compsub['lo'] = 'a'
compsub['meed'] = 'a'
compsub['Nay'] = 'a'
compsub['nay'] = 'a'
compsub['pratest'] = 'a'
compsub['sate'] = 'a'
compsub['sore'] = 'a'
compsub['Thereat'] = 'a'
compsub['thereat'] = 'a'
compsub['thereof'] = 'a'
compsub['Thereto'] = 'a'
compsub['thereto'] = 'a'
compsub['therewithal'] = 'a'
compsub['whereof'] = 'a'
compsub['withal'] = 'a'
compsub['wonderous'] = 'a'
compsub['wonderously'] = 'a'
compsub['wrought'] = 'a'
compsub['Yea'] = 'a'
compsub['yea'] = 'a'
compsub['yon'] = 'a'
compsub['yonder'] = 'a'

f = open("eth-3rd-pers.txt","r")
for l in f:
  l = re.sub(":[^\t]+","",l)
  args = l.split('\t')
  ethtable[args[0]] = args[1]
  #print(args[0],ethtable[args[0]])
f.close()

f = open("est-2nd-pers.txt","r")
for l in f:
  l = re.sub(":[^\t]+","",l)
  args = l.split('\t')
  ethtable[args[0]] = args[1]
  #print(args[0],ethtable[args[0]])
f.close()

def do_eth(s):
   t = re.sub("<[^>]+>"," ",s)
   t = re.sub('[\.,;:"!,\s\?]+'," ",t)
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
       s = re.sub('\\b' + a + "\\b",'<mod n="' + a + ':simpsub">' +  simpsub[a] + "</mod>",s)
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
     for a in ngramsub:
       w = re.sub("\\b" + a + "\\b","<corr n=\"" + a + "\">" + ngramsub[a]+'</corr>',w)
     w = re.sub("goodly\\s+([A-Z])","<mod n=\"goodly\">brilliant</mod> \g<1>",w)
     w = re.sub("was\\s+(abated)","<mod n=\"was\">had</mod> \g<1>",w)
    w = do_eth(w)
    w = re.sub('<mod n="thou:simpsub">you</mod>[\s]+art\\b',"<corr n=\"thou art\">you are</corr>",w)
    w = re.sub('\\bart[\s]+<mod n="thou:simpsub">you</mod>',"<corr n=\"art thou\">are you</corr>",w)

    print(w,end='')
     
