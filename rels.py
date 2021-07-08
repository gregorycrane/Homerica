#!/usr/bin/env python3

import re

from lxml import etree


filename = "tlg0012.tlg001.perseus-grc1.tb.xml"
prefix = "Il"

filename = "tlg0012.tlg002.perseus-grc1.tb.xml"
prefix = "Od"


formlist = {}
headlist = {}
haslemma = {}
hasrelation = {}
hascite = {}
hasform = {}
haspostag = {}

prev_ref = None
with open(filename) as f:
    tree = etree.parse(f)
    for sentence in tree.xpath("//sentence"):
        sentence_id = sentence.attrib["id"]
        subdoc = sentence.attrib["subdoc"]
        for word in sentence.xpath("word"):
            if "cite" in word.attrib:
                word_id = word.attrib["id"]
                form = word.attrib["form"]
                lemma = word.attrib["lemma"]
                postag = word.attrib["postag"]
                head = word.attrib["head"]
                relation = word.attrib["relation"]
                cite = word.attrib["cite"]
                ref = cite.split(":")[-1]
                if ref:
                    fullid = sentence_id + ":"  + word_id
                    headid = sentence_id + ":"  + head
                    headlist[fullid] = headid
                    haslemma[fullid] = lemma
                    hasrelation[fullid] =relation
                    haspostag[fullid] =postag
                    hascite[fullid] =cite
                    hasform[fullid] =form

                #print(word.attrib["form"]," ","fullid:",fullid)
                    formlist[fullid] = word
                #print ("lemma:",formlist[fullid].attrib["lemma"])
                #if ref:
                    #if ref != prev_ref:
                    #    if prev_ref:
                        #    print()
                        #print(f"{prefix}.{ref}", end=" ")
                    #    prev_ref = ref
                    #print(lemma, end=" ")

for id in formlist:
     if(formlist[id].attrib["postag"] and id in headlist):
          #print("pos:",formlist[id].attrib["postag"])
          wdhead = headlist[id]
          if(re.search("_CO",hasrelation[id]) and wdhead in haslemma):
               if( headlist[wdhead] in haslemma):
                wdhead = headlist[wdhead]
#                print ("CO head",headlist[id],hasform[wdhead])

          if( wdhead in haslemma):
           print(haslemma[id], hasform[id],hasrelation[id],haspostag[id],haslemma[wdhead],hasform[wdhead],haspostag[wdhead],hascite[id]),hascite[id]
          #else:
           #print("no lemma for:",headlist[id])

     #print("id",id)
