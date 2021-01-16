#!/usr/bin/python
  
import sys
import re

ethtable = {}
curlemma = ''

simpsub = {}
simpsub['raiment'] = "clothing"
simpsub['maiden'] = "young woman"
simpsub['maidens'] = "young women"
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
simpsub['bane'] = "harm"
simpsub['baneful'] = "harmful"
simpsub['bid'] = "command"
simpsub['bids'] = "commands"
simpsub['brake'] = "broke"
simpsub['builded'] = "built"
simpsub['car'] = "chariot"
simpsub['chine'] = "back-meat"
simpsub['convoy'] = "passage"
simpsub['coursing'] = "racing"
simpsub['dainties'] = "fine foods"
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
simpsub['hearken'] = "listen"
simpsub['hearkened'] = "listened"
simpsub['heretofore'] = "until now"
simpsub['Heretofore'] = "Until now"
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
simpsub['leech'] = "doctor"
simpsub['loathly'] = "disgusting"
simpsub['meaner'] = "inferior"
simpsub['naught'] = "nothing"
simpsub['nigh'] = "near"
simpsub['nowise'] = "in no way"
simpsub['perchance'] = "by chance"
simpsub['perforce'] = "of necessity"
simpsub['reck'] = "care"
simpsub['rede'] = "counsel"
simpsub['saidst'] = "said"
simpsub['knave'] = "scoundrel"
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
simpsub['Troy-land'] = "Troy"
simpsub['twain'] = "two"
simpsub['unto'] = "to"
simpsub['uprose'] = "rose up"
simpsub['Verily'] = "Truly"
simpsub['verily'] = "truly"
simpsub['vex'] = "anger"
simpsub['vexed'] = "angered"
simpsub['vouchsafe'] = "promise"
simpsub['vouchsafed'] = "promised"
simpsub['vouchsafes'] = "promises"
simpsub['wallet'] = "leather sack"
simpsub['ware'] = "aware"
simpsub['wast'] = "were"
simpsub['waxed'] = "became"
simpsub['ween'] = "believe"
simpsub['whatsoe\'er'] = "whatever"
simpsub['whenso'] = "whenever"
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
simpsub['wooer'] = "suitor"
simpsub['wooers'] = "suitors"
simpsub['wont'] = "accustomed"
simpsub['would\'st'] = "accustomed"
simpsub['wroth'] = "angry"
simpsub['Ye'] = "You"
simpsub['ye'] = "you"

bigrams = {}
bigrams['bethought him'] = "thought"
bigrams['bethought them'] = "thought"
bigrams['bethought thee'] = "thought"
bigrams['wax wroth'] = "become angry"
bigrams['his wont'] = "his habit"
bigrams['made answer'] = "answered"
bigrams['such wise'] = "such a way"

ngramsub = {}
bigrams["a meaner"] = "an inferior"
bigrams["be not"] = "do not be"
bigrams["Be thou"] = "Be"
bigrams["for that"] = "for"
bigrams["from out"] = "out of"
bigrams["from out of"] = "out of"
bigrams["gave ear"] = "listened"
bigrams["give ear"] = "listen"
bigrams["good cheer"] = "good food"
bigrams["holden of"] = "held by"
bigrams["like unto"] = "like"
bigrams["make essay"] = "attempt"
bigrams["make prayer"] = "pray"
bigrams["mine own"] = "my own"
bigrams["no wise"] = "no way"
bigrams["is fain"] = "wants"
bigrams["sate him"] = "sat"
bigrams["was fain"] = "wanted"
bigrams["this wise"] = "this way"
bigrams["thou longest"] = "you long"

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
compsub['hence'] = 'a'
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
compsub['therein'] = 'a'
compsub['thereof'] = 'a'
compsub['Thereto'] = 'a'
compsub['thereto'] = 'a'
compsub['therewithal'] = 'a'
compsub['whence'] = 'a'
compsub['wherein'] = 'a'
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

V_excepts = {}
V_excepts["fled not"] = 'did not flee'
V_excepts["found not"] = 'did not find'

def V_not(s):
  for foo in V_excepts:
    if( re.search('\\b' + foo + '\\b',s)):
     s = re.sub('\\b' + foo + '\\b','<mod n="V_not:'+foo+'">'+V_excepts[foo]+"</mod>",s)
     return(s)
  works = s
  works = re.sub('<mod[^>]+>[^<]+',' ',works)
  while(re.search('\\b([a-z]+)ed[ ]+not\\b',works)):
     m = re.search('\\b([a-z]+)(ed)[ ]+not\\b',works)
     sval = m[1] + m[2] + '[ ]+not\\b'
     subv = '<mod n="V_not:' + foo + '">did not ' + m[1] + '</mod>'
     s = re.sub('\\b' + sval + '\\b',subv,s)
     works = re.sub('\\b' + sval + '\\b',' ',works)
  return(s)

def do_eth(s):
   t = re.sub("<[^>]+>"," ",s)
   t = re.sub('[\'\.,;:"!,\s\?]+'," ",t)
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
     elif(re.search('^[A-Z]',a) and a.lower() in compsub):
       s = re.sub('\\b' + a + "\\b","<sic>" + a + "</sic>",s)
     if(a in simpsub and a  not in checkedwords):
       s = re.sub('\\b' + a + "\\b",'<mod n="' + a + ':simpsub">' +  simpsub[a] + "</mod>",s)
     elif(re.search('^[A-Z]',a) and a.lower() in simpsub and a  not in checkedwords):
       sub = simpsub[a.lower()].capitalize()
       s = re.sub('\\b' + a + "\\b",'<mod n="' + a + ':simpsub">' +  sub + "</mod>",s)
     checkedwords[a] = 1

   return(s)

trigrams = {}
trigrams['day by day'] = 'each and every day'
trigrams['of good cheer'] = 'confident'
trigrams["of a surety"] = "surely"
trigrams["thou ever longest"] = "you always long"

def do_bigrams(s):
   works = s
   works = re.sub('<mod[^>]+>[^<]+<\/mod>',' ',works)
   works = re.sub('<[^>]+>', ' ' ,works)

   for foo in trigrams:
     if( re.search('\\b' + foo + '\\b',works)):
       s = re.sub('\\b' + foo + '\\b','<mod n="' + foo + '">' + trigrams[foo] + '</mod>',s)
       works = re.sub('\\b' + foo + '\\b',' ',works)
   
   while(re.search('\\b[A-Za-z]+[ ]+[a-z]+',works)):
      m = re.search('\\b([A-Za-z]+[ ]+[a-z]+)',works)
      if(m and m[1] in bigrams):
        s = re.sub('\\b' + m[1], '<mod n="bigram:'+m[1].upper()+'">'+bigrams[m[1]] + '</mod>',s)
      if(m and m[1].lower() in bigrams):
        subv =  bigrams[m[1].lower()]
        subv = subv.capitalize()
        s = re.sub('\\b' + m[1], '<mod n="bigram:'+m[1].upper()+'">'+subv + '</mod>',s)
      works = re.sub('\\b[A-Za-z]+[ ]+([a-z]+)',' \g<1>',works,1)
   return(s)

intext = 0
for w in sys.stdin.readlines():
    if( re.search("<text",w) ):
      intext = 1
    if( intext ):
     w = do_bigrams(w)
     w = V_not(w)
     w = re.sub("<s\\b","\n\n<s",w)
     w = re.sub("^[ \t]+","",w)
     w = re.sub("\\be'en\\b","even",w) # I hate this form and I am not even leving a race of it.
     #for a in ngramsub:
       #w = re.sub("\\b" + a + "\\b","<corr n=\"" + a + "\">" + ngramsub[a]+'</corr>',w)
     w = re.sub("goodly\\s+([A-Z])","<mod n=\"goodly\">brilliant</mod> \g<1>",w)
     w = re.sub("was\\s+(abated)","<mod n=\"was\">had</mod> \g<1>",w)
    w = do_eth(w)
    w = re.sub('<mod n="thou:simpsub">you</mod>[\s]+art\\b',"<corr n=\"thou art\">you are</corr>",w)
    w = re.sub('\\bart[\s]+<mod n="thou:simpsub">you</mod>',"<corr n=\"art thou\">are you</corr>",w)

    if( re.search('bigram:([A-Z][A-Z][^"]+)',w)):
      m = re.search('bigram:([A-Z][A-Z][^"]+)',w)
      v1 = m[1]
      v2 = m[1].lower()
      w = re.sub('bigram:' + v1 ,'bigram:' + v2,w)
    print(w,end='')
     
