Python interface to camxes
==========================


Parsing Lojban
--------------

The ``parse()`` function returns a parse tree of named nodes.

>>> import camxes
>>> print camxes.parse("coi rodo")
text
 `- free
     +- CMAVO
     |   `- COI
     |       `- word u'coi'
     `- sumti5
         +- CMAVO
         |   `- PA
         |       `- word u'ro'
         `- CMAVO
             `- KOhA
                 `- word u'do'

Child nodes can be accessed by name as attributes, giving a list of such
nodes. If there are no child nodes with that name an exception is raised.

>>> print camxes.parse("coi rodo").free[0].sumti5[0].CMAVO[1]
CMAVO
 `- KOhA
     `- word u'do'

You can also access nodes by sequential position without giving the name.

>>> print camxes.parse("coi rodo")[0][1]
sumti5
 +- CMAVO
 |   `- PA
 |       `- word u'ro'
 `- CMAVO
     `- KOhA
         `- word u'do'

Nodes iterate over their children.

>>> list(camxes.parse("coi rodo")[0][1])
[CMAVO(...), CMAVO(...)]

Nodes also knows their name.

>>> camxes.parse("coi rodo")[0][1].name
u'sumti5'


Verifying grammatical validity
------------------------------

``parse()`` is able to parse some ungrammatical input by processing as much
as is grammatical. It is therefore unreliable for checking if some text is
grammatical. For this purpose, there is the ``isgrammatical()`` predicate.

>>> camxes.isgrammatical("coi rodo")
True
>>> camxes.isgrammatical("mupli cu fliba")
False
>>> print camxes.parse("mupli cu fliba")
text
 `- BRIVLA
     `- gismu
         `- word u'mupli'
