import unittest
from mock import Mock

from collections import namedtuple

from pyxrays.filters.generic import fold, prune, inline

class E(namedtuple('Entry', 'depth value')):
    def with_depth(self, new_depth):
        return E(new_depth, self.value)


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
            return 'ok' not in e.value
        
        result = list(prune(filt, trace))
        expected = [t for t in trace if 'drop' not in t.value]
        self.assertEqual(expected, result)


    def test_filter_keep_single(self):
        self._test_filter((1, 'ok_keep'))
        
    
    def test_filter_drop_single(self):
        self._test_filter((1, 'drop'))


    def test_filter_drop_recursion(self):
        self._test_filter(
            (0, 'drop'),
            (1, 'ok_but_must_drop_automatically'),)
            

    def test_filter_keep_nested(self):
        self._test_filter(
            (0, 'ok1'),
            (1, 'ok2'))

        
    def test_filter_drop_in_middle(self):
        self._test_filter(
            (0, 'ok1'),
            (1, 'ok2'),
            (0, 'drop'),
            (1, 'ok_but_drop'),
            (0, 'ok3'),
            (1, 'ok4'))


#class NormalizeTest(unittest.TestCase):
#    def _test_normalize(self, *data):
#        trace = [E(depth, val) for (depth, val, _) in data]
#        expected = 


class InlineTest(unittest.TestCase):

    def _test_inline(self, *data):
        trace = [E(*t[:-1]) for t in data]
        expected = [E(depth, val) for (_, val, depth) in data \
                        if 'inline' not in val]

        def f(entry):
            return 'inline' in entry.value

        result = inline(f, trace)
        self.assertEquals(expected, list(result))

        
    def test_inline_single1(self):
        self._test_inline(
            (1, 'inline', 0))


    def test_inline_single2(self):
        self._test_inline(
            (1, 'dont_touch', 1))


    def test_inline(self):
        self._test_inline(
            (1, 'inline', 0),
            (2, 'shift', 1))


    def test_nested_inline(self):
        self._test_inline(
            (1, 'inline', 0),
            (2, 'shift1', 1),
            (2, 'inline-too', 0),
            (3, 'shift2', 1),
            (1, 'keep-as-is', 1))


    def test_inline_in_middle(self):
        self._test_inline(
            (0, 'keep', 0),
            (0, 'inline', 0),
            (1, 'shift0', 0),
            (2, 'keep2', 2)) # TODO normalization
