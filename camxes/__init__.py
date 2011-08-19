# coding: utf-8
from pkg_resources import resource_filename
from fnmatch import fnmatch
from itertools import cycle
from subprocess import Popen, PIPE

from lepl import *


JARFILE = resource_filename(__name__, 'camxes.jar')


def isbranch(node):
    return isinstance(node, Node)

def isleaf(node):
    return not isbranch(node)


class NodeBase(Node):

    def filter(self, predicate):
        if predicate(self):
            yield self
            return
        for child in self:
            if isbranch(child):
                for node in child.filter(predicate):
                    yield node
            elif predicate(child):
                yield child

    @property
    def leafs(self):
        return list(self.filter(isleaf))

    def find(self, *names):
        def predicate(node):
            return isbranch(node) and \
                   any(fnmatch(node.name, name) for name in names)
        return list(self.filter(predicate))

    def branches(self, *leafs):
        leafs = list(leafs)
        def predicate(node):
            if isbranch(node):
                return any(isbranch(child) and child.leafs == leafs
                           for child in node)
        return list(self.filter(predicate))

    def __getitem__(self, index):
        if isinstance(index, basestring):
            try:
                return self.find(index)[0]
            except IndexError:
                raise KeyError(index)
        return Node.__getitem__(self, index)

    @property
    def lojban(self):
        sep = '' if self.find('*[Ss]paces') else ' '
        return sep.join(self.leafs)

    def brackets(self, pairs=u'() [] <> {} «»'):
        cycler = cycle(pairs.split())
        def bracketize(node):
            if len(node.leafs) == 1:
                return node.leafs[0]
            open, close = next(cycler)
            return open + ' '.join(bracketize(child)
                                   for child in node) + close
        return bracketize(self)

    @property
    def primitive(self):
        return self.name, [child.primitive if isbranch(child) else child
                           for child in self]

    def __repr__(self):
        return '<{name} {{{lojban}}}>'.format(name=self.name,
                                              lojban=self.lojban)


def named_node(args):
    node_type = type(str(args[0]), (NodeBase,), {'name': args[0]})
    return node_type(*args[1:])

name  = Word(Letter() | Digit())
token = Add(AnyBut(')')[1:])
space = ~Literal(' ')
node  = Delayed()
node += ( space & name & ~Literal('=(')
        & space & node[1:] & space
        & ~Literal(')') & space
        > named_node
        ) | token


procs = {}

def camxes(arg, input):
    if arg not in procs or procs[arg].poll() is not None:
        procs[arg] = Popen(['java', '-jar', JARFILE, arg],
                           stdout=PIPE, stdin=PIPE)
        for _ in xrange(len(arg) - 1):
            procs[arg].stdout.readline()
    procs[arg].stdin.write((input + '\n').encode('utf-8'))
    procs[arg].stdin.flush()
    output = procs[arg].stdout.readline()
    if 'M' in arg:
        procs[arg].stdout.readline()
        output = output.partition(b'Morphology pass: ')[2]
    output = output.decode('utf-8').rstrip('\n')
    return output

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
