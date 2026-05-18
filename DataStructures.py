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
