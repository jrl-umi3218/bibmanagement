# Copyright 2019-2022 CNRS-AIST JRL

from bibmanagement.utils import BibFilter
import unittest

def equal0(x):
    return x == 0
    
def lowerThan5(x):
    return x < 5
    
def positive(x):
    return x > 0

class TestComparator(unittest.TestCase):
    def test_and(self):
        opAnd = BibFilter.And(lowerThan5, positive)
        self.assertTrue(opAnd(3))
        self.assertFalse(opAnd(0))
        self.assertFalse(opAnd(8))
        
        self.assertTrue(opAnd([2,3,6]))
        self.assertFalse(opAnd([-1,6,8]))
        
        opAnd._any = False
        self.assertTrue(opAnd([2,3,4]))
        self.assertFalse(opAnd([2,3,6]))
        
    def test_or(self):
        opOr = BibFilter.Or(equal0, positive)
        self.assertFalse(opOr(-1))
        self.assertTrue(opOr(0))
        self.assertTrue(opOr(1))
        
        self.assertTrue(opOr([-1,0]))
        self.assertFalse(opOr([-2,-1]))
        
        opOr._any = False
        self.assertTrue(opOr([0,1]))
        self.assertFalse(opOr([0,-1]))
        
    def test_not(self):
        opNot = BibFilter.Not(lowerThan5)
        self.assertFalse(opNot(3))
        self.assertFalse(opNot(1))
        self.assertTrue(opNot(8))
        
        self.assertTrue(opNot([6,9,11]))
        self.assertTrue(opNot([6,4,11]))
        self.assertFalse(opNot([1,2,3]))
        
        opNot._any = False
        self.assertTrue(opNot([6,9,11]))
        self.assertFalse(opNot([6,4,11]))
        self.assertFalse(opNot([1,2,3]))
        
    def test_eq(self):
        opEq = BibFilter.EQ(42)
        self.assertTrue(opEq(42))
        self.assertFalse(opEq(3))
        
        self.assertTrue(opEq([7,42,79]))
        self.assertFalse(opEq([7,35,79]))
        
    def test_ne(self):
        opNe = BibFilter.NE(42)
        self.assertFalse(opNe(42))
        self.assertTrue(opNe(3))
        
        self.assertTrue(opNe([7,42,79]))
        self.assertFalse(opNe([42,42,42]))
        
    def test_ge(self):
        opGe = BibFilter.GE(42)
        self.assertTrue(opGe(42))
        self.assertTrue(opGe(45))
        self.assertFalse(opGe(3))
        
        self.assertTrue(opGe([7,42,79]))
        self.assertFalse(opGe([1,2,3]))
        
    def test_le(self):
        opLe = BibFilter.LE(42)
        self.assertTrue(opLe(42))
        self.assertFalse(opLe(45))
        self.assertTrue(opLe(3))
        
        self.assertTrue(opLe([7,42,79]))
        self.assertFalse(opLe([51,52,53]))
    
    def test_gt(self):
        opGt = BibFilter.GT(42)
        self.assertFalse(opGt(42))
        self.assertTrue(opGt(45))
        self.assertFalse(opGt(3))
        
        self.assertTrue(opGt([7,42,79]))
        self.assertFalse(opGt([1,2,3]))
        
    def test_lt(self):
        opLt = BibFilter.LT(42)
        self.assertFalse(opLt(42))
        self.assertFalse(opLt(45))
        self.assertTrue(opLt(3))
        
        self.assertTrue(opLt([7,42,79]))
        self.assertFalse(opLt([51,52,53]))
        
    def test_in(self):
        opIn = BibFilter.IN([1,12,42,76])
        self.assertTrue(opIn(42))
        self.assertFalse(opIn(45))
        self.assertTrue(opIn(12))
        
        self.assertTrue(opIn([7,42,79]))
        self.assertFalse(opIn([51,52,53]))
        
    def test_contains(self):
        opCo = BibFilter.Contains('string')
        self.assertTrue(opCo('long_string'))
        self.assertFalse(opCo('stride'))
        self.assertTrue(opCo('string'))