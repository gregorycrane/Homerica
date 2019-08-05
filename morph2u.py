from cltk.corpus.greek.beta_to_unicode import Replacer
import re

r = Replacer()

fulls = ''
labels = ''
label = ''
workw = ''
lem = ''
raws = ''
postag = ''
stemtype = ''
keys = ''
prim = {}
f = open("homer-lmorph2.txt","r")
for l in f:
  print("starts",l)
  l = re.sub('\s+$','',l)
  l = re.sub('\\+/','/+',l) # o)i/+omai rather than o)i+/omai
  l = re.sub('\\+\\\\','\\+',l) # o)i/+omai rather than o)i+/omai
  l = re.sub('u\'','u’',l)
  fds = l.split("\t")
  fds[0] = re.sub("\s+$","",fds[0])
  if(not re.search(" ",fds[0]) and re.search("indeclform",l)):
    postag = fds[1]
    if(len(fds)>4):
     stemtype= fds[4]
  if(re.search(" ",fds[0])):
    prim = fds[0].split(" ")
    prim[1] = re.sub("w_","w",prim[1])
    prim[1] = re.sub("h_","h",prim[1])
    unis = r.beta_code(re.sub("_","&",prim[1]))
  else:
    prim[0] = fds[0]
  if(prim[0] == ":lem"):
       h = prim[0].split('-')
       if( len(h)>1):
          lem = r.beta_code(re.sub("_","&",h[0])) + '-' + r.beta_code(re.sub("_","&",h[1]))
       else:
          lem = r.beta_code(re.sub("_","&",prim[1]))
  if(prim[0] == ":raw" or prim[0] == ":workw"):
       keys = re.sub("^\s+","",keys)
       if(lem):
        print ("result",raws,workw,lem,fulls,labels,stemtype,postag,keys,sep="\t")
       fulls = ''
       labels = ''
       lem = ''
       postag = ''
       stemtype = ''
       keys = ''
  if(prim[0] == ":workw"):
         workw = r.beta_code(prim[1])
         workw = re.sub('ς\’','σ\’',raws)
  if(prim[0] == ":raw"):
         raws = r.beta_code(prim[1])
         raws = re.sub('ς\’','σ’',raws)
  if( prim[0] == ":end" and len(fds) > 1):
       postag = re.sub('^\s+','',fds[1])
       if(len(fds)>= 4):
        stemtype = fds[4]
        print("setstem",stemtype)

  if( prim[0] == ":end" ):
      if( re.search('indeclform',l)):
       stemtype = 'indecl'
      else:
       if(len(fds)> 4):
        stemtype = fds[4]
  if( prim[0] == ":stem" or prim[0] == ':lem' or prim[0] == ":aug1" or prim[0] == ":suff" or prim[0] == ":prvb"):
     unis = re.sub("ς$","σ",unis)
  if( prim[0] == ":stem" or prim[0] == ":aug1" or prim[0] == ":suff" or prim[0] == ":prvb" or prim[0] == ":end"):
     label = re.sub(":","",prim[0])
  if(len(fds)> 3):
    k = re.sub('^\s+','',fds[3])
    keys = keys + " " + k
  if( label and unis):
   print("fulls",fulls,"labels",labels,"label",label,"unis",unis)
   if( fulls):
    fulls = fulls + "-" +  unis
    labels = labels + "-" + label
   else:
     fulls = unis
     labels = label
   print("fulls",fulls,"labels",labels)
  unis = ''
  label = ''

