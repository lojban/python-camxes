Python Interface to Camxes
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

Turn a tree back into Lojban with the ``lojban`` property.

>>> camxes.parse("coi rodo!").lojban
u'coi ro do'

This joins the leaf nodes with a space, but you can preserve spaces and
punctuation by passing ``spaces=True`` to ``parse()``.

>>> camxes.parse("coi rodo!", spaces=True).lojban
u'coi rodo!'

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
[<CMAVO {ro}>, <CMAVO {do}>]

They also know their name.

>>> camxes.parse("coi rodo")[0][1].name
u'sumti5'


Verifying Grammatical Validity
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


Deconstructing Compound Words into Affixes
------------------------------------------

``decompose()`` gives you the affixes and hyphens of a compound.

>>> camxes.decompose("genturfa'i")
(u'gen', u'tur', u"fa'i")

It will complain for input that is not a single, valid compound.

>>> camxes.decompose("camxes")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid compound 'camxes'


Parsing Only Morphology
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


Tree Traversal
--------------

Search for nodes with the ``find()`` method. It takes any number of arguments
that are wildcard-matched against node names. This operation recurses down
each branch until a match is found, but does not search children of
matching nodes.

>>> camxes.parse("coi rodo").find('sumti*')
[<sumti5 {ro do}>]

>>> camxes.parse("coi rodo").find('PA', 'KOhA')
[<PA {ro}>, <KOhA {do}>]

Key access on nodes is a shortcut for the first match of a find.

>>> camxes.parse("la camxes genturfa'i fi la lojban")['cmene']
<cmene {camxes}>

The ``leafs`` property is a list of all leaf nodes, which should be the
unicode lexemes.

>>> camxes.parse("coi rodo").leafs
[u'coi', u'ro', u'do']

The ``branches()`` method finds the parents of nodes whose leafs match the
arguments. This lets you search for the branches a sequence of lexemes
belong to.

>>> camxes.parse("lo ninmu cu klama lo tcadu").branches("lo")
[<sumti6 {lo ninmu}>, <sumti6 {lo tcadu}>]
>>> camxes.parse("lo ninmu cu klama lo tcadu").branches("ninmu")
[<sumti6 {lo ninmu}>]
>>> camxes.parse("lo ninmu cu klama lo tcadu").branches("klama", "lo", "tcadu")
[<sentence {lo ninmu cu klama lo tcadu}>]

A generalization of these is called ``filter()`` and takes a predicate
function that decides if a node should be listed. ``filter()`` is a
generator so we use ``list()`` here to see the results.

>>> leafparent = lambda node: camxes.isleaf(node[0])
>>> list(camxes.parse("coi rodo").filter(leafparent))
[<COI {coi}>, <PA {ro}>, <KOhA {do}>]


Primitive Trees
---------------

Nodes have a primitive representation of a tuple where the first element is
the name of the node and the second a list of children. This property is
called ``primitive`` and can be useful if you're serializing a parse tree
to a “dumb” format such as JSON.

>>> from pprint import pprint
>>> pprint(camxes.parse("coi rodo").primitive)
(u'text',
 [(u'free',
   [(u'CMAVO', [(u'COI', [u'coi'])]),
    (u'sumti5',
     [(u'CMAVO', [(u'PA', [u'ro'])]), (u'CMAVO', [(u'KOhA', [u'do'])])])])])

>>> import json
>>> print json.dumps(camxes.parse("coi").primitive, indent=2)
[
  "text", 
  [
    [
      "CMAVO", 
      [
        [
          "COI", 
          [
            "coi"
          ]
        ]
      ]
    ]
  ]
]
