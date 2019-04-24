from estnltk import Text
from estnltk.syntax.scoring import las_score
from estnltk.converters.conll_importer import conll_to_text, add_layer_from_conll

def get_fragments(text2):
    fragments2 = []
    for w2 in text2.parsed:
        malt_subj = None
        malt_subj2 = None
        malt_prd = None

        prd_true = False
        subj_true = False

        gold_direction = None

        fragment = None
        #leia potentsiaalsed öeldistäite fraasid maltparseri kihist
        if w2.lemma in ['ole', 'paist', 'tundu', 'näi']:
            children = w2.children
            for child in children:
                if child.deprel == '@SUBJ':
                    if(not malt_subj):
                        malt_subj = child
                    else:
                        malt_subj2 = child
                elif child.deprel == '@PRD' and child.xpostag != 'A':
                    malt_prd = child

            #vaata siin ainult fraase mis sisaldavad @PRD ja @SUBJ
            if malt_subj and malt_prd:

                #ei huvita teine subjekt kui leidub @PRD
                malt_subj2 = None

                #kui @PRD või @SUBJ vanem pole kuldmärgenduse vanemaga vastavuses, siis ei ole ÖTF
                if (malt_subj.head != text2.gold.span_list.get(malt_subj).head or
                malt_prd.head != text2.gold.span_list.get(malt_prd).head):

                        if(malt_subj.head == text2.gold.span_list.get(malt_subj).head and subj_gold_value.deprel == "@SUBJ"):
                            subj_true = True
                        if(malt_prd.head == text2.gold.span_list.get(malt_prd).head and prd_gold_value.deprel == "@PRD"):
                            prd_true = True

                        assert subj_true == False or prd_true == False

                        fragment = [w2, malt_subj, malt_subj2, malt_prd, subj_true, prd_true, gold_direction]

                #vaatame kas kuldmärgenduses on ka @PRD ja @SUBJ samadel kohtadel või vastupidistel kohtadel
                else:
                    prd_gold_value = text2.gold.span_list.get(malt_prd)
                    subj_gold_value = text2.gold.span_list.get(malt_subj)

                    #samadel kohtadel
                    if(prd_gold_value.deprel == "@PRD" and subj_gold_value.deprel == "@SUBJ"):
                        gold_direction = subj_gold_value.start < prd_gold_value.start
                        prd_true, subj_true = True, True

                        fragment = [w2, malt_subj, malt_subj2, malt_prd, subj_true, prd_true, gold_direction]

                    #vastupidistel kohtadel
                    elif(prd_gold_value.deprel == "@SUBJ" and subj_gold_value.deprel == "@PRD"):
                        gold_direction = subj_gold_value.start < prd_gold_value.start
                        prd_true, subj_true = False, False

                        fragment = [w2, malt_subj, malt_subj2, malt_prd, subj_true, prd_true, gold_direction]

                    #vähemalt üks kahest on valesti märgitud (s.t @SUBJ või @PRD on puudu)
                    else:
                        subj_true = subj_gold_value.deprel == "@SUBJ"
                        prd_true = prd_gold_value.deprel == "@PRD"

                        assert subj_true != True or prd_true != True

                        fragment = [w2, malt_subj, malt_subj2, malt_prd, subj_true, prd_true, gold_direction]

            #juhul kui pole @SUBJ ja @PRD sisaldavat fraasi, vaatame, kas malt on leidnud @SUBJ ja @SUBJ fraasi,
            #mis goldis vastab öeldistäite fraasile
            elif malt_subj and malt_subj2:
                subj_gold_value = text2.gold.span_list.get(malt_subj)
                subj2_gold_value = text2.gold.span_list.get(malt_subj2)

                #ei huvita sõnad, millel goldis pole sama vanem
                if (malt_subj.head != subj_gold_value.head or
                    malt_subj2.head != subj2_gold_value.head):

                    continue

                if(subj_gold_value.deprel == "@PRD" and subj2_gold_value.deprel == "@SUBJ"):
                    subj_true = True
                    gold_direction = subj2_gold_value.start < subj_gold_value.start

                    fragment = [w2, malt_subj, malt_subj2, malt_prd, subj_true, prd_true, gold_direction]

                elif(subj_gold_value.deprel == "@SUBJ" and subj2_gold_value.deprel == "@PRD"):
                    subj_true = True
                    gold_direction = subj_gold_value.start < subj2_gold_value.start

                    fragment = [w2, malt_subj, malt_subj2, malt_prd, subj_true, prd_true, gold_direction]

        if fragment:
            fragments2.append(fragment)

    return fragments2
