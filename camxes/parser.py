from lepl import *
from .nodes import named_node


name  = Word(Letter() | Digit())
token = Add(AnyBut(')')[1:])
space = ~Literal(' ')
node  = Delayed()
node += ( space & name & ~Literal('=(')
        & space & node[1:] & space
        & ~Literal(')') & space
        > named_node
        ) | token
