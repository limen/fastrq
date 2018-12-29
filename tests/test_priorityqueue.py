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

    def test_push_e(self):
        self.assertFalse(self.queue.push_ae({'alice': 1}))
        self.queue.push({'alice': 1})
        self.assertEqual(self.queue.push_ae({'bob': 2}), 2)
        self.assertFalse(self.queue.push_ne({'alice': 1}))
        self.queue.destruct()
        self.assertEqual(self.queue.push_ne({'alice': 1}), 1)

    def test_push_ni(self):
        self.assertEqual(self.queue.push_ni('alice', 1), (1, True))
        self.assertEqual(self.queue.push_ni('bob', 2), (2, True))
        self.assertEqual(self.queue.push_ni('alice', 1), (2, False))
        self.assertEqual(self.queue.push_ni('bob', 2), (2, False))
        self.assertEqual(self.queue.push_ni('cath', 3), (3, True))
    
    def test_range(self):
        values = {
            "alice": 1,
            "bob": 2,
            "cath": 3,
        }
        self.queue.push(values)
        self.assertEqual(self.queue.range(), [('alice', 1), ('bob', 2), ('cath', 3)])
        self.assertEqual(self.queue.range(1, 2), [('alice', 1), ('bob', 2)])

    def test_indexof(self):
        values = {
            "alice": 1,
            "bob": 2,
            "cath": 3,
        }
        self.queue.push(values)
        self.assertEqual(self.queue.indexof_one('alice'), 0)
        self.assertEqual(self.queue.indexof_one('bob'), 1)
        self.assertEqual(self.queue.indexof_one('cath'), 2)
        self.assertEqual(self.queue.indexof_one('dick'), None)
        self.assertEqual(self.queue.indexof_many(['alice', 'bob', 'dick']), {'alice': 0, 'bob': 1, 'dick': None})


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

    def test_push_e(self):
        self.assertFalse(self.queue.push_ae({'alice': 1}))
        self.queue.push({'alice': 1})
        self.assertEqual(self.queue.push_ae({'bob': 2}), 2)
        self.assertFalse(self.queue.push_ne({'alice': 1}))
        self.queue.destruct()
        self.assertEqual(self.queue.push_ne({'alice': 1}), 1)

    def test_push_ni(self):
        self.assertEqual(self.queue.push_ni('alice', 1), (1, True))
        self.assertEqual(self.queue.push_ni('bob', 2), (2, True))
        self.assertEqual(self.queue.push_ni('alice', 1), (2, False))
        self.assertEqual(self.queue.push_ni('bob', 2), (2, False))
        self.assertEqual(self.queue.push_ni('cath', 3), (3, True))
        self.assertEqual(self.queue.push_ni('cath', 3), 'err_qf')
        self.assertEqual(self.queue.push_ni('dick', 3), 'err_qf')


class TestOfCappedPriorityQueue(TestCappedPriorityQueue):
    def setUp(self):
        self.queue = OfCappedPriorityQueue("fastrp_of_capped_priority_queue", 3)
        self.queue.destruct()
    
    def test_push_pop(self):
        p = self.queue.push({
            'cath': 3,
            'dylon': 4,
        })
        self.assertEqual(p, (2, []))
        self.assertEqual(self.queue.push({'alice': 1, 'bob': 2}), (3, [('dylon', 4)]))
        self.assertEqual(self.queue.push({'cathe': 0}), (3, [('cath', 3)]))

    def test_push_e(self):
        self.assertFalse(self.queue.push_ae({'alice': 1}))
        self.queue.push({'alice': 1})
        self.assertEqual(self.queue.push_ae({'bob': 2}), (2, []))
        self.assertFalse(self.queue.push_ne({'alice': 1}))

    def test_push_ni(self):
        self.assertEqual(self.queue.push_ni('alice', 1), (1, [], True))
        self.assertEqual(self.queue.push_ni('bob', 2), (2, [], True))
        self.assertEqual(self.queue.push_ni('alice', 1), (2, [],  False))
        self.assertEqual(self.queue.push_ni('bob', 2), (2, [], False))
        self.assertEqual(self.queue.push_ni('cath', 3), (3, [], True))
        self.assertEqual(self.queue.push_ni('dick', 0), (3, [('cath', 3)], True))
        self.assertEqual(self.queue.push_ni('ed', 5), (3, [], False))
        self.assertEqual(self.queue.push_ni('ed', 1), (3, [('bob', 2)], True))

