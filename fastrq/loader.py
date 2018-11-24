from os.path import dirname


_lua_path = dirname(__file__) + '/_lua_scripts'

_map = {
    # queue
    'queue_push': 'queue_push',
    'queue_pop': 'queue_pop',
    'capped_queue_push': 'capped_queue_push',
    'capped_queue_pop': 'capped_queue_pop',
    'of_capped_queue_push': 'of_capped_queue_push',
    'of_capped_queue_pop': 'of_capped_queue_pop',
    # deque
    'deque_push_back': 'queue_push',
    'deque_push_front': 'deque_push_front',
    'deque_pop_back': 'deque_pop_back',
    'deque_pop_front': 'queue_pop',
    'capped_deque_push_front': 'capped_deque_push_front',
    'capped_deque_push_back': 'capped_queue_push',
    'of_capped_deque_push_front': 'of_capped_deque_push_front',
    'of_capped_deque_push_back': 'of_capped_queue_push',
    'of_capped_deque_pop_front': 'queue_pop',
    'of_capped_deque_pop_back': 'deque_pop_back',
    # stack
    'stack_push': 'stack_push',
    'stack_pop': 'stack_pop',
    'capped_stack_push': 'capped_stack_push',
    'capped_stack_pop': 'stack_pop',
    # priority queue
    'priority_queue_push': 'priority_queue_push',
    'priority_queue_pop': 'priority_queue_pop',
    'capped_priority_queue_push': 'capped_priority_queue_push',
    'capped_priority_queue_pop': 'priority_queue_pop',
    'of_capped_priority_queue_push': 'of_capped_priority_queue_push',
}


def load(command):
    script = _map[command]
    with open('%s/%s.lua' % (_lua_path, script)) as f:
        lua = f.read()
    return lua
