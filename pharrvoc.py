#!/usr/bin/env python3
  
import sys
import re
import operator

cunids = {}
cunlemmas = {}

lexfile = "cunliffe.lexentries.unicode.xml"
with open(lexfile) as f:
  for line in f:
    line = re.sub('†','',line)
    m = re.search('id="([^"]+(lex|suffix|prefix))"',line)
    if( m):
     curid = m.group(1)
     curlemma = ''
     m = re.search('n="([^"]+)"',line)
     if(m ):
      curlemma = m.group(1)
      cunids[curid] = curlemma
      cunlemmas[curlemma] = curid


lexfile = "cunliffe.hompers.unicode.xml"
with open(lexfile) as f:
  for line in f:
    m = re.search('id="([^"]+name)"',line)
    if( m):
     curid = m.group(1)
     curlemma = ''
     m = re.search('n="([^"]+)"',line)
     if(m ):
      curlemma = m.group(1)
      cunids[curid] = curlemma
      cunlemmas[curlemma] = curid

pharr2stand = {}
pharr2stand['αὖτις'] = 'αὖθις'
pharr2stand['Πηληιάδης'] = 'Πηλείδης'
pharr2stand['Ἀχαιοί'] = 'Ἀχαιός'
pharr2stand['μυρίοι'] = 'μυρίος'
pharr2stand['νοῦσος'] = 'νόσος'
pharr2stand['ἀ-'] = 'ἀ-1'
pharr2stand['Δαναός'] = 'Δαναοί'
pharr2stand['διΐφιλος'] = 'διίφιλος'
pharr2stand['Ἀτρεΐδης'] = 'Ἀτρείδης'
pharr2stand['*κλεύω'] = 'ἔκλυον'
pharr2stand['κλεύω'] = 'ἔκλυον'
pharr2stand['μετέειπον'] = 'μετεῖπον'
pharr2stand['προσέειπον'] = 'προσεῖπον'
pharr2stand['Ἄις'] = 'Ἅιδης'
pharr2stand['δαίς'] = 'δαίς1'
pharr2stand['πολλός'] = 'πολύς'
pharr2stand['τέ'] = 'τε'
pharr2stand['προϊάπτω'] = 'προιάπτω'
pharr2stand['ξuvίημι'] = 'σuvίημι'
pharr2stand['ἀπάνευθεν'] = 'ἀπάνευθε'
pharr2stand['ἠύκομος'] = 'εὔκομος'
pharr2stand['ἐέλδωρ'] = 'ἔλδωρ'
pharr2stand['νηός'] = 'ναός'
pharr2stand['νηός'] = 'ναός'
pharr2stand['εἴκω'] = 'εἴκω1'
pharr2stand['φαρέτρη'] = 'φαρέτρα'
pharr2stand['αἰεί'] = 'ἀεί'
pharr2stand['αὐτάρ'] = 'ἀτάρ'
pharr2stand['ἀγορή'] = 'ἀγορά'
pharr2stand['μηρίον'] = 'μηρία'
pharr2stand['ἢ'] = 'ἤ'
pharr2stand['κέν'] = 'ἄν'
pharr2stand['μίν'] = 'μιν'
pharr2stand['νύ'] = 'νῦν'
pharr2stand['οὐρεύς'] = 'ὀρεύς'
pharr2stand['Ἥρη'] = 'Ἥρα'
pharr2stand['γέ'] = 'γε'
pharr2stand['οἴω'] = 'οἴομαι'
pharr2stand['πτόλεμος'] = 'πόλεμος'
pharr2stand['τὶς'] = 'τις'
pharr2stand['αἰ'] = 'εἰ'
pharr2stand['ἀρήν'] = 'ἀρνός'
pharr2stand['εἴ τε'] = 'εἴτε'
pharr2stand['ἧ τοι'] = 'ἧτοι'
pharr2stand['κνίση'] = 'κνῖσα'
pharr2stand['πώς'] = 'πως'
pharr2stand['εἴδω'] = 'εἶδον'
pharr2stand['χέρης'] = 'χερείων'
pharr2stand['ἀπαμείβω'] = 'ἀπαμείβομαι'

curlesson = ''
lexfile = "pharr.homgramm.xml"
with open(lexfile) as f:
  for line in f:
    m = re.search(r'"lesson([0-9]+)"',line)
    if(m):
      curlesson = m.group(1)
    if( re.search(r'0[12]',curlesson)):
     continue
    m = re.search('<item[^>]*>(.+)[ ]+(<gloss>.+)</item>',line)
    if(m):
     greek = m.group(1)
     gloss = m.group(2)
     lemma = re.sub(r'<foreign[^>]+>([^<]+).+','\g<1>',greek)
     lemma = re.sub(r'[()\*]+','',lemma)
     lemma = re.sub(r'(.)[\-](.)','\g<1>\g<2>',lemma)
     lemma = re.sub('ῡ','υ',lemma)
     lemma = re.sub('ᾱ','α',lemma)
     lemma = re.sub('ῑ','ι',lemma)
     if(lemma in pharr2stand ):
      lemma = pharr2stand[lemma]
     if( not lemma in cunlemmas):
      print(curlesson,lemma)
     i = 0
    else:
      if(re.search('<item',line)):
       print("badline",line)
