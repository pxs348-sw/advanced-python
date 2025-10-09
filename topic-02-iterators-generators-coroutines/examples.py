class CountDown:
    def __init__(self, start):
        self.start = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

countdown = CountDown(3)
for num in countdown:
    print(num)

countdown2 = CountDown(2)
iterator = iter(countdown2)
print(next(iterator))  # 2
print(next(iterator))  # 1
# print(next(iterator))  # Would raise StopIteration

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    
    def __iter__(self):
        return TreeIterator(self)

class TreeIterator:
    def __init__(self, root):
        self.stack = [root] if root else []
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.stack:
            raise StopIteration
        
        node = self.stack.pop()
        
        # Add children to stack (right first for left-to-right traversal)
        if node.right:
            self.stack.append(node.right)
        if node.left:
            self.stack.append(node.left)
        
        return node.value

root = TreeNode(1, 
                TreeNode(2, TreeNode(4), TreeNode(5)), 
                TreeNode(3, TreeNode(6), TreeNode(7)))

for value in root:
    print(value)

class PagedData:
    def __init__(self, data, page_size=3):
        self.data = data
        self.page_size = page_size
    
    def __iter__(self):
        return PageIterator(self.data, self.page_size)

class PageIterator:
    def __init__(self, data, page_size):
        self.data = data
        self.page_size = page_size
        self.current_page = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        start = self.current_page * self.page_size
        end = start + self.page_size
        
        if start >= len(self.data):
            raise StopIteration
        
        page = self.data[start:end]
        self.current_page += 1
        return page


data = list(range(10))
paged = PagedData(data, page_size=3)

for page in paged:
    print(f"Page: {page}")

# Well, that was fun, but... 

print("using generators")

def countdown_generator(start):
    while start > 0:
        yield start
        start -= 1

for num in countdown_generator(3):
    print(num)  # Prints: 3, 2, 1

def fibonacci_generator(limit):
    """Generate Fibonacci sequence up to limit."""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

fib_nums = list(fibonacci_generator(20))
print(fib_nums)

squares_gen = (x**2 for x in range(10))
print(type(squares_gen))  # <class 'generator'>

large_dataset = range(1000000)
filtered_data = (x for x in large_dataset if x % 1000 == 0)
squared_filtered = (x**2 for x in filtered_data)

first_five = [next(squared_filtered) for _ in range(5)]
print(first_five)  # [0, 1000000, 4000000, 9000000, 16000000]

def running_average():
    """Generator that maintains running average of sent values."""
    total = 0
    count = 0
    
    while True:
        value = yield total / count if count > 0 else 0
        if value is not None:
            total += value
            count += 1

avg_gen = running_average()
next(avg_gen)  # Prime the generator

print(avg_gen.send(10))  # 10.0
print(avg_gen.send(20))  # 15.0
print(avg_gen.send(30))  # 20.0

def inner_generator():
    yield 1
    yield 2
    yield 3

def outer_generator():
    yield "start"
    yield from inner_generator()
    yield "end"

for i in outer_generator():
    print(i)

class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []
    
    def traverse(self):
        """Generator for depth-first traversal."""
        yield self.value
        for child in self.children:
            yield from child.traverse()

root = TreeNode('A', [
    TreeNode('B', [TreeNode('D'), TreeNode('E')]),
    TreeNode('C', [TreeNode('F')])
])

for node_value in root.traverse():
    print(node_value)  # Prints: A, B, D, E, C, F

def flatten(nested_list):
    """Recursively flatten nested lists using yield from."""
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, 3], [4, [5, 6]], 7]
flat = list(flatten(nested))
print(flat)  # [1, 2, 3, 4, 5, 6, 7]

def read_files(*filenames):
    """Generator that reads multiple files sequentially."""
    for filename in filenames:
        try:
            with open(filename, 'r') as file:
                yield from file
        except FileNotFoundError:
            print(f"Warning: {filename} not found")

# Usage (if files existed)
# for line in read_files('file1.txt', 'file2.txt', 'file3.txt'):
#     print(line.strip())

def data_processor():
    """Coroutine that processes incoming data."""
    processed_count = 0
    
    while True:
        data = yield processed_count
        if data is not None:
            # Process the data
            processed_data = data.upper() if isinstance(data, str) else str(data)
            print(f"Processed: {processed_data}")
            processed_count += 1

# Usage
processor = data_processor()
next(processor)  # Prime the coroutine

processor.send("hello")      # Processed: HELLO
processor.send("world")      # Processed: WORLD
count = processor.send(42)   # Processed: 42
print(f"Total processed: {count}")  # Total processed: 3

def logger(target=None):
    """Coroutine that logs messages and forwards them."""
    while True:
        message = yield
        print(f"LOG: {message}")
        if target:
            target.send(message)

def validator(target=None):
    """Coroutine that validates data and forwards valid items."""
    while True:
        data = yield
        if data and len(str(data)) > 2:  # Simple validation
            print(f"VALID: {data}")
            if target:
                target.send(data)
        else:
            print(f"INVALID: {data}")

def database_writer():
    """Coroutine that simulates writing to database."""
    while True:
        data = yield
        print(f"SAVED TO DB: {data}")

db_writer = database_writer()
next(db_writer)

validator_stage = validator(db_writer)
next(validator_stage)

log_stage = logger(validator_stage)
next(log_stage)

log_stage.send("hello")     # LOG -> VALID -> SAVED
log_stage.send("hi")        # LOG -> INVALID (too short)
log_stage.send("python")    # LOG -> VALID -> SAVED

# CSV pipeline

def csv_reader(filename):
    """Generator that reads CSV file line by line."""
    import csv
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row

def data_transformer(data_stream):
    """Generator that transforms data as it flows through."""
    for record in data_stream:
        # Transform the data
        if 'price' in record:
            record['price'] = float(record['price'])
        if 'date' in record:
            # Simulate date parsing
            record['processed_date'] = f"parsed_{record['date']}"
        yield record

def data_filter(data_stream, min_price=0):
    """Generator that filters data based on criteria."""
    for record in data_stream:
        if record.get('price', 0) >= min_price:
            yield record

sample_data = [
    {'name': 'item1', 'price': '10.50', 'date': '2023-01-01'},
    {'name': 'item2', 'price': '5.00', 'date': '2023-01-02'},
    {'name': 'item3', 'price': '25.75', 'date': '2023-01-03'}
]

def mock_csv_reader():
    """Mock CSV reader for demonstration."""
    for row in sample_data:
        yield row

pipeline = data_filter(
    data_transformer(
        mock_csv_reader()), 
    min_price=10.0
)

for processed_record in pipeline:
    print(processed_record)

def state_machine():
    """Generator-based state machine for order processing."""
    state = 'pending'
    
    while True:
        action = yield state
        
        if state == 'pending':
            if action == 'pay':
                state = 'paid'
            elif action == 'cancel':
                state = 'cancelled'
        
        elif state == 'paid':
            if action == 'ship':
                state = 'shipped'
            elif action == 'refund':
                state = 'refunded'
        
        elif state == 'shipped':
            if action == 'deliver':
                state = 'delivered'
        
        # Terminal states: cancelled, refunded, delivered

# Usage
order = state_machine()
print(next(order))          # pending

print(order.send('pay'))    # paid
print(order.send('ship'))   # shipped
print(order.send('deliver')) # delivered
