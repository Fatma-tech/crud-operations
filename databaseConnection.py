
import mysql.connector
from customer import Customer
import mysql.connector
import logging
import json


def db_entry_to_customer(entry):
    return Customer(entry[0], entry[1], entry[2], entry[3])

# Database Creation in MySQL

def load_config():
    with open('config/config.json', 'r') as f:
        return json.load(f)

class DB:
    def __init__(self):
        conf = load_config()
        self.database = conf['database']
        self.master_node = conf['master_node']
        self.user = conf['user']
        self.passwd = conf['passwd']
        self.create_db_if_not_exits()
        self._connection = None
        self._cursor = None


        self.refresh_connection()

        self.create_customer_table_if_not_exists()


    def create_db_if_not_exits(self):
        connection = mysql.connector.connect(host=self.master_node, user=self.user, passwd=self.passwd)
        cursor = connection.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')

    def refresh_connection(self):
        self._connection = mysql.connector.connect(host=self.master_node,
                                                     user=self.user,
                                                     passwd=self.passwd,
                                                     database=self.database)
        self._cursor = self._connection.cursor()





    def create_customer_table_if_not_exists(self):
        self._cursor.execute(
            'CREATE TABLE IF NOT EXISTS customers  (customer_id int primary key not null,customer_name varchar(45)  not null, '
            'password varchar(45), credit int unsigned) '
            'PARTITION BY KEY(customer_id) PARTITIONS 4')
    def get_customer(self, customer_id):
        """
        return a valid customer object if there is customer with the same id, or None if not available
        :param customer_id:
        :return: valid customer on success or None otherwise
        """
        try:
            self._cursor.execute(f'SELECT * FROM customer WHERE customer_id=%s', (customer_id,))
            entry = self._cursor.fetchone()
            return db_entry_to_customer(entry)
        except Exception as e:
            logging.error(f'error while getting customer: {customer_id}, with error: {e}')
            return None

    def update_customer_credit(self, customer_name, credit):
        self._cursor.execute('UPDATE customer SET credit = %s WHERE customer_name=%s', (credit,customer_name))
        self._connection.commit()
        return "credit was updated in database"

    def delete_customer(self, customer_id) -> None:
        """
        deletes customer from the users table
        :param customer_id:
        :return:
        """
        try:
            self._cursor.execute('DELETE FROM customer WHERE customer_id=%s', (customer_id,))
            self._connection.commit()
            return "customer was deleted from database "
        except Exception as e:
            logging.error(f'Error while deleting: {customer_id}\nwith error: {e}')

    def add_customer(self, customer: Customer) -> bool:
        values = tuple(customer.__dict__().values())
        try:
            self._cursor.execute(f'INSERT INTO customer VALUES ('
                                   '%s, %s, %s, %s ) ', values)
            self._connection.commit()
            return "done"
        except Exception as e:
            logging.error(f'Error while adding customer: {e}')
            return " the id of customer repeated"


if __name__ == '__main__':

    db = DB()

