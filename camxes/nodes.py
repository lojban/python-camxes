# coding: utf-8
from fnmatch import fnmatch
from itertools import cycle
from lepl import Node


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
