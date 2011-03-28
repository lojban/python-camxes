Python interface to camxes
==========================

To install, you need a Java runtime environment as a ``java`` command on
your ``$PATH``, Python 2.6+ (including 3.1) and python-setuptools (or
distribute). Then you can simply install this package from PyPI with
``easy_install`` or ``pip``, or as a dependency in your own ``setup.py``.
The parser itself is bundled with this package so you don't need to worry
about that.

::

    easy_install camxes


Parsing Lojban
--------------

The ``parse()`` function returns a parse tree of named nodes.

>>> import camxes
>>> print camxes.parse("coi rodo")
text
 `- free
     +- CMAVO
     |   `- COI
     |       `- u'coi'
     `- sumti5
         +- CMAVO
         |   `- PA
         |       `- u'ro'
         `- CMAVO
             `- KOhA
                 `- u'do'

Child nodes can be accessed by name as attributes, giving a list of such
nodes. If there are no child nodes with that name an exception is raised.

>>> print camxes.parse("coi rodo").free[0].sumti5[0].CMAVO[1]
CMAVO
 `- KOhA
     `- u'do'

You can also access nodes by sequential position without giving the name.

>>> print camxes.parse("coi rodo")[0][1]
sumti5
 +- CMAVO
 |   `- PA
 |       `- u'ro'
 `- CMAVO
     `- KOhA
         `- u'do'

Nodes iterate over their children.

>>> list(camxes.parse("coi rodo")[0][1])
[CMAVO(...), CMAVO(...)]

They also know their name.

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
         `- u'mupli'


Parsing only morphology
-----------------------

The ``morphology()`` function works much like ``parse()``.

>>> print camxes.morphology("coi")
text
 `- CMAVO
     `- COI
         +- c
         |   `- u'c'
         +- o
         |   `- u'o'
         `- i
             `- u'i'
