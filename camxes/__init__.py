from os import path
from fnmatch import fnmatch
from subprocess import Popen, PIPE

from lepl import *


JARFILE = path.join(path.dirname(__file__), 'camxes.jar')


class NodeBase(Node):

    def filter(self, predicate):
        if predicate(self):
            yield self
            return
        for child in self:
            if isinstance(child, Node):
                for node in child.filter(predicate):
                    yield node
            elif predicate(child):
                yield child

    def find(self, name=None):
        def predicate(node):
            if isinstance(node, Node):
                return name is not None and fnmatch(node.name, name)
            return name is None
        return list(self.filter(predicate))

    def map(self, transformer):
        return tuple([transformer(self)] +
                     [child.map(transformer) if isinstance(child, Node)
                                             else transformer(child)
                                             for child in self])

    def primitive(self):
        def stringify(node):
            if isinstance(node, Node):
                return node.name
            return node
        return self.map(stringify)

    def __repr__(self):
        return '<{name} {{{text}}}>'.format(name=self.name,
                                            text=' '.join(self.find()))


def named_node(args):
    node_type = type(str(args[0]), (NodeBase,), {'name': args[0]})
    return node_type(*args[1:])

ident = Word(Letter() | Digit() | Literal("'"))
space = ~Literal(' ')
node  = Delayed()
node += ( ( space & ident & ~Literal('=(')
          & space & node[1:] & space
          & ~Literal(')') & space
          > named_node
          )
        | ident
        )


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

def parse(text):
    return node.parse(camxes('-f', text))[0]

def morphology(text):
    return node.parse(camxes('-Mf', text))[0]

def find_affixes(compound):
    affixes = []
    rafsi = morphology(compound).find('lujvo')[0].find('*Rafsi')
    for node in rafsi:
        affixes.append(''.join(lerfu[0] for lerfu in node.find('?')))
    return tuple(affixes)

def isgrammatical(text):
    return camxes('-t', text) == text
