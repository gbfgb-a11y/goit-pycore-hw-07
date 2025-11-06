from datetime import datetime, timedelta
from collections import UserDict

# Класси

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def __str__(self):
        phones = "; ".join(str(p) for p in self.phones)
        bd = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {phones}{bd}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_record(self, name):
        record = self.find(name)
        if not record:
            raise KeyError(f"Contact '{name}' not found")
        return record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                days_left = (bday - today).days
                if 0 <= days_left <= 7:
                    congrat_date = bday
                    if congrat_date.weekday() == 5:  # Saturday
                        congrat_date += timedelta(days=2)
                    elif congrat_date.weekday() == 6:  # Sunday
                        congrat_date += timedelta(days=1)
                    upcoming.append({
                        "name": record.name.value,
                        "congratulation_date": congrat_date.strftime("%Y-%m-%d")
                    })
        return upcoming

# Декоратор

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Error: Not enough arguments provided."
        except ValueError as e:
            return f"Error: {e}"
        except KeyError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
    return inner

# Хендлери

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError()
    name, phone = args
    try:
        record = book.get_record(name)
        msg = "Contact updated."
    except KeyError:
        record = Record(name)
        book.add_record(record)
        msg = "Contact added."
    record.add_phone(phone)
    return msg

@input_error
def change(args, book: AddressBook):
    if len(args) < 3:
        raise IndexError()
    name, old_phone, new_phone = args
    record = book.get_record(name)
    for i, ph in enumerate(record.phones):
        if ph.value == old_phone:
            record.phones[i] = Phone(new_phone)
            return "Phone changed."
    return "Old phone not found."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.get_record(name)
    return f"{name}: {', '.join(str(p) for p in record.phones)}"

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts yet."
    return "\n".join(str(r) for r in book.data.values())

@input_error
def add_birthday(args, book: AddressBook):
    name, date = args
    record = book.get_record(name)
    record.add_birthday(date)
    return f"Birthday added for {name}."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.get_record(name)
    if not record.birthday:
        return "This contact has no birthday yet."
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"

@input_error
def birthdays(_, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    lines = []
    for b in upcoming:
        congrat_date = datetime.strptime(b["congratulation_date"], "%Y-%m-%d").date()
        weekday_name = congrat_date.strftime("%A")
        lines.append(f"{b['name']}: {b['congratulation_date']}, weekday: {weekday_name}")
    return "\n".join(lines)

def get_help():
    return '''--------------------
Available commands: 
* help > to call this list.
* hello > greetings.
* add > to add phone to any contact or create a brand new contact.
* change > to change phone to any contact.
* phone > to find contact name by phone numbers.
* all > show whole list of contacts and phones
* add-birthday > to add birthday date to any contact.
* show-birthday > to find birthday by given contact
* birthdays > to show all list of birthdays and combined names.
* close/exit > to close the program. 
* patterns > shows the way how to call any command.
--------------------'''

def show_patterns():
    return '''--------------------
add > 'add name phone'
change > 'change name old_phone new_phone'
phone > 'phone name'
all > 'all'
add-birthday > 'add-birthday name date'
show-birthday > 'show-birthday name'
birthdays > 'birthdays'
close/exit > 'close'/'exit'
--------------------'''

# Головна частина

def main():
    book = AddressBook()
    print("Welcome to the assistant bot! Type command 'help' to see available commands.")

    while True:
        user_input = input("Enter a command: ").strip().lower()
        if not user_input:
            continue
        parts = user_input.split()
        command, args = parts[0], parts[1:]
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == 'patterns':
            print(show_patterns())
        elif command == 'help':
            print(get_help())
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

