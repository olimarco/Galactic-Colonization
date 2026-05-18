class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def add(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next != None:
                current = current.next
            current.next = new_node
        self.size += 1

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Indice fuori dai limiti")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data
    
    def contains(self, data):
        current = self.head
        while current != None:
            if current.data == data:
                return True
            current = current.next
        return False
        
    def size(self):
        return self.size    
    

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        
    def enqueue(self, item):
        new_node = Node(item)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        if not self.head:
            return None
        dequeued_item = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self.size -= 1
        return dequeued_item
        
    def is_empty(self):
        return self.size == 0
    

class HeapNode(Node):
    def __init__(self, data, priority):
        super().__init__(data)
        self.priority = priority


class Array:
    def __init__(self, size):
        self.size = size
        self.array = [None] * size

    def get(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Indice fuori dai limiti della memoria")
        return self.array[index]
    
    def set(self, index, value):
        if index < 0 or index >= self.size:
            raise IndexError("Indice fuori dai limiti della memoria")
        self.array[index] = value

    def length(self):
        return self.size
    

class MinPriorityQueue:
    def __init__(self, max_size):
        self.A = Array(max_size)
        self.size = 0
    
    def parent(self, i):
        return (i - 1) // 2
    
    def left(self, i):
        return 2 * i + 1
    
    def right(self, i):
        return 2 * i + 2
    
    def min_heapify(self, i):
        left = self.left(i)
        right = self.right(i)
        smallest = i
        if left < self.size and self.A.get(left).priority < self.A.get(smallest).priority:
            smallest = left
        if right < self.size and self.A.get(right).priority < self.A.get(smallest).priority:
            smallest = right
        if smallest != i:
            self.A.set(i, self.A.get(smallest))
            self.A.set(smallest, self.A.get(i))
            self.min_heapify(smallest)

    def minimum(self):
        if self.size == 0:
            return None
        return self.A.get(0)

    def extract_min(self):
        if self.size == 0:
            return None
        min_node = self.minimum()
        self.A.set(0, self.A.get(self.size - 1))
        self.A.set(self.size - 1, None)
        self.size -= 1
        if self.size > 0:
            self.min_heapify(0)
        return min_node.data
    
    def decrease_key(self, i, k):
        if k > self.A.get(i).priority:
            raise ValueError("La nuova priorità è maggiore di quella attuale")
        self.A.get(i).priority = k
        while i > 0 and self.A.get(self.parent(i)).priority > self.A.get(i).priority:
            parent = self.parent(i)
            self.A.set(i, self.A.get(parent))
            self.A.set(parent, self.A.get(i))
            i = parent