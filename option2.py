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
