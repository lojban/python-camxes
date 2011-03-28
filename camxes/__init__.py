from os import path
from subprocess import Popen, PIPE
from lepl import *


JARFILE = path.join(path.dirname(__file__), 'camxes.jar')


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
        | ident
        )


procs = {}

def camxes(arg, input):
    if arg not in procs or procs[arg].poll() is None:
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

def isgrammatical(text):
    return camxes('-t', text) == text
