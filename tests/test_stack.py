import unittest

from fastrq.stack import Stack, CappedStack


class TestStack(unittest.TestCase):
    def setUp(self):
        self.queue = Stack("fastrq_stack")
        self.queue.destruct()
    
    def tearDown(self):
        self.queue.destruct()
    
    def test_push_pop(self):
        self.assertEqual(self.queue.push([1, 2, 3]), 3)
        self.assertEqual(self.queue.length(), 3)
        self.assertEqual(self.queue.pop(), '3')
        self.assertEqual(self.queue.pop(2), ['2', '1'])
        self.assertEqual(self.queue.pop(), None)

    def test_push_e(self):
        self.assertEqual(self.queue.push_ne(1), 1)
        self.assertFalse(self.queue.push_ne(1))
        self.queue.destruct()
        self.assertFalse(self.queue.push_ae(1))
        self.queue.push(1)
        self.assertEqual(self.queue.push_ae(1), 2)

    def test_push_ni(self):
        self.assertEqual(self.queue.push_ni(1), (1, True))
        self.assertEqual(self.queue.push_ni('apple'), (2, True))
        self.assertEqual(self.queue.push_ni(1), (2, False))
        self.assertEqual(self.queue.push_ni('apple'), (2, False))

    def test_indexof(self):
        self.queue.push(['apple', 'banana'])
        self.assertEqual(self.queue.indexof_one('banana'), 0)
        self.assertEqual(self.queue.indexof_one('apple'), 1)
        self.assertEqual(self.queue.indexof_one('pear'), None)
        self.assertEqual(self.queue.indexof_many(['apple', 'banana', 'pear']), {'apple': 1, 'banana': 0, 'pear': None})


class TestCappedStack(TestStack):
    def setUp(self):
        self.queue = CappedStack("fastrq_capped_stack", 3)
        self.queue.destruct()
    
    def test_push_pop(self):
        self.queue.push([1, 2])
        self.assertEqual(self.queue.push([3, 4]), 'err_qof')
        self.assertEqual(self.queue.push(3), 3)
        self.assertEqual(self.queue.push(4), 'err_qf')

    def test_push_e(self):
        self.assertEqual(self.queue.push_ne(1), 1)
        self.assertFalse(self.queue.push_ne(1))
        self.queue.destruct()
        self.assertFalse(self.queue.push_ae(1))
        self.queue.push(1)
        self.assertEqual(self.queue.push_ae(1), 2)

    def test_push_ni(self):
        self.assertEqual(self.queue.push_ni(1), (1, True))
        self.assertEqual(self.queue.push_ni(1), (1, False))
        self.assertEqual(self.queue.push_ni(2), (2, True))
        self.assertEqual(self.queue.push_ni(3), (3, True))
        self.assertEqual(self.queue.push_ni(4), 'err_qf')

