import time
import unittest

from fastrq.deque import Deque, CappedDeque, OfCappedDeque


class TestDeque(unittest.TestCase):
    def setUp(self):
        self.queue = Deque("fastrq_deque")
        self.queue.destruct()
    
    def tearDown(self):
        self.queue.destruct()
    
    def test_push_pop(self):
        ql = self.queue.push_back((1, 2))
        self.assertEqual(ql, 2)
        self.assertEqual(self.queue.length(), 2)
        head = self.queue.pop_front()
        self.assertEqual(head, '1')
        self.assertEqual(self.queue.length(), 1)
        self.assertEqual(len(self.queue), 1)
        
        self.queue.push_front((3, 4, 5, 6, 7))
        head3 = self.queue.pop_front(3)
        self.assertEqual(head3, ['7', '6', '5'])
        self.assertEqual(self.queue.pop_back(3), ['2', '3', '4'])
        self.assertEqual(self.queue.pop_back(), None)

    def test_push_e(self):
        self.assertEqual(self.queue.push_front_ne(1), 1)
        self.assertFalse(self.queue.push_back_ne(1))
        self.queue.destruct()
        self.assertFalse(self.queue.push_front_ae(1))
        self.queue.push_front(1)
        self.assertEqual(self.queue.push_front_ae(1), 2)

    def test_push_ni(self):
        self.assertEqual(self.queue.push_back_ni(1), [1, True])
        self.assertEqual(self.queue.push_back_ni(2), [2, True])
        self.assertEqual(self.queue.push_back_ni(4), [3, True])
        self.assertEqual(self.queue.push_back_ni(4), [3, False])
        self.assertEqual(self.queue.push_back_ni('apple'), [4, True])
        self.assertEqual(self.queue.pop_front(), '1')
        self.assertEqual(self.queue.pop_back(), 'apple')
    
    def test_range(self):
        self.queue.push_back((1, 2, 3, 4))
        self.assertEqual(self.queue.range(0, -1), ['1', '2', '3', '4'])
        self.assertEqual(self.queue.range(0, 2), ['1', '2', '3'])
        self.assertEqual(self.queue.range(0, 0), ['1'])
        self.queue.destruct()
        self.assertEqual(self.queue.range(0, -1), [])
    
    def test_expire(self):
        self.queue.push_back((1, 2))
        self.assertEqual(self.queue.ttl(), -1)
        self.queue.expire(10)
        self.assertEqual(self.queue.ttl(), 10)
        time.sleep(11)
        self.assertEqual(self.queue.ttl(), -2)


class TestCappedDeque(unittest.TestCase):
    def setUp(self):
        self.queue = CappedDeque("fastrq_capped_deque", 3)
        self.queue.destruct()
    
    def tearDown(self):
        self.queue.destruct()
    
    def test_push(self):
        self.queue.push_back([1, 2])
        self.queue.push_front(3)
        self.assertEqual(self.queue.range(0, -1), ['3', '1', '2'])
        self.assertEqual(self.queue.push_back(4), 'err_qf')

    def test_push_e(self):
        self.assertEqual(self.queue.push_front_ne(1), 1)
        self.assertFalse(self.queue.push_back_ne(1))
        self.queue.destruct()
        self.assertFalse(self.queue.push_front_ae(1))
        self.queue.push_front(1)
        self.assertEqual(self.queue.push_front_ae(1), 2)

    def test_push_ni(self):
        self.assertEqual(self.queue.push_back_ni(1), [1, True])
        self.assertEqual(self.queue.push_back_ni(1), [1, False])
        self.assertEqual(self.queue.push_front_ni(2), [2, True])
        self.assertEqual(self.queue.push_front_ni(2), [2, False])
        self.assertEqual(self.queue.push_back_ni(3), [3, True])
        self.assertEqual(self.queue.push_back_ni(3), 'err_qf')
        self.assertEqual(self.queue.push_back_ni(4), 'err_qf')
        self.assertEqual(self.queue.pop_front(), '2')
        self.assertEqual(self.queue.pop_back(), '3')


class TestOfCappedDeque(unittest.TestCase):
    def setUp(self):
        self.queue = OfCappedDeque("fastrq_of_capped_deque", 3)
        self.queue.destruct()
    
    def tearDown(self):
        self.queue.destruct()
    
    def test_push(self):
        self.assertEqual(self.queue.push_back([1, 2]), [2, []])
        self.assertEqual(self.queue.push_front(3), [3, []])
        self.assertEqual(self.queue.push_back(4), [3, ['3']])
        self.assertEqual(self.queue.pop_front(), '1')
        self.assertEqual(self.queue.pop_back(), '4')

    def test_push_e(self):
        self.assertEqual(self.queue.push_front_ne(1), [1, []])
        self.assertFalse(self.queue.push_back_ne(1))
        self.queue.destruct()
        self.assertFalse(self.queue.push_front_ae(1))
        self.queue.push_front(1)
        self.assertEqual(self.queue.push_front_ae(1), [2, []])

    def test_push_ni(self):
        self.assertEqual(self.queue.push_back_ni('apple'), [1, [], True])
        self.assertEqual(self.queue.push_back_ni('banana'), [2, [], True])
        self.assertEqual(self.queue.push_back_ni('banana'), [2, [], False])
        self.assertEqual(self.queue.push_front_ni('pear'), [3, [], True])
        self.assertEqual(self.queue.push_front_ni('pear'), [3, [], False])
        self.assertEqual(self.queue.push_front_ni('grape'), [3, ['banana'], True])
        self.assertEqual(self.queue.pop_front(), 'grape')
        self.assertEqual(self.queue.pop_back(), 'apple')
        

