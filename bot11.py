def parse_input(user_input):
    parts = user_input.strip().split(maxsplit=2)  
    cmd = parts[0].lower()  
    args = parts[1:] if len(parts) > 1 else []  
    return cmd, args

def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added."

def change_contact(args, contacts):
    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        return "Contact not found."

def show_phone(args, contacts):
    name = args[0]
    if name in contacts:
        return contacts[name]
    else:
        return "Contact not found."

def show_all_contacts(contacts):
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])




def input_error(handler):
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid value provided."
        except IndexError:
            return "Please provide enough arguments."
    return wrapper

@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise IndexError
    name, phone = args
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise IndexError
    name, phone = args
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    if name not in contacts:
        raise KeyError
    return contacts[name]

@input_error
def show_all_contacts(contacts):
    if not contacts:
        return "No contacts found."
    return "\n".join([f"{name}: {phone}" for name, phone in contacts.items()])

def parse_input(user_input):
    parts = user_input.strip().split(maxsplit=2)  
    cmd = parts[0].lower()  
    args = parts[1:] if len(parts) > 1 else []  
    return cmd, args


class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not self.value.isdigit() or len(self.value) != 10:
            raise ValueError("Invalid phone format")

class Record:
    def __init__(self, name, phones=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones] if phones else []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        found = False
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                found = True
                break
        if not found:
            raise ValueError("Phone not found")

    def __str__(self):
        phones_str = ', '.join([phone.value for phone in self.phones])
        return f"Name: {self.name.value}, Phones: {phones_str}"

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return "Phone not found"

class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, name, phones=None):
        if name in self.records:
            print("Record already exists. Use 'edit_phone' to modify.")
        else:
            self.records[name] = Record(name, phones)
            print(f"Record for {name} added.")

    def find(self, name):
        record = self.records.get(name, None)
        if record:
            return record
        else:
            print("Record not found.")

    def delete(self, name):
        if name in self.records:
            del self.records[name]
            print(f"Record for {name} removed.")
        else:
            print("Record not found.")

def parse_input(user_input):
    parts = user_input.strip().split(maxsplit=2)  
    cmd = parts[0].lower()  
    args = parts[1:] if len(parts) > 1 else []  
    return cmd, args

def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add_record":
            name, phones = args[0], args[1:]
            address_book.add_record(name, phones)
        elif command == "find_record":
            name = args[0]
            record = address_book.find(name)
            if record:
                print(record)
        elif command == "remove_record":
            name = args[0]
            address_book.delete(name)
        elif command == "add_phone":
            name, phone = args[0], args[1]
            record = address_book.find(name)
            if record:
                record.add_phone(phone)
                print(f"Phone {phone} added to {name}.")
        elif command == "remove_phone":
            name, phone = args[0], args[1]
            record = address_book.find(name)
            if record:
                record.remove_phone(phone)
                print(f"Phone {phone} removed from {name}.")
        elif command == "edit_phone":
            name, old_phone, new_phone = args[0], args[1], args[2]
            record = address_book.find(name)
            if record:
                record.edit_phone(old_phone, new_phone)
                print(f"Phone {old_phone} for {name} changed to {new_phone}.")
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()