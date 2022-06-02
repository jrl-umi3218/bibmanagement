def testEntries():
    '''Partial biblio from \"G. Perec, Experimental demonstration of the tomatotopic organization in the Soprano (Cantatrix sopranica L.)\"'''
    e1 = {'ID': 'chou:laryngol:1927',
          'ENTRYTYPE': 'Article',
          'author': 'Chou, O. and Lai, A.',
          'title': 'Note on the tomatic inhibition in the singing gorilla',
          'year': 1927,
          'volume': 8,
          'pages': '41--42',
          'crossref': 'jrnl:laryngol'
         }
         
    e2 = {'ID': 'chou:fat:1927',
          'ENTRYTYPE': 'InCollection',
          'author': 'Chou, O. and Lai, A.',
          'title': 'Musicali effetti del tomatino jettatura durante il reprezentazione dell\' opere di Verdi',
          'pages': '145--172',
          'crossref': 'book:fat'}
          
    e3 = {'ID': 'jeanpace:dijon:1932',
          'ENTRYTYPE': 'Article',
          'author': 'Jeanpace, L. and Desmeyeurs, P.',
          'title': 'Recherches histologiques sur les noyaux de Pesch et de Poissy',
          'year': 1932,
          'volume': 5,
          'pages': '1--73',
          'journal': 'Dijon med.'}
          
    e4 = {'ID': 'beulott:ias:1974',
          'ENTRYTYPE': 'InProceedings',
          'author': 'Beulott, A. and Rebeloth, B. and Dizdeudayre, C.D.',
          'title': 'Brain designing',
          'crossref': 'conf:ias:1974'}
          
    e5 = {'ID': 'dendritt:brainres:1975',
          'ENTRYTYPE': 'Article',
          'author': 'Dendritt, A. and Haxon, B.',
          'title': 'Note on the tomatic inhibition in the singing gorilla',
          'crossref': 'jrnl:brainres',
          'note': 'in press'
         }
         
    e6 = {'ID': 'balalaika:pathol:1515',
          'ENTRYTYPE': 'Article',
          'author': 'Balalaïka, P.',
          'title': 'Deafness caused by tomato injury. Observations on half a case',
          'year': 1515,
          'volume': 1,
          'pages': '1--7',
          'crossref': 'jrnl:pathol'}
         
    e7 = {'ID': 'einstein:nfs:1974',
          'ENTRYTYPE': 'InProceedings',
          'author': 'Einstein, Z. and Zweistein, D. and Dreistein, V. and Vierstein, F. and St. Pierre, E.',
          'title': 'Spatial integration in the temporal cortex',
          'crossref': 'conf:nfs:1974'}
    
    c1 = {'ID':'jrnl:laryngol',
          'ENTRYTYPE': 'Proceedings',
          'title': 'Acta Laryngologia',
          'journal': 'Acta Laryngologia'
         }
         
    c2 = {'ID':'book:fat',
          'ENTRYTYPE': 'Book',
          'title': 'Festschrift am Arturo Toscanini',
          'editor': 'A. Pick, I. Pick, E. Kohl & E. Gramm',
          'year': 1929,
          'publisher': 'Thieme & Becker',
          'address': 'München'
         }
         
    c3 = {'ID':'conf:ias:1974',
          'ENTRYTYPE': 'Proceedings',
          'title': 'Institute of advanced studies',
          'year': 1974,
          'address': 'Châteauneuf-en-Thymerais',
          'booktitle': 'Institute of advanced studies'
         }
         
    c4 = {'ID':'jrnl:brainres',
          'ENTRYTYPE': 'Proceedings',
          'title': 'Brain Research',
          'journal': 'Brain Research'
         }
         
    c5 = {'ID':'jrnl:pathol',
          'ENTRYTYPE': 'Proceedings',
          'title': 'Acta pathologica marignan',
          'journal': 'Acta pathologica marignan'
         }
         
    c6 = {'ID':'conf:nfs:1974',
          'ENTRYTYPE': 'Proceedings',
          'title': 'Research Proceedings of the Neurophysioly Fanatic Society',
          'year': 1974,
          'booktitle': 'Research Proceedings of the Neurophysioly Fanatic Society'
         }
         
    return [e1, e2, e3, e4, e5, e6, e7, c1, c2, c3, c4, c5, c6]