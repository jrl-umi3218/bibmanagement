from bibmanagement.bibParser import *
from bibmanagement.Entry import *
from bibmanagement.fields import Date
from bibmanagement.fields import FormatExpr
from bibmanagement.fields import StringField
from bibmanagement.fields import Authors
from bibmanagement.fields import Pages
from bibmanagement.fields import Journal
from bibmanagement.fields import Booktitle
from bibmanagement.formatExpr import Parser
from bibmanagement import Biblio
from bibmanagement.utils import StyleFilters as sf
from bibmanagement.utils import BibFilter as ub

if __name__ == '__main__':
    # Path to JRLPubli data folder
    dataPath = 'C:/Work/admin/JRLPubli/'

    # Default file names
    bibFile = 'master.bib'
    journalFile = 'journal.json'
    confFile = 'conferences.json'

    # Relative path for output
    outPath = './'


# Load data for journal and conferences
Journal.Journal.readVectorList(dataPath+journalFile)
Booktitle.Booktitle.readVectorList(dataPath+confFile)

# Reading the bib file and resolving crossrefs
bib = Biblio.Biblio.fromBibFile(dataPath+bibFile)
bib = bib.resolveCrossref()

# Criterion for sorting paper by lexicographic increasing (year, month, day)
crit = [('%year%','<'),('[%mm%]%month%', '<'),('[%dd%]%month%', '<')]

# Filtering and outputing international journal papers
bib2 = bib.filter(ub.Selector(type="article", year=ub.GE(2017), national=False, lab='jrl'))
bib2.sort(crit)
bib2.toWord(r"[][{%F% %Last%}{, }{ and }{}]%author%<?, ?>[][]%title%<?, ?>{[][]%booktitle%|[][]%journal%}<?, ?>{vol.%volume%}<?, ?>{%number%?no.%number%}<?, ?>{[%p%%f%[-]%l%]%pages%}<?, ?>%year%", out=outPath+'journal')

# Filtering and outputing national journal papers
bib3 = bib.filter(ub.Selector(type="article", year=ub.GE(2017), national=True, lab='jrl'))
bib3.sort(crit)
bib3.toWord(r"[][{%F% %Last%}{, }{ and }{}]%author%<?, ?>[][]%title%<?, ?>{[][]%booktitle%|[][]%journal%}<?, ?>{vol.%volume%}<?, ?>{%number%?no.%number%}<?, ?>{[%p%%f%[-]%l%]%pages%}<?, ?>%year%", out=outPath+'journalNat')

# Filtering and outputing international conference papers
bib4 = bib.filter(ub.Selector(type="InProceedings", year=ub.GE(2017), national=False, lab='jrl'))
bib4.sort(crit)
bib4.toWord(r"[][{%F% %Last%}{, }{ and }{}]%author%<?, ?>[][]%title%<?, ?>{[][]%booktitle%|[][]%journal%}<?, ?>{[%p%%f%[-]%l%]%pages%}<?, ?>%year%<?/?>[%mm%]%month%</?>[%dd%]%month%", out=outPath+'conference')

# Filtering and outputing national conference papers
bib5 = bib.filter(ub.Selector(type="InProceedings", year=ub.GE(2017), national=True, lab='jrl'))
bib5.sort(crit)
bib5.toWord(r"[][{%F% %Last%}{, }{ and }{}]%author%<?, ?>[][]%title%<?, ?>{[][]%booktitle%|[][]%journal%}<?, ?>{[%p%%f%[-]%l%]%pages%}<?, ?>%year%<?/?>[%mm%]%month%</?>[%dd%]%month%", out=outPath+'conferenceNat')