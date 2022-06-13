# Copyright 2019-2022 CNRS-AIST JRL

import json
from extra.Position import *

class AuthorData:
    @staticmethod
    def _parseName(name):
        s = name.split(',')
        if len(s) != 2:
            raise ValueError('Expecting name of the form \'last, first\', but got {}'.format(name))
        return s
        
    @staticmethod
    def _requireKey(p, k, pos=None):
        if not k in p.keys():
            if not pos:
                pos = p
            raise ValueError('Require key {} in {}'.format(k, pos))
        
    @staticmethod
    def _processPosition(positions):
        sequentialPos = []
        parallelPos = []
        prev = {}
        for i,pos in enumerate(positions):
            parallel = pos.get('parallel', False)
            if parallel:
                parallelPos.append(Position(**pos))
            else:
                if i!=0:
                    AuthorData._requireKey(pos, 'start')
                # Recopy some fields of the previous position
                p = {i:prev[i] for i in ['status', 'contract', 'employer', 'affiliation'] if i in prev.keys()}
                # Add items of the current position to p. Items with identical keys will be
                # overwritten by the values of the current position
                p = {**p, **pos}
                AuthorData._requireKey(p, 'status', pos)
                AuthorData._requireKey(p, 'contract', pos)
                AuthorData._requireKey(p, 'employer', pos)
                AuthorData._requireKey(p, 'affiliation', pos)
                
                sequentialPos.append(p)
                prev = p
        
        prev = None
        for pos in sequentialPos:
            if prev: 
                if 'end' not in prev.keys():
                    prev['end'] = PreviousDay(pos['start'] )
                if 'pubStart' in prev.keys() and 'pubEnd' not in prev.keys():
                    prev['pubEnd'] = PreviousDay(pos['pubStart'])
            prev = pos
            
        positions = [Position(**p) for p in sequentialPos]
        positions.extend(parallelPos)
        return positions
        
    
    def __init__(self, **kwargs):
        name = kwargs.get('name')
        if not name:
            raise ValueError('No name found for entry\n {}'.format(kwargs))
        self.last, self.first = AuthorData._parseName(name)
        
        self.japanese = kwargs.get('japanese')
        
        alt = kwargs.get('alternative')
        if alt:
            if isinstance(alt, str):
                self.alternative = [tuple(AuthorData._parseName(alt))]
            else: #assume iterable
                self.alternative =[tuple(AuthorData._parseName(name)) for name in alt]
                
        position = kwargs.get('position')
        self.position = AuthorData._processPosition(position)