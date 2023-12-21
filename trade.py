import time, math, random
from collections import OrderedDict
import itertools

class Account:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def update_balance(self, amount):
        self.balance += amount

class Transaction:
    def __init__(self, from_account, to_account, amount, fee):
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount
        self.fee = fee

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


def maximize_transactions_fee(accounts, transactions):
    max_fee = 0
    best_sequence = []
    cache = LRUCache(capacity=10000) 
 
    def get_account_balances():
        return tuple(account.balance for account in accounts.values())

    def get_potential_max_fee(idx, total_fee):
        return total_fee + sum(txn.fee for txn in transactions[idx:])

    def dfs(idx, total_fee, current_sequence):
        nonlocal max_fee, best_sequence

        state = (idx, get_account_balances())
        cached_fee = cache.get(state)
        if cached_fee is not None:
            return cached_fee

        if idx == len(transactions) or get_potential_max_fee(idx, total_fee) <= max_fee:
            if total_fee > max_fee:
                max_fee = total_fee
                best_sequence = list(current_sequence)
            return total_fee
        
        from_account = transactions[idx].from_account
        to_account = transactions[idx].to_account
        amount = transactions[idx].amount
        fee = transactions[idx].fee

        if from_account.balance >= amount + fee:
            from_account.update_balance(-amount-fee)
            to_account.update_balance(amount)
            current_sequence.append(transactions[idx])
            dfs(idx+1, total_fee+fee, current_sequence)
            current_sequence.pop()
            from_account.update_balance(amount+fee)
            to_account.update_balance(-amount)

        dfs(idx+1, total_fee, current_sequence)

        cache.put(state, max_fee)
        return max_fee
    
    dfs(0, 0, [])
    return max_fee, best_sequence


def maximize_system_fee(accounts, transactions_seq):    
    total_permutations = math.factorial(len(transactions_seq))

    if total_permutations > 1000:
        all_combinations = random.sample(list(itertools.permutations(transactions_seq)), 1000)
    else:
        all_combinations = itertools.permutations(transactions_seq)

    overall_max_fee = 0
    overall_best_sequence = None

    for combination in all_combinations:
        
        merged = [item for sublist in combination for item in sublist]

        max_fee, best_sequence = maximize_transactions_fee(accounts, merged)
        if max_fee > overall_max_fee:
            overall_max_fee = max_fee
            overall_best_sequence = best_sequence

    print(overall_max_fee)
    for txn in overall_best_sequence:
        print(f"Transaction: {txn.from_account.name} -> {txn.to_account.name}, Amount: {txn.amount}, Fee: {txn.fee}")
        

def test_maximize_fee(test_accounts, test_transactions_seq):
    start_time = time.time() 
    maximize_system_fee(test_accounts, test_transactions_seq)
    end_time = time.time() 

    duration = end_time - start_time 
    return duration


accounts = {
    "Alice": Account("Alice", 110),
    "Bob": Account("Bob", 5),
    "Charlie": Account("Charlie", 2)
}
transactions_seq = [
    [   
        Transaction(accounts["Alice"], accounts["Bob"], 12, 100)
    ],
    [
        Transaction(accounts["Charlie"], accounts["Alice"], 2, 0),
        Transaction(accounts["Alice"], accounts["Bob"], 5, 1)
    ],
]

duration = test_maximize_fee(accounts, transactions_seq)
print(f"Duration: {duration} seconds")


accounts = {
    "Alice": Account("Alice", 1500),
    "Bob": Account("Bob", 1200),
    "Charlie": Account("Charlie", 1000),
    "Dave": Account("Dave", 800),
    "Eve": Account("Eve", 500),
    "Frank": Account("Frank", 300),
    "Grace": Account("Grace", 100)
}

transactions_seq = [
    [
        Transaction(accounts["Alice"], accounts["Bob"], 100, 10),
        Transaction(accounts["Bob"], accounts["Charlie"], 120, 12),
        Transaction(accounts["Charlie"], accounts["Alice"], 140, 14),
        Transaction(accounts["Alice"], accounts["Dave"], 160, 16)
    ],
    [
        Transaction(accounts["Dave"], accounts["Eve"], 180, 18),
        Transaction(accounts["Eve"], accounts["Frank"], 200, 20),
        Transaction(accounts["Frank"], accounts["Grace"], 220, 22),
        Transaction(accounts["Grace"], accounts["Charlie"], 240, 24)
    ],
    [
        Transaction(accounts["Charlie"], accounts["Bob"], 260, 26),
        Transaction(accounts["Bob"], accounts["Dave"], 280, 28),
        Transaction(accounts["Dave"], accounts["Eve"], 300, 30),
        Transaction(accounts["Eve"], accounts["Alice"], 320, 32)
    ],
    [
        Transaction(accounts["Alice"], accounts["Frank"], 340, 34),
        Transaction(accounts["Frank"], accounts["Grace"], 360, 36),
        Transaction(accounts["Grace"], accounts["Dave"], 380, 38),
        Transaction(accounts["Dave"], accounts["Charlie"], 400, 40)
    ],
    [
        Transaction(accounts["Charlie"], accounts["Eve"], 420, 42),
        Transaction(accounts["Eve"], accounts["Bob"], 440, 44),
        Transaction(accounts["Bob"], accounts["Alice"], 460, 46),
        Transaction(accounts["Alice"], accounts["Grace"], 480, 48)
    ]
]

duration = test_maximize_fee(accounts, transactions_seq)
print(f"Duration: {duration} seconds")
