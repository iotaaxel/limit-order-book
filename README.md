# limit-order-book

# Option 1: 

A limit order book is a data structure used in financial markets to manage buy and sell orders. It is a priority queue where orders are sorted by price and then by time. The implementation of a limit order book in Python, considering the time in force.

# Example usage
```
order_book = LimitOrderBook()
```

# Add orders
```
order_book.add_order(Order(1, OrderType.BUY, 100, 10, timedelta(minutes=5)))
order_book.add_order(Order(2, OrderType.SELL, 120, 5, timedelta(minutes=5)))
order_book.add_order(Order(3, OrderType.BUY, 110, 8, timedelta(minutes=5)))
order_book.add_order(Order(4, OrderType.SELL, 130, 12, timedelta(minutes=5)))
```

# Match orders
```
order_book.match_orders()
```

# Expire orders
```
order_book.expire_orders()
```

This implementation includes the following features:

Order class: Represents a single order with attributes for order ID, order type (buy or sell), price, quantity, time in-force, and timestamp.
LimitOrderBook class: Manages the buy and sell orders using two priority queues (implemented using heapq).
add_order method: Adds a new order to the order book.
cancel_order method: Cancels an existing order by order ID and order type.
match_orders method: Matches buy and sell orders based on price and executes trades.
expire_orders method: Removes orders that have exceeded their time in-force.
Note that this is a simplified example and a real-world limit order book would require more features, such as handling multiple order types, managing order priority, and ensuring thread safety for concurrent access.


# Option 2: 

Building a limit order book in Python involves creating a data structure to store and manage limit orders. A limit order book is a list of buy and sell orders, sorted by price, that are waiting to be executed. The time in-force (TIF) of an order determines how long the order remains in the order book before it is automatically canceled.

Here is a basic implementation of a limit order book in Python, considering the time in-force:

import heapq
import time

class Order:
    def __init__(self, side, price, quantity, tif):
        self.side = side
        self.price = price
        self.quantity = quantity
        self.tif = tif
        self.timestamp = time.time()

    def __lt__(self, other):
        return self.price < other.price

class LimitOrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.side == 'buy':
            heapq.heappush(self.buy_orders, order)
        else:
            heapq.heappush(self.sell_orders, order)

    def cancel_order(self, order):
        if order.side == 'buy':
            self.buy_orders.remove(order)
            heapq.heapify(self.buy_orders)
        else:
            self.sell_orders.remove(order)
            heapq.heapify(self.sell_orders)

    def execute_orders(self):
        while self.buy_orders and self.sell_orders:
            buy_order = self.buy_orders[0]
            sell_order = self.sell_orders[0]
            if buy_order.price >= sell_order.price:
                # Execute the trade
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity
                if buy_order.quantity == 0:
                    heapq.heappop(self.buy_orders)
                if sell_order.quantity == 0:
                    heapq.heappop(self.sell_orders)
            else:
                break

    def check_tif(self):
        current_time = time.time()
        for order in self.buy_orders + self.sell_orders:
            if order.tif == 'GTC' and current_time - order.timestamp > 86400:
                # Cancel the order if it's been in the book for more than 24 hours
                self.cancel_order(order)
            elif order.tif == 'IOC' and current_time - order.timestamp > 60:
                # Cancel the order if it's been in the book for more than 1 minute
                self.cancel_order(order)

# Example usage
lob = LimitOrderBook()

# Add some orders
lob.add_order(Order('buy', 100, 10, 'GTC'))
lob.add_order(Order('sell', 120, 5, 'IOC'))
lob.add_order(Order('buy', 110, 8, 'GTC'))
lob.add_order(Order('sell', 130, 3, 'IOC'))

# Execute orders
lob.execute_orders()

# Check time in-force
lob.check_tif()
This implementation uses two heaps to store the buy and sell orders, sorted by price. The add_order method adds a new order to the book, the cancel_order method removes an order from the book, and the execute_orders method executes trades by matching buy and sell orders. The check_tif method checks the time in-force of each order and cancels it if it has expired.

The Order class represents a single order, with attributes for the side (buy or sell), price, quantity, time in-force, and timestamp. The LimitOrderBook class represents the limit order book, with methods for adding, canceling, and executing orders, as well as checking the time in-force.

Note that this is a simplified example and a real-world limit order book would require more features, such as handling multiple order types, managing order priority, and dealing with edge cases.
