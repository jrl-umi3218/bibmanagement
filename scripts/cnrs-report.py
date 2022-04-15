from bibParser import *
from Entry import *
import Fields.Date
import Fields.FormatExpr
import Fields.StringField
import Fields.Authors
import Fields.Pages
import Fields.Journal
import FormatExpr.Parser as Parser
import Biblio
import utils.StyleFilters as sf
import utils.BibFilter as ub

# Path to JRLPubli data folder
dataPath = 'C:/Work/admin/JRLPubli/'

# Load data for journal and conferences
Fields.Journal.Journal.readVectorList(dataPath+'journal.json')
Fields.Booktitle.Booktitle.readVectorList(dataPath+'conferences.json')

# Reading the bib file and resolving crossrefs
bib = Biblio.Biblio.fromBibFile(dataPath+'master.bib')
bib = bib.resolveCrossref()

# Criterion for sorting paper by lexicographic increasing (year, month, day)
crit = [('%year%','<'),('[%mm%]%month%', '<'),('[%dd%]%month%', '<')]

# Filtering and outputing international journal papers
bib2 = bib.filter(ub.Selector(type="article", year=ub.GE(2017), national=False, lab='jrl'))
bib2.sort(crit)
bib2.toWord(r"[][{%F% %Last%}{, }{ and }{}]%author%<?, ?>[][]%title%<?, ?>{[][]%booktitle%|[][]%journal%}<?, ?>{vol.%volume%}<?, ?>{%number%?no.%number%}<?, ?>{[%p%%f%[-]%l%]%pages%}<?, ?>%year%", out='journal')

# Filtering and outputing national journal papers
bib3 = bib.filter(ub.Selector(type="article", year=ub.GE(2017), national=True, lab='jrl'))
bib3.sort(crit)
bib3.toWord(r"[][{%F% %Last%}{, }{ and }{}]%author%<?, ?>[][]%title%<?, ?>{[][]%booktitle%|[][]%journal%}<?, ?>{vol.%volume%}<?, ?>{%number%?no.%number%}<?, ?>{[%p%%f%[-]%l%]%pages%}<?, ?>%year%", out='journalNat')

# Filtering and outputing international conference papers
bib4 = bib.filter(ub.Selector(type="InProceedings", year=ub.GE(2017), national=False, lab='jrl'))
bib4.sort(crit)
bib4.toWord(r"[][{%F% %Last%}{, }{ and }{}]%author%<?, ?>[][]%title%<?, ?>{[][]%booktitle%|[][]%journal%}<?, ?>{[%p%%f%[-]%l%]%pages%}<?, ?>%year%<?/?>[%mm%]%month%</?>[%dd%]%month%", out='conference')

# Filtering and outputing national conference papers
bib5 = bib.filter(ub.Selector(type="InProceedings", year=ub.GE(2017), national=True, lab='jrl'))
bib5.sort(crit)
bib5.toWord(r"[][{%F% %Last%}{, }{ and }{}]%author%<?, ?>[][]%title%<?, ?>{[][]%booktitle%|[][]%journal%}<?, ?>{[%p%%f%[-]%l%]%pages%}<?, ?>%year%<?/?>[%mm%]%month%</?>[%dd%]%month%", out='conferenceNat')