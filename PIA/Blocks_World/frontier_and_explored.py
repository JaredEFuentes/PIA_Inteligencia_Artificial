from collections import deque


# TODO : MAKE IT MORE CLEAR
class Frontier(object):

    def __init__(self):

        'FIFO'
        self.queue = deque()

        'PRIORITY QUEUE'
        self.heap = []
        
    def __contains__(self, item):

        # custom method compares only configs
        if self.queue:
            for element in self.queue:
                if tuple(map(tuple, item.config)) == element.config:
                    return True
        else:
            for element in self.heap:
                if item.config == element[1].config:
                    return True
        return False


class Explored(object):

    def __init__(self):
        self.set = set()
