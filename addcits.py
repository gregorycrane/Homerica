#!/usr/bin/env python3
  
import sys
import re

from lxml import etree
from greek_accentuation.characters import *
from greek_accentuation.syllabify import *
from greek_accentuation.accentuation import *

lexfile = "cunliffe.lexentries.unicode.xml"
with open(lexfile) as f:
  for line in f:
    line = re.sub(r'n="(Il|Od)','n="Hom. \g<1>',line)
    m = re.search(r'<bibl>([α-ωΑ-Ω][ ]+[0-9]+)<\/bibl>',line)
    if( m ):
     #print("string",m.group(1))
     #print("startline",line)
     line = re.sub('<bibl>Β[ ]+([0-9]+)','<bibl n="Hom. Il. 2.\g<1>">Hom. Il. 2.\g<1>',line)
     line = re.sub('<bibl>Δ[ ]+([0-9]+)','<bibl n="Hom. Il. 4.\g<1>">Hom. Il. 4.\g<1>',line)
     line = re.sub('<bibl>Ε[ ]+([0-9]+)','<bibl n="Hom. Il. 5.\g<1>">Hom. Il. 5.\g<1>',line)
     line = re.sub('<bibl>Ζ[ ]+([0-9]+)','<bibl n="Hom. Il. 6.\g<1>">Hom. Il. 6.\g<1>',line)
     line = re.sub('<bibl>Η[ ]+([0-9]+)','<bibl n="Hom. Il. 7.\g<1>">Hom. Il. 7.\g<1>',line)
     line = re.sub('<bibl>Θ[ ]+([0-9]+)','<bibl n="Hom. Il. 8.\g<1>">Hom. Il. 8.\g<1>',line)
     line = re.sub('<bibl>Ι[ ]+([0-9]+)','<bibl n="Hom. Il. 9.\g<1>">Hom. Il. 9.\g<1>',line)
     line = re.sub('<bibl>Μ[ ]+([0-9]+)','<bibl n="Hom. Il. 12.\g<1>">Hom. Il. 12.\g<1>',line)
     line = re.sub('<bibl>Ν[ ]+([0-9]+)','<bibl n="Hom. Il. 13.\g<1>">Hom. Il. 13.\g<1>',line)
     line = re.sub('<bibl>Ξ[ ]+([0-9]+)','<bibl n="Hom. Il. 14.\g<1>">Hom. Il. 14.\g<1>',line)
     line = re.sub('<bibl>Π[ ]+([0-9]+)','<bibl n="Hom. Il. 16.\g<1>">Hom. Il. 16.\g<1>',line)
     line = re.sub('<bibl>Ρ[ ]+([0-9]+)','<bibl n="Hom. Il. 17.\g<1>">Hom. Il. 17.\g<1>',line)
     line = re.sub('<bibl>Τ[ ]+([0-9]+)','<bibl n="Hom. Il. 19.\g<1>">Hom. Il. 19.\g<1>',line)
     line = re.sub('<bibl>Φ[ ]+([0-9]+)','<bibl n="Hom. Il. 21.\g<1>">Hom. Il. 21.\g<1>',line)
     line = re.sub('<bibl>Χ[ ]+([0-9]+)','<bibl n="Hom. Il. 22.\g<1>">Hom. Il. 22.\g<1>',line)
     line = re.sub('<bibl>Ψ[ ]+([0-9]+)','<bibl n="Hom. Il. 23.\g<1>">Hom. Il. 23.\g<1>',line)

     line = re.sub('<bibl>γ[ ]+([0-9]+)','<bibl n="Hom. Od. 3.\g<1>">Hom. Od. 3.\g<1>',line)
     line = re.sub('<bibl>δ[ ]+([0-9]+)','<bibl n="Hom. Od. 4.\g<1>">Hom. Od. 4.\g<1>',line)
     line = re.sub('<bibl>ε[ ]+([0-9]+)','<bibl n="Hom. Od. 5.\g<1>">Hom. Od. 5.\g<1>',line)
     line = re.sub('<bibl>λ[ ]+([0-9]+)','<bibl n="Hom. Od. 11.\g<1>">Hom. Od. 11.\g<1>',line)
     line = re.sub('<bibl>ν[ ]+([0-9]+)','<bibl n="Hom. Od. 13.\g<1>">Hom. Od. 13.\g<1>',line)
     line = re.sub('<bibl>π[ ]+([0-9]+)','<bibl n="Hom. Od. 16.\g<1>">Hom. Od. 16.\g<1>',line)
     line = re.sub('<bibl>ρ[ ]+([0-9]+)','<bibl n="Hom. Od. 17.\g<1>">Hom. Od. 17.\g<1>',line)
     line = re.sub('<bibl>ω[ ]+([0-9]+)','<bibl n="Hom. Od. 24.\g<1>">Hom. Od. 24.\g<1>',line)
    if( re.search(r'<bibl>([α-ωΑ-Ω][ ]+[0-9]+)<\/bibl>',line)):
      sys.stderr.write("bibl\t"+line)
    while( re.search(r'(<bibl n="Hom.[ ]+[IO][dl]\.[ ]+[0-9]+\.)([^>]+>[^<]+<\/bibl>)[ ]*=[ ]*([0-9]+)',line)):
      line = re.sub( r'(<bibl n="Hom.[ ]+[IO][dl]\.[ ]+[0-9]+\.)([^>]+>[^<]+<\/bibl>)[ ]*=[ ]*([0-9]+)','\g<1>\g<2> =xx \g<1>\g<3>">\g<3></bibl>',line,1)
    if( re.search(r'<.bibl>[ ]*=[ ]*[0-9]+',line)):
       sys.stderr.write('missedequal\t'+line)
    while( re.search(r'(<bibl n="Hom. [IO][dl]\.[ ]+[0-9]+\.)([^>]+[^<]+<\/bibl>)[ ]*,[ ]+([0-9]+)',line)):
      line = re.sub( r'(<bibl n="Hom. [IO][dl]\.[ ]+[0-9]+\.)([^>]+[^<]+<\/bibl>)[ ]*,[ ]+([0-9]+)','\g<1>\g<2>,XX \g<1>\g<3>">\g<3></bibl>',line,1)
    if( re.search(r'<.bibl>,[ ]+[0-9]+',line)):
       sys.stderr.write('missedbib\t'+line)
    print(line,end='')
