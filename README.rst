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

>>> print camxes.parse("coi rodo").free[0].sumti5[0].CMAVO[1]
CMAVO
 `- KOhA
     `- word u'do'

