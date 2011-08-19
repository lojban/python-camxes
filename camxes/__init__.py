from .nodes import isbranch, isleaf
from .parser import node
from .process import camxes


def parse(text, spaces=False):
    if spaces:
        return node.parse(camxes('-fs', text))[0]
    return node.parse(camxes('-f', text))[0]


def morphology(text):
    return node.parse(camxes('-Mf', text))[0]


def decompose(compound):
    root = morphology(compound)
    nodes = (root, root[0], root[0][0])
    if any(len(node) != 1 for node in nodes) or \
       [node.name for node in nodes] != ['text', 'BRIVLA', 'lujvo']:
        raise ValueError('invalid compound {0!r}'.format(compound))
    rafsi = root.find('*Rafsi')
    parts = []
    for node in rafsi:
        parts.append(''.join(''.join(lerfu.leafs)
            for lerfu in node.find('consonant', 'vowel', 'h', 'diphthong')))
        for glue in node.find('rHyphen', 'y'):
            parts.extend(glue.leafs)
    return tuple(parts)


def isgrammatical(text):
    return camxes('-t', text) == text
