import giotest2
from giotest2 import compsents
import re
import sys
input_text_grc = "βέβληται γὰρ ἄριστος Ἀχαιῶν , οὐ δέ ἕ φημι δήθ' ἀνσχήσεσθαι κρατερὸν βέλος , εἰ ἐτεόν με ὦρσεν ἄναξ Διὸς υἱὸς ἀπορνύμενον Λυκίηθεν ."

input_text_eng = "Struck is the best man of the Achaeans, and I think he will not for long endure the mighty shaft, if in very truth the king, the son of Zeus, sped me on my way when I set forth from Lycia."

    
def do_sent(l):
        args = l.split('\t')
        print(args[2],args[3])
        
        curid = args[0]
        curcit = args[1]
        input_text_eng = args[2]
        input_text_grc = args[3]
        # πράξεις·
        input_text_grc = re.sub('·','',input_text_grc)
        input_words_grc = re.sub('([,\.;]|·|·)',' ',input_text_grc).split()
        greekdict = {}
        for foo in input_words_grc:
             greekdict[foo] = 0
        output_text_eng = args[2]
        print(curid,curcit,end='\t')

        addapostr = {}

        rawgreek = re.sub('[,\.:;?!",]','',input_text_grc)
        for foo in rawgreek.split():
             #print('g',foo)
             if(re.search("'",foo)):
                  addapostr[re.sub("'",'',foo)] = foo
        print('apo',addapostr)
        sentalign = compsents(input_text_grc,input_text_eng)
        excepts = {}
        for foo in input_text_eng.split():
            foo = re.sub('[,\.:;?!",]','',foo)
            foo = re.sub('·','',foo)
            #print('word',foo)
            if(re.search('-',foo)):
                excepts[re.sub('-','',foo)] = foo
                #print('\n\nsetex',FileNotFoundError)
        for foo in sentalign:
            subpat = sentalign[foo]
            if(subpat in addapostr):
                 subpat = addapostr[subpat]
            if(not subpat in greekdict):
                 print('missing',subpat,greekdict)
                 continue
            greekdict[subpat] = greekdict[subpat] + 1
            if(foo in excepts):
                print('\n\nexcept',excepts[foo])
                foo = excepts[foo]
            output_text_eng = re.sub('\\b'+foo+'\\b',foo+'['+subpat+']',output_text_eng)
        output_text_eng = re.sub('\\b(a|an|the|The|A|An|his|her|their|my)\\b ','\g<1>[0] ',output_text_eng)
        #print('\n\n',sentalign,'\n\n',output_text_eng+'\n')

        missedgreek = {}
        for foo in greekdict:
             if(foo == '·'):
                  continue
             if(greekdict[foo]!=1):
                  missedgreek[foo] = greekdict[foo]
        return(output_text_eng,missedgreek,input_text_grc)

def do_work(wkid):
    fname = 'github/Homerica/'+wkid + '-sentalign.tsv'
    f = open(fname)
    outfname = re.sub('sentalign','sentalign2',fname)
    outf = open(outfname,'w')
    for l in f:
        aligneds = do_sent(l)
        continue
    f.close()

for l in sys.stdin:
    if(len(l.split('\t'))<4):
         continue
    outs,missedg,gks = do_sent(l)
    print()
    print(gks)
    print(outs)
    print(missedg)
    #print


#do_work('tlg0012.tlg001')
