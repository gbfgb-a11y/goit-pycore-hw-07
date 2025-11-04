from collections import UserDict
from datetime import datetime, timedelta

class Field:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):

    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("Phone must be a string")
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)


    def __eq__(self, other):
        return isinstance(other, Phone) and self.value == other.value
    
class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y').date()
            
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    def add_birthday(self, date):
        date_indatetime = Birthday(date)
        if date_indatetime != None:
            self.birthday = date_indatetime
        b=Birthday
    def add_phone(self, phone):
        if isinstance(phone, Phone):
            phone = phone.value
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if isinstance(phone, Phone):
            phone = phone.value
        isornot2 = self.find_phone(phone)
        if isornot2 is not None:
            self.phones.remove(isornot2)
        else:
            raise ValueError('Phone does not exist.')
        

    def edit_phone(self, old_phone, new_phone):
        if isinstance(old_phone, Phone):
            old_phonephone = old_phone.value
        if isinstance(new_phone, Phone):
            new_phonephone = new_phone.value
        if new_phone and old_phone:
            for i, a in enumerate(self.phones):
                if a.value == old_phone:
                    self.remove_phone(old_phone)
                    self.add_phone(new_phone)
        else:
            raise ValueError('Phone does not anwer requirements.')

    def find_phone(self, phone):
        if isinstance(phone, Phone):
            phone = phone.value
        for i in self.phones:
            if i.value == phone:
                return i
        return None
    

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}, birthday_date: {self.birthday}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for name, record in self.data.items():
            if isinstance(record.birthday, Birthday):
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days
                if 0 <= delta_days <= 7:
                    congratulation_date = birthday_this_year
                    if congratulation_date.weekday() == 5:      
                        congratulation_date += timedelta(days=2)
                    elif congratulation_date.weekday() == 6:    
                        congratulation_date += timedelta(days=1)
                    bw1 = congratulation_date.weekday()+1
                    bw0 = ''
                    if bw1 == 1:
                        bw0 = 'Monday'
                    if bw1 == 2:
                        bw0 = 'Tuesday'
                    if bw1 == 3:
                        bw0 = 'Wednesday'
                    if bw1 == 4:
                        bw0 = 'Thursday'
                    if bw1 == 5:
                        bw0 = 'Friday'
                    if bw1 == 6:
                        bw0 = 'Saturday'
                    if bw1 == 7:
                        bw0 = 'Sunday'
                    upcoming_birthdays.append({
                        "name": name,
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                        "weekday": bw0
                    })
                    return upcoming_birthdays
                else:
                    return 'No birthdays next 7 days.'
# Створення нової адресної книги

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday('05.11.2000')
john_record.edit_phone('5555555555', '0987654321')
# Додавання запису John до адресної книги
book = AddressBook()
book.add_record(john_record)
print(book.get_upcoming_birthdays())

