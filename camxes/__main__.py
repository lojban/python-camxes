import sys
from camxes import parse, isgrammatical

print parse(sys.argv[1])
print
if not isgrammatical(sys.argv[1]):
    print 'not',
print 'grammatical:', sys.argv[1]
