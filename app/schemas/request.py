class RbBuyer:

    def __init__(self, buyer_id: int | None = None,
                 phone_number: str | None = None,
                 ):
        self.id = buyer_id
        self.phone_number = phone_number

    def to_dict(self) -> dict:
        data = {'id': self.id, 'phone_number': self.phone_number}

        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if
                         value is not None}
        return filtered_data


class RbProduct:

    def __init__(self, product_id: int | None = None,
                 name: str | None = None,
                 ):
        self.id = product_id
        self.name = name

    def to_dict(self) -> dict:
        data = {'id': self.id, 'name': self.name}

        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if
                         value is not None}
        return filtered_data
