class Customer:
    def __init__(self, customer_id, customer_name, password, credit):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.password = password
        self.credit = credit
    def __dict__(self):
        return {
            
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'password': self.password,
            'credit': self.credit,
        }

    def __str__(self):
        return f'User->{self.__dict__()}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.customer_id == other
        elif isinstance(other,Customer):
            return self.customer_id == other.customer_id
        else:
            return False

    def __ne__(self, other):
        return not self == other

    
