from fastrq.queue import Queue
from fastrq.deque import Deque

q = Queue('bank_counter')
print(q.getkey())

dq = Deque('game_line')
print(dq.getkey())

