import stanza
from stanza.utils.conll import CoNLL

processor_dict = {
    'tokenize': 'perseus',
    'tokenize': 'perseus',
    'mwt': 'perseus',
    'pos': 'perseus',
    'lemma': 'perseus',
    'depparse': 'perseus'
}

stanza.download('grc', processors=processor_dict, package='perseus')
nlp_grc = stanza.Pipeline('grc', processors=processor_dict, package='perseus')

il = nlp_grc('μήνιν')

il

gr = nlp_grc(' τί ἦν κλαγγὴ δεινὴ ἐv Χρύσῃ καλῇ ;') 
gr = nlp_grc(' ἢν δέ που μορίῳ τινὶ προσμείξωσι, κρατήσαντές τέ τινας ἡμῶν πάντας αὐχοῦσιν ἀπεῶσθαι καὶ νικηθέντες ὑφ᾽ ἁπάντων ἡσσῆσθαι.') 

gr = nlp_grc(' Ἡροδότου Ἁλικαρνησσέος ἱστορίης ἀπόδεξις ἥδε, ὡς μήτε τὰ γενόμενα ἐξ ἀνθρώπων τῷ χρόνῳ ἐξίτηλα γένηται, μήτε ἔργα μεγάλα τε καὶ θωμαστά, τὰ μὲν Ἕλλησι τὰ δὲ βαρβάροισι ἀποδεχθέντα') 
print(gr)
gr = nlp_grc('οὔκουν χρή, εἴ τῳ καὶ δοκοῦμεν πλήθει ἐπιέναι καὶ ἀσφάλεια πολλὴ εἶναι μὴ ἂν ἐλθεῖν τοὺς ἐναντίους ἡμῖν διὰ μάχης, τούτων ἕνεκα ἀμελέστερόν τι παρεσκευασμένους χωρεῖν, ἀλλὰ καὶ πόλεως ἑκάστης ἡγεμόνα καὶ στρατιώτην τὸ καθ᾽ αὑτὸν αἰεὶ προσδέχεσθαι ἐς κίνδυνόν τινα ἥξειν.') 


print(gr)
gr
print(type(gr))
foo = gr.to_dict()
print(type(foo[0]))
for a in foo[0]:
  print(a)
