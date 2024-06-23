import heapq
from enum import Enum
from datetime import datetime, timedelta

class OrderType(Enum):
    BUY = 1
    SELL = 2

class Order:
    def __init__(self, order_id, order_type, price, quantity, time_in_force):
        self.order_id = order_id
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
        self.time_in_force = time_in_force
        self.timestamp = datetime.now()

    def __lt__(self, other):
        if self.price == other.price:
            return self.timestamp < other.timestamp
        elif self.order_type == OrderType.BUY:
            return self.price > other.price
        else:
            return self.price < other.price

class LimitOrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []

    def add_order(self, order):
        if order.order_type == OrderType.BUY:
            heapq.heappush(self.buy_orders, order)
        else:
            heapq.heappush(self.sell_orders, order)

    def cancel_order(self, order_id, order_type):
        if order_type == OrderType.BUY:
            self.buy_orders = [order for order in self.buy_orders if order.order_id != order_id]
            heapq.heapify(self.buy_orders)
        else:
            self.sell_orders = [order for order in self.sell_orders if order.order_id != order_id]
            heapq.heapify(self.sell_orders)

    def match_orders(self):
        while self.buy_orders and self.sell_orders:
            buy_order = self.buy_orders[0]
            sell_order = self.sell_orders[0]
            if buy_order.price >= sell_order.price:
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity
                print(f'Trade executed: {trade_quantity} at {buy_order.price}')
                if buy_order.quantity == 0:
                    heapq.heappop(self.buy_orders)
                if sell_order.quantity == 0:
                    heapq.heappop(self.sell_orders)
            else:
                break

    def expire_orders(self):
        current_time = datetime.now()
        self.buy_orders = [order for order in self.buy_orders if current_time - order.timestamp < order.time_in_force]
        heapq.heapify(self.buy_orders)
        self.sell_orders = [order for order in self.sell_orders if current_time - order.timestamp < order.time_in_force]
        heapq.heapify(self.sell_orders)
