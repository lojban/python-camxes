from subprocess import Popen, PIPE
from lepl import *


def named_node(args):
    node_type = type(str(args[0]), (Node,), {'name': args[0]})
    return node_type(*args[1:])

ident = Word(Letter() | Digit() | Literal("'"))
space = ~Literal(' ')
node  = Delayed()
node += ( ( space & ident & ~Literal('=(')
          & space & node[1:] & space
          & ~Literal(')') & space
          > named_node
          )
        | (ident > 'word')
        )


procs = {}

def camxes(arg, input):
    if arg not in procs or procs[arg] is None:
        procs[arg] = Popen(['camxes', arg], stdout=PIPE, stdin=PIPE)
        procs[arg].stdout.readline()
    procs[arg].stdin.write(input + '\n')
    output = procs[arg].stdout.readline().rstrip('\n')
    return output

def parse(text):
    return node.parse(camxes('-f', text))[0]

def isgrammatical(text):
    return camxes('-t', text) == text


if __name__ == '__main__':
    import sys
    print parse(sys.argv[1])
    print
    if not isgrammatical(sys.argv[1]):
        print 'not',
    print 'grammatical:', sys.argv[1]
