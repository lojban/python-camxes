from attest import Tests, assert_hook
import camxes


parse = Tests()

@parse.context
def parse_tree():
    yield camxes.parse("coi rodo mi cipra loka na cfila la camxes")

@parse.test
def ast(pt):
    assert pt.free[0].CMAVO[0].COI[0].word[0] == "coi"
    assert pt.sentence[0].bridiTail3[0].BRIVLA[0].gismu[0].word[0] == "cipra"

@parse.test
def index(pt):
    assert pt[0][0][0][0] == "coi"
    assert pt[1][1][0][0][0] == "cipra"

@parse.test
def leaf_names(pt):
    assert pt[0].name == 'free'
    assert pt[1].name == 'sentence'


grammar = Tests()

@grammar.test
def grammatical():
    assert camxes.isgrammatical("coi rodo")

@grammar.test
def ungrammatical():
    assert not camxes.isgrammatical("coi '")


all = Tests([parse, grammar])
