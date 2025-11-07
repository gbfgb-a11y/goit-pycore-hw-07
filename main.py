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
                    if congrat_date.weekday() == 5:
                        congrat_date += timedelta(days=2)
                    elif congrat_date.weekday() == 6:
                        congrat_date += timedelta(days=1)
                    wd0 = congrat_date.strftime("%A")
                    upcoming.append({
                        "name": record.name.value,
                        "congratulation_date": congrat_date.strftime("%Y-%m-%d"),
                        "weekday": wd0
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


def input_error_for_addphone(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError) as e:
            return f"Error: To add contact write command acording to pattern 'add NAME PHONE'."
    return inner

# Обробники команд 
@input_error
def add_contact(args, book):
    name, phone = args

    record = book.find(name)
    msg = "Contact updated."
    record = Record(name)
    book.add_record(record)
    msg = "Contact added."
    record.add_phone(phone)
    return [msg, record]


@input_error
def change(args, book, Ro):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return "No such contact."
    elif not Ro.find_phone(old_phone):
        return "Old phone not found."
    else:
            Ro.edit_phone(old_phone, new_phone)
            book.add_record(Ro)
            return "Phone changed."


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}: {', '.join(str(p) for p in record.phones)}"
    return "Contact not found."


@input_error
def show_all(book):
    if not book.data:
        return "No contacts yet."
    return "\n".join(str(r) for r in book.data.values())


@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return f"Birthday added for {name}."
    return "Contact not found."


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    elif record:
        return "This contact has no birthday yet."
    else:
        return "Contact not found."


@input_error
def birthdays(_, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    lines = [f"{b['name']}: {b['congratulation_date']}, weekday: {b['weekday']}" for b in upcoming]
    return "\n".join(lines)
@input_error
def get_help():
    return '''--------------------
Avalible commands: 
* help > to call this list.
* hello > greetings.
* add > to add phone to any contact or create a brandnew contact.
* change > to change phone to any contact.
* phone > to find contact name by phone numbers.
* all > show whole list of contacts and phones
* add-birthday > to add birthday date to any contact.
* show-birthday > to find birthday by given contact
* birthdays > to show all list of birthdays and combined names.
* close/exit > to close the programm. 
* patterns > shows the way how to call any command.
--------------------'''
@input_error
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
--------------------    '''
# Головна частина

def main():
    book = AddressBook()
    print("Welcome to the assistant bot! type command help to see avalible commands.")

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
            args=add_contact(args, book)
            try:
                mssg, Ro = args
                print(mssg)
            except Exception as e:
                print('Error: something went wrong.')
        elif command == "change":
            print(change(args, book, Ro))
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
