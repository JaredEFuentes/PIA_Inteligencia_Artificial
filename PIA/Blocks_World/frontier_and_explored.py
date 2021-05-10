from collections import deque

class Frontier(object):

    def __init__(self):

        'FIFO'
        self.queue = deque()

        'PRIORITY QUEUE'
        self.heap = []
        
    def __contains__(self, item):

        # comparamos configs
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
