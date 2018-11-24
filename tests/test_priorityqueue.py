import unittest

from fastrq.priorityqueue import PriorityQueue, CappedPriorityQueue, OfCappedPriorityQueue


class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        self.queue = PriorityQueue("fastrq_priority_queue")
        self.queue.destruct()
    
    def tearDown(self):
        self.queue.destruct()
    
    def test_push_pop(self):
        values = {
            "alice": 1,
            "bob": 2,
            "cath": 3,
        }
        self.assertEqual(self.queue.push(values), 3)
        self.assertEqual(self.queue.length(), 3)
        self.assertEqual(self.queue.pop(), ('alice', 1))
        self.assertEqual(self.queue.pop(2), [('bob', 2), ('cath', 3)])
        self.assertEqual(self.queue.pop(), None)
        self.assertEqual(self.queue.pop(2), [])
    
    def test_range(self):
        values = {
            "alice": 1,
            "bob": 2,
            "cath": 3,
        }
        self.queue.push(values)
        self.assertEqual(self.queue.range(), [('alice', 1), ('bob', 2), ('cath', 3)])
        self.assertEqual(self.queue.range(1, 2), [('alice', 1), ('bob', 2)])


class TestCappedPriorityQueue(TestPriorityQueue):
    def setUp(self):
        self.queue = CappedPriorityQueue("fastrp_capped_priority_queue", 3)
        self.queue.destruct()
    
    def test_push_pop(self):
        self.queue.push({
            'alice': 1,
            'bob': 2,
        })
        self.assertEqual(self.queue.push({'cath': 3, 'dylon': 4}), 'err_qof')
        self.assertEqual(self.queue.push({'cath': 3}), 3)
        self.assertEqual(self.queue.push({'cath': 3, 'dylon': 4}), 'err_qf')


class TestOfCappedPriorityQueue(TestCappedPriorityQueue):
    def setUp(self):
        self.queue = OfCappedPriorityQueue("fastrp_of_capped_priority_queue", 3)
        self.queue.destruct()
    
    def test_push_pop(self):
        p = self.queue.push({
            'cath': 3,
            'dylon': 4,
        })
        self.assertEqual(p, [2, []])
        self.assertEqual(self.queue.push({'alice': 1, 'bob': 2}), [3, [('dylon', 4)]])
        self.assertEqual(self.queue.push({'cathe': 0}), [3, [('cath', 3)]])