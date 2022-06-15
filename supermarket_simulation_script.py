
from random import randrange
import datetime
import time
import random


class Customer:
    """
    a single customer that moves through the supermarket

    Parameter
    -------
    states: possible states for a customer
    probs: Transition Matrix for states (calculated from Data)

    self.id: unique customer id for the day, assigned in Supermarket class
    self.current_state: current isle for customer, assigned in Supermarket
    self.active_cust: is Customer still in Supermarket. Start=True, Checked-out --> False
    current_time: timestamp at print statement
    """

    states = ['checkout', 'dairy', 'drinks', 'fruit', 'spices']
    probs = {'checkout': [0.0, 0.0, 0.0, 0.0, 0.0],
            'dairy': [0.3930326992947211, 0.0, 0.22248343663175893, 0.18935670014960462, 0.19512716392391535],
            'drinks': [0.5372599231754162, 0.02714468629961588, 0.0, 0.21895006402048656, 0.21664532650448143],
            'fruit': [0.5001952362358454, 0.23799297149550958, 0.13607965638422492, 0.0, 0.12573213588442014],
            'spices': [0.25199786893979753, 0.3231220031965903, 0.27277570591369205, 0.15210442194992008, 0.0]}

    def __init__(self, id, start_state, active_cust=True):
        self.id = id
        self.current_state = start_state
        self.active_cust = active_cust

    def next_state(self):
        self.current_state = random.choices(self.states, weights=self.probs[self.current_state])[0]
        if self.current_state == 'checkout':
            current_time = datetime.datetime.now().strftime('%H:%M:%S')
            self.active_cust = False
            print(f'{current_time}, Customer {self.id}, {self.current_state}')
    
    def __repr__(self):
        return f'Customer {self.id}, is at {self.current_state}'


class Supermarket:
    """
    a supermarket in a MCMC simulattion

    Parameter
    -------
    initial_states: start isle for new customer 
    initial_probs: Transition Matrix for initial states (calculated from Data)

    self.name: name of Supermarket object, assigned at Main function
    self.customers: list of Customer Objects
    self.run_time: running time
    self.duration: length of simulation, assigned at Main Function
    self.last_id : running customer id for the day
    self.closing_time: timestamp at closing time

    n_cust: number of new customers to add, random - range [0:5]
    id: next id to give to a new customer
    start_state: fist isle for new customer
    c : initiate new Customer Object
    current_time: timestamp at print statement
    """

    initial_states = ['fruit', 'dairy', 'spices', 'drinks']
    initial_probs =  [0.3069573006867722, 0.2782920274708868, 0.21887130486712453, 0.1958793669752165]

    def __init__(self, day, duration):
        self.name = day
        self.customers = []
        self.run_time = 0
        self.duration = duration
        self.closing_time = 0
        self.last_id = 1

    def new_cust(self, n_cust):
        for i in range(n_cust):
            start_state = random.choices(self.initial_states, weights=self.initial_probs)[0]
            c = Customer(self.last_id, start_state)
            self.customers.append(c)
            self.last_id = self.last_id + 1

    def new_state(self):
        for customer in self.customers:
            if customer.active_cust:
                customer.next_state()

    def print(self):
        for customer in self.customers:
            if customer.active_cust:
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                print(f'{current_time}, Customer {customer.id}, {customer.current_state}')

    def end(self):
        print('Dear Customers - The Supermarkert is about to close. please proceed to checkout')
        time.sleep(5)
        for customer in self.customers:
            if customer.active_cust:
                customer.current_state = 'checkout'
                customer.active_cust = False
                current_time = datetime.datetime.now().strftime('%H:%M:%S')
                self.closing_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'{current_time}, customer {customer.id}, {customer.current_state}')
        print(f'{current_time}: To the {self.last_id} customers that visited us today - Thank you for shopping at Doodle Supermarket')

    def __repr__(self):
        return f'Name: {self.name}, Closing time: {self.closing_time}. Total Number of customers: {self.last_id}'



# Main Function - initiates and runs Supermarket Object
def run_supermarket(name, duration):
    """
    Initiates a Supermarket object and itirates adding new customers and shuffeling their state. 
        "name" - object name (recommended to give name of day)
        "duration" - duration of time it runs in seconds

    Parameter
    -------
    day: initiated Supermarket Object
    day.run_time: object attribute (incremented run time)
    day.duration: object attribute (closing time = duration)
    n_cust: number of new customers, randomly chosen [0,5]

    day.new_state: object method (assigns new isle to customers in shop)
    day.new_cust: object method (initiates new customers)
    day.print: object method (prints state of active customers)
    day.end: object method (checks out customer before closing the shop)
    """
    
    day = Supermarket(name, duration)
    while day.run_time < day.duration:
        n_cust = randrange(1, 5)
        day.new_state()
        day.new_cust(n_cust)
        day.print()
        time.sleep(5)
        day.run_time = day.run_time + 10
    day.end()
    return day


#Create empty list for initiated Supermarket Objects
supermarkets = []

# activate Main function (give: "object name" ** recomended day_name, "duration of runing time")
if __name__ == '__main__':
    record = run_supermarket('friday', 30)
    supermarkets.append(record)

# print initiated Supermarket Objects
for supermarket in supermarkets:
    print(supermarket)
