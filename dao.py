from databaseConnection import DB
from customer import Customer
db=DB()
def get_customer(customer_id):
    return db.get_customer(customer_id)

def delete_customer(customer_id):
    return db.delete_customer(customer_id)

def update_customer(customer_name,credit):
    return db.update_customer_credit(customer_name,credit)

def add_new_customer(customer: Customer) -> bool:
    return db.add_customer(customer)