# Fastrq - Queue, Stack and Priority Queue built on Redis

[![Build Status](https://travis-ci.org/limen/fastrq.svg?branch=master)](https://travis-ci.org/limen/fastrq)

[Wiki](https://github.com/limen/fastrq/wiki)

[Fastrq for PHP](https://github.com/limen/fastrq-php)

## Features

+ Abstract Queue, Deque, Capped Queue/Deque, and Overflow-able Capped Queue/Deque
+ Abstract Stack, Capped Stack
+ Abstract Priority Queue, Capped Priority Queue and Overflow-able Capped Priority Queue
+ Push and Pop support batch operation
+ Using Lua scripts to save RTT (Round Trip Time)
+ Support getting indexes of members 
+ Support pushing only if a member not already inside the queue
+ Support pushing only if the queue already exists/not already exist
+ All operations are `atomic`

## Requirements

- Redis >=3.0.2
- Python 2.7 or >=3.4

## Installation

via pip

```
pip install fastrq
```

or from source

```
python setup.py install
```

## Usage

```python
from fastrq.queue import Queue, CappedQueue
from fastrq.deque import Deque
from fastrq.stack import Stack
from fastrq.priorityqueue import PriorityQueue

# queue
q = Queue("fastrq_queue")
q.push(1)
q.push([2, 3])
q.push_ni(1) # got [3, False]. `ni` stands for `not inside`
q.push_ae(1) # got 4. `ae` stands for `already exists`
q.push_ne(1) # got False. `ne` stands for `not already exist`
q.ttl(10)   # set the lifetime in seconds
q.range(0, -1)  # got ['1', '2', '3']
q.range(0, 1)  # got ['1', '2']
q.indexof_one(1); # got 0
q.indexof_one(2); # got 1
q.indexof_one(4); # got None
q.indexof_many([1, 2, 4]); # got {1: 0, 2: 1, 4: None}
# push only if the member not inside the queue
q.push_ni(4) # got [4, True]
q.pop()
q.pop(2)
q.destruct() # destruct the queue
cq = CappedQueue("fastrq_capped_queue", 3)
cq.push(1)
cq.push(2)
cq.push([3, 4]) # got "err_qof"
cq.push(3)
cq.push(4) # got "err_qf"
of_cq = OfCappedQueue("fastrq_of_capped_queue", 3)
of_cq.push(1)
of_cq.push([2, 3, 4])  # "1" would be forced out


# deque
dq = Deque("fastrq_deque")
dq.push_front([1, 2])
dq.push_back([3, 4])
dq.pop_front()
dq.pop_back()
dq.push_front_ni(3)
dq.push_back_ni(5)

# priority queue
pq = PriorityQueue("fastrq_priority_queue")
pq.push({'alibaba': 1})
pq.push({'google': 0, 'microsoft': 2})
pq.indexof_one('google'); # got 0
pq.indexof_one('alibaba'); # got 1
pq.indexof_one('baidu'); # got None
pq.pop()
pq.pop(2)
pq.push_ni('ibm', 4)
pq.push_ni('amazon', 5)

# stack
s = Stack("fastrq_stack")
s.push([1,2,3])
s.indexof_one(1); # got 2
s.indexof_one(2); # got 1
s.indexof_one(3); # got 0
s.pop()
s.push_ni(4)

```

## Data types

### Queue

+ first in and first out
+ unlimited capacity
+ support batch push and batch pop

### Deque

Derive from queue with more features

+ support push front and push back
+ support pop front and pop back

### Capped Queue/Deque

Derive from queue/deque with more features

+ Have fixed capacity
+ Push to a full one would fail
+ Push to one whose positions are not enough would fail

### Overflow-able Capped Queue/Deque

Derive from capped queue/deque with more features

+ The queue length would never exceed its capacity
+ Push to an end would force out from the other end if one is full

### Stack

+ Last in and First out
+ Unlimited capacity
+ Support batch push and batch pop

### Capped Stack

Derive from Stack with more features

+ Have fixed capacity
+ Push to a full capped stack would fail
+ Push to a capped stack whose positions are not enough would fail

### Priority Queue

+ The lower the score, the higher the priority
+ Unlimited capacity
+ Support batch push and batch pop

### Capped Priority Queue

Derive from Priority Queue with more features

+ Have fixed capacity
+ Push to a full one would fail
+ Push to a capped one whose positions are not enough would fail

### Overflow-able Capped Priority Queue

Derive from Capped Priority Queue with more features

+ The queue length would never exceed its capacity
+ Push to would force out the lowest priority if queue is full
