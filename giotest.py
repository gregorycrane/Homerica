import torch, os, re, csv
from transformers import AutoModel, XLMRobertaForMaskedLM, XLMRobertaModel, XLMRobertaTokenizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

model = XLMRobertaModel.from_pretrained('UGARIT/grc-alignment',output_hidden_states = True)

tokenizer=XLMRobertaTokenizer.from_pretrained('xlm-roberta-base')

#input_text_eng ="I am to speak against persons who pride themselves on their eloquence; so, to begin with a text of Scripture"
input_text_eng = "I am to speak against persons who pride themselves on their eloquence; so, to begin with a text of Scripture, “Behold, I am against thee, O thou proud one,” not only in thy system of teaching, but also in thy hearing, and in thy tone of mind. For there are certain persons who have not only their ears and their tongues, but even, as I now perceive, their hands too, itching for our words; who delight in profane babblings, and oppositions of science falsely so called, and strifes about words, which tend to no profit; for so Paul, the Preacher and Establisher of the “Word cut short,” the disciple and teacher of the Fishermen, calls all that is excessive or superfluous in discourse. But as to those to whom we refer, would that they, whose tongue is so voluble and clever in applying itself to noble and approved language, would likewise pay some attention to actions. For then perhaps in a little while they would become less sophistical, and less absurd and strange acrobats of words, if I may use a ridiculous expression about a ridiculous subject. "

input_text_eng = "Rouse yourself, good son of Capaneus; get you down from the chariot, that you may draw forth from my shoulder the bitter arrow."

clean_sent_eng=re.sub(r'[^\w\s]', '', input_text_eng)

#input_text_grc = "Πρὸς τοὺς ἐν λόγῳ κομψοὺς ὁ λόγος. καὶ ἵνα ἀπὸ τῆς γραφῆς ἄρξωμαι"
input_text_grc = "Πρὸς τοὺς ἐν λόγῳ κομψοὺς ὁ λόγος. καὶ ἵνα ἀπὸ τῆς γραφῆς ἄρξωμαι· Ἴδου ἐγὼ ἐπὶ σὲ τὴν ὑβρίστριαν. εἰσὶ γάρ, εἰσί τινες, οἱ τὴν ἀκοὴν προσκνώμενοι καὶ τὴν γλῶσσαν, ἤδη δέ, ὡς ὁρῶ, καὶ τὴν χεῖρα, τοῖς ἡμετέροις λόγοις, καὶ χαίροντες ταῖς βεβήλοις κενοφωνίαις, καὶ ἀντιθέσεσι τῆς ψευδωνύμου γνώσεως, καὶ ταῖς εἰς οὐδὲν χρήσιμον φερούσαις λογομαχίαις. οὕτω γὰρ ὁ Παῦλος καλεῖ πᾶν τὸ ἐν λόγῳ περιττὸν καὶ περίεργον, ὁ τοῦ συντετμημένου λόγου κῆρυξ καὶ βεβαιωτής, ὁ τῶν ἁλιέων μαθητὴς καὶ διδάσκαλος. οὗτοι δέ, περὶ ὧν ὁ λόγος, εἴθε μέν, ὥσπερ τὴν γλῶσσαν εὔστροφον ἔχουσι καὶ δεινὴν ἐπιθέσθαι λόγοις εὐγενεστέροις τε καὶ δοκιμωτέροις, οὕτω τι καὶ περὶ τὰς πράξεις ἠσχολοῦντο μικρὸν γοῦν, καὶ ἴσως ἧττον ἂν ἦσαν σοφισταὶ καὶ κυβισταὶ λόγων ἄτοποι καὶ παράδοξοι, ἵν εἴπω τι καὶ γελοίως περὶ γελοίου πράγματος."
input_text_grc = "ὄρσο πέπον Καπανηϊάδη , καταβήσεο δίφρου , ὄφρά μοι ἐξ ὤμοιο ἐρύσσῃς πικρὸν ὀϊστόν"
clean_sent_grc = re.sub(r'[^\w\s]', '', input_text_grc)

eng_input = tokenizer(clean_sent_eng, return_tensors='pt')
grc_input = tokenizer(clean_sent_grc, return_tensors='pt')

model.eval()
with torch.no_grad():
    outputs = model(**eng_input)
    hidden_states = outputs.hidden_states

layer_eight_embedding=hidden_states[8]

with torch.no_grad():
    outputs = model(**grc_input)
    hidden_states = outputs.hidden_states

layer_eight_embedding1=hidden_states[8]

#Return index of closest token in sentence 2
def find_close(input_array, embedding):
  max=0
  index=0
  for k in range(embedding.shape[1]):
    vector1 =input_array
    vector2=embedding[0][k].numpy()
    cos=cosine_similarity([vector1],[vector2])
    if cos>max:
      max=cos
      index=k
  return index

eng_list=[]
grc_list=[]
for i in range(1,layer_eight_embedding.shape[1]-1,1):
  max_index_2=find_close(layer_eight_embedding[0][i].numpy(), layer_eight_embedding1)
  max_index_1=find_close(layer_eight_embedding1[0][max_index_2].numpy(), layer_eight_embedding)
  if max_index_1 == i:
    eng_list.append(i)
    #print(eng_list)
    grc_list.append(max_index_2)

def find_word_pos(token_pos_list,aligned_token):
  word_pos=[]
  for tk in aligned_token:
    tk_idx=tk-1
    for i in range(len(token_pos_list)-1):
      if tk_idx >= token_pos_list[i] and tk_idx < token_pos_list[i+1]:
        word_pos.append(token_pos_list.index(token_pos_list[i]))
  return word_pos

tokens_sent1_pos=[i for i, string in enumerate(tokenizer.tokenize(clean_sent_eng)) if "▁" in string]
tokens_sent1_pos.append(500)

words_sent1_pos=find_word_pos(tokens_sent1_pos,eng_list)
aligned_words_sent1=[clean_sent_eng.split()[i] for i in words_sent1_pos]

tokens_sent2_pos=[i for i, string in enumerate(tokenizer.tokenize(clean_sent_grc)) if "▁" in string]
tokens_sent2_pos.append(500)

words_sent2_pos=find_word_pos(tokens_sent2_pos,grc_list)
aligned_words_sent2=[clean_sent_grc.split()[i] for i in words_sent2_pos]


#Code here may need to be modified to preserve order
alignment_dict={}
for i in range(len(aligned_words_sent1)):
  alignment_dict[aligned_words_sent1[i]]=aligned_words_sent2[i]

print(alignment_dict)
