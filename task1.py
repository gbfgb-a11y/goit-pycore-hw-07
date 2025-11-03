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
            self.dateb = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = 1
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
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record
        print(self.data)

    def find(self, name):
        return self.data.get(name)
    

    def delete(self, name):
        if name in self.data:
            del self.data[name]
    @property
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for name, record in self.data.items():
            if isinstance(record.birthday, Birthday):
                birthday_this_year = record.birthday.dateb.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                delta_days = (birthday_this_year - today).days
                if 0 <= delta_days <= 7:
                    congratulation_date = birthday_this_year
                    if congratulation_date.weekday() == 5:      # суббота
                        congratulation_date += timedelta(days=2)
                    elif congratulation_date.weekday() == 6:    # воскресенье
                        congratulation_date += timedelta(days=1)

                    upcoming_birthdays.append({
                        "name": name,
                        "congratulation_date": congratulation_date.strftime("%Y.%m.%d")
                    })
        return upcoming_birthdays

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday('20.11.2025')
# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday('04.11.2025')
book.add_record(jane_record)

# Виведення всіх записів у книзі
for value in book.data.items():
    print(value)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
print(book.get_upcoming_birthdays)
# Видалення запису Jane
book.delete("Jane")