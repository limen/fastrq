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


class TestCappedStack(TestStack):
    def setUp(self):
        self.queue = CappedStack("fastrq_capped_stack", 3)
        self.queue.destruct()
    
    def test_push_pop(self):
        self.queue.push([1, 2])
        self.assertEqual(self.queue.push([3, 4]), 'err_qof')
        self.assertEqual(self.queue.push(3), 3)
        self.assertEqual(self.queue.push(4), 'err_qf')
