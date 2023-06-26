from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value
    
    #перевірка на коректний номер телефону
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        new_value = (
            value.removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if len(new_value) <= 12 and new_value.isdigit():
            self.__value = new_value
        else:
            print("Please, check your phone number. It contain only digits.")


class Birthday(Field):
    def __init__(self, value):
        self.value = value
        self.__value = None

    def __repr__(self):
        return datetime.strftime(self.__value, '%d.%m.%Y')

    #перевірка на коректну дату дня народження
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        try:
            date_birthday = datetime.strptime(value, '%d.%m.%Y')
            self.__value = date_birthday
        except ValueError:
            print("Please, enter correct birthday in format DD.MM.YYYY")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday = None):
        self.name = name
        self.phones = []
        if isinstance(phone, Phone):
            self.phones.append(phone)
        if birthday:
            self.birthday = Birthday(birthday)    

    #додавання контакту
    def add_phone_num(self, phone):
        self.phones.append(phone)

    #видалення контакту
    def delete_phone_num(self, phone):
        for seq_num, i in enumerate(self.phones):
            if i == phone:
                self.phones.pop(seq_num)

    #редагування контакту
    def change_phone_num(self, old_phone, new_phone):
        for seq_num, i in enumerate(self.phones):
            if i == old_phone:
                self.phones[seq_num] = new_phone

    #днів до дня народження
    def days_to_birthday(self):
        date_now = datetime.now()
        date_birthday = datetime(year=date_now.year, month=self.month, day=self.day)
        if date_birthday.date() == date_now.date():
            return f'{self.name} has Birthday TODAY!!!'
        elif date_birthday < date_now:
            days_to_birth_day = (datetime(year=date_now.year + 1, month=self.month, day=self.day) - date_now).days
            return f'{self.name} will have Birthday on {days_to_birth_day} days'
        else:
            days_to_birth_day = (date_birthday - date_now).days
            return f'{self.name} will have Birthday on {days_to_birth_day+1} days'


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def iterator(self, n=2): 
        index = 1
        print_block = '-' * 50 + '\n'  
        for record in self.data.values(): 
            print_block += str(record) + '\n'
            if index < n: 
                index += 1
            else:
                yield print_block 
                index = 1
                print_block = '-' * 50 + '\n'
        yield print_block 

