
import heapq

class queue(object):
    def __init__(self, list=None):
        if list:
            self.list = heapq.heapify(list)
        else:
            self.list = []
            
    def push(self, item):
        heapq.heappush(self.list, item)
        
    def pop(self):
        if self.list:
            return heapq.heappop(self.list)
        else:
            return None
            
    def peak(self):
        if self.list:
            return self.list[0]
        else:
            return None
            
    def __len__(self):
        return len(self.list)
        
    def __repr__(self):
        return 'queue(%s)' % self.list
