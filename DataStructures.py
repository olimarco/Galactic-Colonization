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
    

class DisjointSet:
    def __init__(self, max_size):
        self.parent = HashTable(max_size)
        self.rank = HashTable(max_size)

    def make_set(self, representative):
        if not self.parent.contains(representative):
            self.parent.put(representative, representative)
            self.rank.put(representative, 0)

    def find_set(self, representative):
        curr_parent = self.parent.get(representative)
        if curr_parent != representative:
            root = self.find_set(curr_parent)
            self.parent.put(representative, root)
            return root
        return representative
    
    def union(self, repr1, repr2):
        root1 = self.find_set(repr1)
        root2 = self.find_set(repr2)
        if root1 == root2:
            return
        rank1 = self.rank.get(root1)
        rank2 = self.rank.get(root2)
        if rank1 >= rank2:
            self.parent.put(root2, root1)
            if rank1 == rank2:
                self.rank.put(root1, rank1 + 1)
        else:
            self.parent.put(root1, root2)
    

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
            temp = self.A.get(i)
            self.A.set(i, self.A.get(smallest))
            self.A.set(smallest, temp)
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
            temp = self.A.get(i)
            self.A.set(i, self.A.get(parent))
            self.A.set(parent, temp)
            i = parent

    def insert(self, x, k):
        if self.size == self.A.length():
            raise OverflowError("La coda di priorità è piena")
        new_node = HeapNode(x, float("inf"))
        self.A.set(self.size, new_node)
        new_index = self.size
        self.size += 1
        self.decrease_key(new_index, k)


class HashEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class HashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buckets = Array(capacity)
        for i in range(capacity):
            self.buckets.set(i, LinkedList())
        self.size = 0

    def hash(self, key):
        key = str(key)
        hash_value = 0
        multiplier = 31
        for char in key:
            hash_value = (hash_value * multiplier) + ord(char)
        return hash_value % self.capacity

    def search_entry(self, key):
        index = self.hash(key)
        bucket = self.buckets.get(index)
        current = bucket.head
        while current != None:
            if current.data.key == key:
                return current.data
            current = current.next
        return None
    
    def put(self, key, value):
        is_entry = self.search_entry(key)
        if is_entry != None:
            is_entry.value = value
        else:
            index = self.hash(key)
            self.buckets.get(index).add(HashEntry(key, value))
            self.size += 1
    
    def get(self, key):
        entry = self.search_entry(key)
        if entry != None:
            return entry.value
        return None
    
    def contains(self, key):
        return self.search_entry(key) != None


class Edge:
    def __init__(self, destination, weight):
        self.destination = destination
        self.weight = weight


class Graph:
    def __init__(self, capacity):
        self.adjacency_list = HashTable(capacity)
        self.all_vertices = LinkedList()
    
    def add_vertex(self, vertex):
        if not self.adjacency_list.contains(vertex):
            self.adjacency_list.put(vertex, LinkedList())
            self.all_vertices.add(vertex)

    def add_edge(self, source, destination, weight):
        self.add_vertex(source)
        self.add_vertex(destination)
        source_edges = self.adjacency_list.get(source)
        new_edge = Edge(destination, weight)
        source_edges.add(new_edge)

    def get_adjacent_vertices(self, vertex):
        if not self.adjacency_list.contains(vertex):
            return None
        return self.adjacency_list.get(vertex)
    
    def get_vertices(self):
        return self.all_vertices