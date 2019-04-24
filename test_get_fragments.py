from estnltk import Text
from estnltk.syntax.scoring import las_score
from estnltk.converters.conll_importer import conll_to_text, add_layer_from_conll

from get_fragments import get_fragments

test_sentences_gold = "test_sentences/gold_test_sentences.conll"
test_sentneces_malt = "test_sentences/malt_test_sentences.conll"

malt_phrases = []
gold_prases = []

text2 = conll_to_text(file=test_sentences_gold, syntax_layer='gold')
add_layer_from_conll(file=test_sentneces_malt, text=text2, syntax_layer='parsed')

def test_get_fragments(text2):
    gold_spans = text2.gold.span_list
    parsed_spans = text2.parsed.span_list

    fragments = get_fragments(text2)

    #esimesed kaks lauset malt on leidnud ÖT õigesti, tahan testida, et sellises olukorras
    #tagastatakse see malti leitud fragment formaadis ehk get_fragments väljund
    #[w2, malt_subj, malt_subj2, malt_prd, subj_true, prd_true, gold_direction] peab olema
    #[verb, subjekt, None, predikatiiv, True, True, True/False]
    for sentence in text2.sentences[:2]:
        subj_on_prd_vs_subj_on_prd(fragments, gold_spans, parsed_spans, sentence)

def subj_on_prd_vs_subj_on_prd(fragments, gold_spans, parsed_spans, sentence):
    for word in sentence:
        #what do I do here
        break
