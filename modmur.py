#!/usr/bin/python
  
import sys
import re

ethtable = {}
curlemma = ''
modwords = 0
basewords = 0

simpsub = {}
simpsub['raiment'] = "clothing"
simpsub['maiden'] = "young woman"
simpsub['maidens'] = "young women"
simpsub['abide'] = "remain"
simpsub['adread'] = "afraid"
simpsub['aforetime'] = "in the past"
simpsub['Albeit'] = "Although"
simpsub['albeit'] = "although"
simpsub['amid'] = "among"
simpsub['anigh'] = "near"
simpsub['anywise'] = "in any way"
simpsub['aright'] = "correctly"
simpsub['asunder'] = "apart"
simpsub['athrob'] = "throbbing"
simpsub['aught'] = "anything"
simpsub['bade'] = "commanded"
simpsub['badest'] = "commanded"
simpsub['bane'] = "harm"
simpsub['baneful'] = "harmful"
simpsub['bid'] = "command"
simpsub['bidden'] = "commanded"
simpsub['bids'] = "commands"
simpsub['brake'] = "broke"
simpsub['builded'] = "built"
simpsub['car'] = "chariot"
simpsub['chine'] = "back-meat"
simpsub['clove'] = "cut"
simpsub['cloven'] = "cut"
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
simpsub['foeman'] = "enemy"
simpsub['foemen'] = "enemies"
simpsub['folk'] = "people"
simpsub['fordone'] = "done in"
simpsub['froward'] = "willful"
simpsub['gainsay'] = "deny"
simpsub['gat'] = "got"
simpsub['hadst'] = "had"
simpsub['hapless'] = "unhappy"
simpsub['hath'] = "has"
simpsub['hast'] = "have"
simpsub['hasted'] = "hastened"
simpsub['hearken'] = "listen"
simpsub['hearkened'] = "listened"
simpsub['heretofore'] = "until now"
simpsub['Heretofore'] = "Until now"
simpsub['hither'] = "here" #NB: hither is more preccise.
simpsub['housewife'] = "woman in charge of the house" #housewife always corresponds to tamih -- i lose the one-word to one-word equivalence by chosing this phrase
simpsub['Howbeit'] = "However"
simpsub['howbeit'] = "however"
simpsub['kine'] = "cattle"
simpsub['quaff'] = "drink"
simpsub['quaffs'] = "drinks"
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
simpsub['meseems'] = "I think"
simpsub['methinks'] = "I think"
simpsub['naught'] = "nothing"
simpsub['nigh'] = "near"
simpsub['nowise'] = "in no way"
simpsub['perchance'] = "by chance"
simpsub['perforce'] = "of necessity"
simpsub['reck'] = "care"
simpsub['recks'] = "cares"
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
simpsub['somewhat'] = "something"
simpsub['sooth'] = "truth"
simpsub['spake'] = "spoke"
simpsub['stinting'] = "lack"
simpsub['stranger-folk'] = "strangers"
simpsub['succour'] = "help"
simpsub['surfeit'] = "all too much"
simpsub['suspecting'] = "suspicious"
simpsub['tarried'] = "waited"
simpsub['tarry'] = "wait"
simpsub['thine'] = "your"
simpsub['thither'] = "there" #thither is more precise
simpsub['Thrice'] = "Three times"
simpsub['thrice'] = "three times"
simpsub['travailing'] = "laboring"
simpsub['Troy-land'] = "Troy"
simpsub['twain'] = "two"
simpsub['ungentle'] = "harsh"
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
simpsub['waxes'] = "grows"
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
simpsub['whosoever'] = "whoever"
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
bigrams['a foeman'] = "an enemy"
bigrams['am come'] = "have come"
bigrams['arrayed him'] = "arrayed himself"
bigrams['art come'] = "have come"
bigrams['in sunder'] = "apart"
bigrams['baser fellow'] = "lesser man"
bigrams['base fellow'] = "lesser man"
bigrams['bethought him'] = "thought"
bigrams['bethought them'] = "thought"
bigrams['bethought thee'] = "thought"
bigrams['clad him'] = "clad himself"
bigrams['did on'] = "put on"
bigrams['do thou'] = ""
bigrams['do ye'] = ""
bigrams['do you'] = "you"
bigrams['evil case'] = "bad situation"
bigrams['fear me'] = "fear"
bigrams['from without'] = "from outside"
bigrams['go thou'] = "go"
bigrams['his wont'] = "his habit"
bigrams['insatiate fellow'] = "insatiable man"
bigrams['is come'] = "has come"
bigrams['maid unwed'] = "unmarried girl"
bigrams['unwedded maid'] = "unmarried girl"
bigrams['made answer'] = "answered"
bigrams['other fellow'] = "other man"
bigrams['rouse thee'] = "rouse yourself"
bigrams['sat him'] = "sat himself"
bigrams['sit thou'] = "sit yourself"
bigrams['such wise'] = "such a way"
bigrams['this fellow'] = "this man"
bigrams['to surfeit'] = "to a bellyful"
bigrams['travail sore'] = "suffer badly"
bigrams['wax wroth'] = "become angry"
bigrams['what time'] = "when"
bigrams['young maiden'] = "young girl"
bigrams['cares not'] = 'does not care'
bigrams['concerns not'] = 'does not concern'
bigrams['lives not'] = 'does not live'
bigrams['perishes not'] = 'does not perish'
bigrams['bridles not'] = 'does not bridle'
bigrams['deigns not'] = 'does not deign'
bigrams['comes not'] = 'does not come'
bigrams['recks not'] = 'does not think'
bigrams['lives not'] = 'does not live'
bigrams['escapes not'] = 'does not escape'
bigrams['knows not'] = 'does not know'
bigrams['leaves not'] = 'does not leave'
bigrams['beseems not'] = 'it is not fitting'
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
bigrams["hard by"] = "nearby"
bigrams["holden of"] = "held by"
bigrams["is fain"] = "wants"
bigrams["like unto"] = "like"
bigrams["make essay"] = "attempt"
bigrams["make prayer"] = "pray"
bigrams["mine eyes"] = "my eyes"
bigrams["mine own"] = "my own"
bigrams["must needs"] = "must"
bigrams["near to"] = "near"
bigrams["no wise"] = "no way"
bigrams["sate him"] = "sat"
bigrams["was fain"] = "wanted"
bigrams["this wise"] = "this way"
bigrams["thou longest"] = "you long"
bigrams['didst promise'] = 'promised'
bigrams['didst leave'] = 'left'
bigrams['didst hear'] = 'heard'
bigrams['didst come'] = 'came'
bigrams['didst blind'] = 'blinded'
bigrams['didst take'] = 'took'
bigrams['didst slay'] = 'killed'
bigrams['didst send'] = 'sent'
bigrams['didst name'] = 'named'
bigrams['didst lie'] = 'lied'
bigrams['didst lay'] = 'lay'
bigrams['didst bid'] = 'commanded'
bigrams['didst bear'] = 'bore'
bigrams['didst yield'] = 'yielded'
bigrams['didst wish'] = ' wished'
bigrams['didst win'] = 'won'
bigrams['didst watch'] = ' watched'
bigrams['didst wander'] = ' wandered'
bigrams['didst vanquish'] = 'vanquished'
bigrams['didst speak'] = 'spoke'
bigrams['didst sit'] = 'sat'
bigrams['didst set'] = 'set'
bigrams['didst save'] = 'saved'
bigrams['didst sail'] = ' sailed'
bigrams['didst rouse'] = 'roused'
bigrams['didst rend'] = 'rent'
bigrams['didst rear'] = ' reared'
bigrams['didst reach'] = ' reached'
bigrams['didst rage'] = 'raged'
bigrams['didst pray'] = ' prayed'
bigrams['didst moor'] = ' moored'
bigrams['didst make'] = 'made'
bigrams['didst long'] = ' longed'
bigrams['didst lead'] = 'led'
bigrams['didst honour'] = ' honoured'
bigrams['didst honor'] = ' honored'
bigrams['didst herd'] = ' herded'
bigrams['didst hearken'] = ' hearkened'
bigrams['didst hang'] = 'hung'
bigrams['didst guard'] = ' guarded'
bigrams['didst grasp'] = ' grasped'
bigrams['didst follow'] = ' followed'
bigrams['didst entertain'] = 'entertained'
bigrams['didst endure'] = 'endured'
bigrams['didst devise'] = 'devised'
bigrams['didst cheer'] = ' cheered'
bigrams['didst call'] = ' called'
bigrams['didst bring'] = 'brought'
bigrams['didst boast'] = ' boasted'
bigrams['didst beguile'] = 'beguiled'
compsub = {}
compsub['abode'] = 'a'
compsub['aye'] = 'a'
compsub['baneful'] = 'a'
compsub['bethink'] = 'a'
compsub['dread'] = 'a'
compsub['demesne'] = 'τέμενος' #separate land, of gods and of kinds
compsub['essay'] = 'a'
compsub['fellow'] = 'a'
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


def do_counts(s):
  global modwords
  global basewords
  works = s
  while(re.search('<mod',works)):
    modwords = modwords + 1
    works = re.sub('<mod[^>]+>',' ',works,1)
  works = s
  works = re.sub('<[^>]+>',' ',works)
  while(re.search('[A-Za-z\']+',works)):
    basewords = basewords + 1
    works = re.sub('[A-Za-z\']+',' ',works,1)

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

V_s_excepts = {}
V_s_excepts['is not'] = 1
V_s_excepts['does not'] = 1
V_s_excepts['was not'] = 1
V_s_excepts['has not'] = 1
V_s_excepts['as not'] = 1
V_s_excepts['us not'] = 1
def V_not(s):

  works = s
  while( re.search('\\b([a-z]+s[ ]not)\\b',works)):
   m = re.search('\\b([a-z]+s[ ]not)\\b',works)
   if( m and not m[1] in V_s_excepts):
    sys.stderr.write(m[1]+'\n')
   works = re.sub('\\b([a-z]+s[ ]not)\\b',' ',works,1)
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
   t = re.sub('[—\'\.,;:"!,\s\?]+'," ",t)
   t = re.sub('<mod[^>]+>[^<]+<\/mod>',' ',t)
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
trigrams['am I come'] = 'have I come'
trigrams['day by day'] = 'each and every day'
trigrams['do thou thus'] = 'do as follows'
trigrams['fear me lest'] = 'fear lest'
trigrams['in evil case'] = 'in great stress'
trigrams['in despite of'] = 'in spite of'
trigrams['on the morrow'] = 'tomorrow'
trigrams['of good cheer'] = 'confident'
trigrams["of a surety"] = "surely"
trigrams["of a truth"] = "truly"
trigrams["out on it"] = "curse it"
trigrams["put on him"] = "put on"
trigrams["thou ever longest"] = "you always long"
trigrams["without the courtyard"] = "outside the courtyard"

def do_bigrams(s):
   works = s
   works = re.sub('<mod[^>]+>[^<]+<\/mod>',' ',works)
   works = re.sub('<[^>]+>', ' ' ,works)

   for foo in trigrams:
     if( re.search('\\b' + foo + '\\b',works)):
       s = re.sub('\\b' + foo + '\\b','<mod n="trigram:' + foo.upper() + '">' + trigrams[foo] + '</mod>',s)
       works = re.sub('\\b' + foo + '\\b',' ',works)
     if( re.search('\\b' + foo.capitalize() + '\\b',works)):
       s = re.sub('\\b' + foo.capitalize() + '\\b','<mod n="' + foo + '">' + trigrams[foo].capitalize() + '</mod>',s)
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
     w = re.sub("goodly\\s+([A-Z])","<mod n=\"goodly\">brilliant</mod> \g<1>",w)
     w = re.sub("goodly\\s+([a-z])","<mod n=\"goodly\">brilliant</mod> \g<1>",w)
     w = do_bigrams(w)
     w = V_not(w)
     w = re.sub("<s\\b","\n\n<s",w)
     w = re.sub("^[ \t]+","",w)
     w = re.sub("\\be'en\\b","even",w) # I hate this form and I am not even leving a race of it.
     #for a in ngramsub:
       #w = re.sub("\\b" + a + "\\b","<corr n=\"" + a + "\">" + ngramsub[a]+'</corr>',w)
     w = re.sub("was\\s+(abated)","<mod n=\"was\">had</mod> \g<1>",w)
    w = do_eth(w)
    w = re.sub('<mod n="thou:simpsub">you</mod>[\s]+art\\b',"<corr n=\"thou art\">you are</corr>",w)
    w = re.sub('\\bart[\s]+<mod n="thou:simpsub">you</mod>',"<corr n=\"art thou\">are you</corr>",w)

    workw = w
    while( re.search('gram:([A-Z][A-Z][^"]+)',workw)):
      m = re.search('gram:([A-Z][A-Z][^"]+)',workw)
      v1 = m[1]
      v2 = m[1].lower()
      w = re.sub('gram:' + v1 ,'gram:' + v2,w,1)
      workw  = re.sub('gram:[A-Z][A-Z][^"]+',' ',workw,1)
    do_counts(w)
    print(w,end='')
     
sys.stderr.write(str(basewords) + '\t' + str(modwords) + '\n')
