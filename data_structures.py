# contains code for data structures used in the project


class WrapperStack:

    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return str(self._items)

    def push(self,ele):
        self._items.append(ele)

    def pop(self):
        if len(self._items) == 0:
            raise AssertionError('Stack is empty')
        item = self._items.pop()
        return item

    def top(self):
        if len(self._items) == 0:
            raise AssertionError('Stack is empty')
        return self._items[-1]

    def isEmpty(self):
        if len(self._items) == 0:
            return True
        else:
            return False

class WrapperQueue:

    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return str(self._items)

    def enqueue(self,ele):
        self._items.append(ele)

    def dequeue(self):
        if len(self._items)==0:
            print('Queue is empty')
        item = self._items.pop(0)
        return item

    def front(self):
        return self._items[0]

    def rear(self):
        return self._items[-1]

    def isEmpty(self):
        if len(self)==0:
            return True
        else:
            return False
        
class PQueue:

    ''' Priority Queue '''
    
    def __init__(self):
        self._hpq = WrapperQueue()
        self._lpq = WrapperQueue()

    def isEmpty(self):
        if self._hpq.isEmpty() and self._lpq.isEmpty():
            return True

    def enqueue(self, qno, item):
        if qno == 0:
            self._hpq.enqueue(item)
        elif qno == 1:
            self._lpq.enqueue(item)
        else:
            print('Queue priority invalid')

    def dequeue(self):
        if not self._hpq.isEmpty():
            return self._hpq.dequeue()
        elif not self._lpq.isEmpty():
            return self._lpq.dequeue()
        
        else:
            print('Queue is Empty, cannot dequeue')

    def front(self, qno):
        if qno==0:
            return self._hpq.front()
        elif qno==1:
            return self._lpq.front()
        else:
            return 'Queue priority invalid'

    def rear(self, qno):
        if qno==0:
            return self._hpq.rear()
        elif qno==1:
            return self._lpq.rear()
        else:
            return 'Queue priority invalid'
