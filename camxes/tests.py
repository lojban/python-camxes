from attest import Tests, assert_hook, raises
import camxes


parse = Tests()

@parse.context
def parse_tree():
    yield camxes.parse("coi rodo mi cipra loka na cfila la camxes")

@parse.test
def ast(pt):
    assert pt.free[0].CMAVO[0].COI[0][0] == "coi"
    assert pt.sentence[0].bridiTail3[0].BRIVLA[0].gismu[0][0] == "cipra"

@parse.test
def index(pt):
    assert pt[0][0][0][0] == "coi"
    assert pt[1][1][0][0][0] == "cipra"

@parse.test
def node_names(pt):
    assert pt[0].name == 'free'
    assert pt[1].name == 'sentence'

@parse.test
def filter(pt):
    nodes = pt.filter(lambda node: getattr(node, 'name', None) == 'cmene')
    node = list(nodes)[0][0]
    assert node == "camxes"

@parse.test
def find(pt):
    assert pt.find('cmene')[0][0] == "camxes"
    assert pt.find('COI', 'PA') == pt.find('COI') + pt.find('PA')
    assert pt['cmene'] is pt.find('cmene')[0]
    with raises(KeyError):
        pt['']

@parse.test
def leafs(pt):
    assert ' '.join(pt.find('sumti6')[0].leafs) == "lo ka na cfila la camxes"

@parse.test
def branches(pt):
    assert pt.branches("lo") == pt.find('sumti6')
    assert pt.branches("ro", "do") == pt.find('free')

@parse.test
def map(pt):
    node = pt.find('sumti5')[0]
    def swapcase(node):
        return getattr(node, 'name', node).swapcase()
    assert node.map(swapcase) == \
        ('SUMTI5',
            ('cmavo', ('pa', "RO")),
            ('cmavo', ('koHa', "DO")))

@parse.test
def primitive(pt):
    node = pt.find('sumti5')[0]
    assert node.primitive == \
        ('sumti5',
            ('CMAVO', ('PA', "ro")),
            ('CMAVO', ('KOhA', "do")))

@parse.test
def node_repr(pt):
    assert repr(pt.find('cmene')[0]) == "<cmene {camxes}>"


spaces = Tests()

@spaces.context
def parse_trees_from_outer_space():
    yield camxes.parse("coi rodo!"), camxes.parse("coi rodo!", spaces=True)

@spaces.test
def space_leafs(nospaces, withspaces):
    assert nospaces.leafs == ("coi", "ro", "do")
    assert withspaces.leafs == ("coi", " ", "ro", "do", "!")

@spaces.test
def lojban(nospaces, withspaces):
    assert nospaces.lojban == "coi ro do"
    assert withspaces.lojban == "coi rodo!"


morphology = Tests()

@morphology.test
def non_lojban():
    assert camxes.morphology("jbo")[0].name == 'nonLojbanWord'

@morphology.test
def affixes():
    compounds = {
        "ba'argau": ("ba'a", "r", "gau"),
        "ba'armo'a": ("ba'a", "r", "mo'a"),
        "ba'ostu": ("ba'o", "stu"),
        "ba'urtadji": ("ba'u", "r", "tadj"),
        "backemselrerkru": ("bac", "kem", "sel", "rer", "kru"),
        "backla": ("bac", "kla"),
        "bacycripu": ("bac", "y", "crip"),
    }

    for compound, affixes in compounds.iteritems():
        assert camxes.decompose(compound) == affixes

    not_compounds = ("camxes", "coi", "donri", "sfe'ero")
    for noncompound in not_compounds:
        with raises(ValueError):
            camxes.decompose(noncompound)


grammar = Tests()

@grammar.test
def grammatical():
    assert camxes.isgrammatical("coi rodo")

@grammar.test
def ungrammatical():
    assert not camxes.isgrammatical("coi '")


all = Tests([parse, spaces, morphology, grammar])
