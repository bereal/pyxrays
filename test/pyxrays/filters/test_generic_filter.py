import unittest
from mock import Mock

from collections import namedtuple

from pyxrays.filters.generic import fold, prune

E = namedtuple('Entry', 'depth value')


class FoldTest(unittest.TestCase):

    def _test_fold(self, *trace):
        trace = [E(*t) for t in trace]
        
        def filt(e):
            return 'fold' in e.value
        
        result = list(fold(filt, trace))
        expected = [t for t in trace if 'drop' not in t.value]
        self.assertEqual(expected, result)
             
    
    def test_single_fold(self):
        self._test_fold(
            (1, 'foldme'),
            (2, 'drop'))


    def test_fold_in_middle(self):
        self._test_fold(
            (1, 'val1'),
            (2, 'val2'),
            (1, 'foldme'),
            (2, 'dropme'),
            (1, 'val3'))


    def test_fold_nested(self):
        self._test_fold(
            (1, 'foldme'),
            (2, 'drop1'),
            (3, 'drop2'))


    def test_fold_several(self):
        self._test_fold(
            (1, 'foldme1'),
            (2, 'drop1'),
            (3, 'drop3'),
            (1, 'donttouch1'),
            (2, 'donttouch2'),
            (1, 'foldme2'),
            (2, 'drop2'))


        
class PruneTest(unittest.TestCase):
    def _test_filter(self, *trace):
        '''
        Entries with 'OK' in the value will be passed by filter
        Entries with 'drop' in the value are expected to be removed
        '''
        trace = [E(*t) for t in trace]
        
        def filt(e):
            return 'ok' in e.value
        
        result = list(prune(filt, trace))
        expected = [t for t in trace if 'drop' not in t.value]
        self.assertEqual(expected, result)


    def test_filter_keep_single(self):
        self._test_filter((1, 'ok_keep'))
        
    
    def test_filter_drop_single(self):
        self._test_filter((1, 'drop'))


    def test_filter_drop_recursion(self):
        self._test_filter(
            (1, 'drop'),
            (2, 'ok_but_must_drop_automatically'),)
            

    def test_filter_keep_nested(self):
        self._test_filter(
            (1, 'ok1'),
            (2, 'ok2'))

        
    def test_filter_drop_in_middle(self):
        self._test_filter(
            (1, 'ok1'),
            (2, 'ok2'),
            (1, 'drop'),
            (2, 'ok_but_drop'),
            (1, 'ok3'),
            (2, 'ok4'))

