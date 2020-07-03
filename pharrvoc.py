#!/usr/bin/env python3
  
import sys
import re
import operator

cunids = {}
cunlemmas = {}
pharrlemmas = {}
pharrlesson = {}
pharrvoc = {}
allvoc = {}

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

f.close()


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
pharr2stand['ξuvίημι'] = 'συνίημι'
pharr2stand['ἀπάνευθεν'] = 'ἀπάνευθε'
pharr2stand['ἠύκομος'] = 'εὔκομος'
pharr2stand['ἐέλδωρ'] = 'ἔλδωρ'
pharr2stand['νηός'] = 'ναός'
pharr2stand['νηῦς'] = 'ναῦς'
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
pharr2stand['ἧ τοι'] = 'ἦ'
pharr2stand['κνίση'] = 'κνῖσα'
pharr2stand['πώς'] = 'πως'
pharr2stand['εἴδω'] = 'εἶδον'
pharr2stand['χέρης'] = 'χείρων'
pharr2stand['χερείων'] = 'χείρων'
pharr2stand['ἀπαμείβω'] = 'ἀπαμείβομαι'
pharr2stand['ἤν'] = 'ἐάν'
pharr2stand['μετόπισθεν'] = 'μετόπισθε'
pharr2stand['προβούλομαι'] = 'προβέβουλα'
pharr2stand['σαόω'] = 'σώζω'
pharr2stand['ζώω'] = 'ζάω'
pharr2stand['ὅς τε'] = 'ὅστε'
pharr2stand['θεοπροπίη'] = 'θεοπροπία'
pharr2stand['κούρη'] = 'κόρη'
pharr2stand['τούνεκα'] = 'τοὔνεκα'
pharr2stand['πώ'] = 'πω'
pharr2stand['φιλοκτεανώτατος'] = 'φιλοκτέανος'
pharr2stand['ἐπείκω'] = 'ἐπέοικε'
pharr2stand['ποθί'] = 'ποθι'
pharr2stand['τετραπλῇ'] = 'τετραπλόος'
pharr2stand['τριπλῇ'] = 'τριπλόος'
pharr2stand['ἅλς'] = 'ἅλς2'
pharr2stand['δεύομαι'] = 'δεύω2'
pharr2stand['ἐρύω'] = 'ἐρύω1'
pharr2stand['ἱερόν'] = 'ἱερός'
pharr2stand['ἐλάω'] = 'ἐλαύνω'
pharr2stand['μαχέομαι'] = 'μάχομαι'
pharr2stand['οὖρος'] = 'ὄρος'
pharr2stand['Tpῶes'] = 'Τρώς'
pharr2stand['Φθίη'] = 'Φθία'
pharr2stand['ἶσος'] = 'ἴσος'
pharr2stand['μετατρέπω'] = 'μετατρέπομαι'
pharr2stand['Τροίη'] = 'Τροία'
pharr2stand['ἀναιδείη'] = 'ἀναίδεια'

curlesson = ''
lexfile = "pharr.homgramm.xml"
with open(lexfile) as f:
  for line in f:
    line = re.sub('\t','',line)
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
     pharrlemmas[lemma] = line 
     pharrlesson[lemma] = "pharr" + curlesson
     i = 0

f.close()

outf = open('pharrvoc.txt', 'w')
sawkeys = {}
lexfile = "tlg0012-tbankplus.txt"
with open(lexfile) as f:
  for line in f:
   fd = line.split('\t')
   if( fd[1] in sawkeys):
     continue
   sawkeys[fd[1]] = 1

   if( fd[3] in allvoc):
     allvoc[fd[3]] = allvoc[fd[3]] + 1
   else:
     allvoc[fd[3]] = 1

   if( fd[3] in pharrlesson):
     #print(pharrlesson[fd[3]],line,sep="\t",end='')
     outf.write(pharrlesson[fd[3]] + "\t" + line )
     if( fd[3] in pharrvoc):
      pharrvoc[fd[3]] = pharrvoc[fd[3]] + 1
     else:
      pharrvoc[fd[3]] = 1


for foo in dict(sorted(allvoc.items(), key=operator.itemgetter(1),reverse=True)):
   if( foo in pharrvoc):
#     print(pharrvoc[foo],foo,pharrlesson[foo],"pharrvoc",sep="\t")
     outf.write(str(pharrvoc[foo]) + "\t" + foo + "\t" + pharrlesson[foo] + "\t" + "pharrvoc\n")
   else:
     #print(allvoc[foo],foo,"newvoc",sep="\t")
     outf.write(str(allvoc[foo])+"\t"+foo+"\t"+"newvoc\n")

f.close()
