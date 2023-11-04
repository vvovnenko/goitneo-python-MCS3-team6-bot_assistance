# goitneo-python-final-project-team-6
## MCS3-C4-bot_assistant

## Address Book and NoteBook Bot
This is a simple assistant bot that can be used to manage contacts and notes.

### Features

* Add, edit, and delete contacts data such as: name, list of phones, email, birthday and address
* Search contacts by all fields
* View contacts birthdays:
  * by concrete date
  * next weak
  * in N days
* Add, edit, delete and tag notes
* Search notes by text and tags
* View all contacts and notes
* `help` command can list all commands and show syntax for concrete command
* Smart command suggestion for wrong input
* Store contacts and notes in the file storage on disk
* Generation of random data for contacts and notes on first launch


## Requirements

- Python 3.11 or higher
- pip
- [Faker](https://pypi.org/project/Faker/)


## Usage

To start the bot, run the following command:

- python main.py


## Address Book Commands

Create a new contact in the address book with a phone, or add a phone to an existing contact. 
```
> add [contact_name] [phone]
```
Change contact phone number.
```
> change-phone [contact_name] [old_phone] [new_phone]
```
Show contact phone number.
```
> phone [contact_name]
```
Add contact birthday.
```
> add-birthday [contact_name] [birthdate]
```
Show contact birthday.
```
> show-birthday [contact_name]
```
Show all contacts.
```
> all-contacts
```
Delete contact.
```
> del-contact [contact_name]
```
Search contacts on all fields.
```
> search-contacts [word]
```
Show all birthdays in the next week period.
```
> birthdays
```
Show contacts with a birthday in N days.
```
> birthdays-in-days [days]
```
Show contacts with a birthday on a specific date.
```
> birthdays-by-date [date]
```
Add email to a contact.
```
> add-email [contact_name] [email]
```
Add address to a contact.
```
> add-ad [contact_name] [address]
```

## NoteBook Commands

Add a note to the NoteBook.
```
> add-note
```
Edit an existing note.
```
> edit-note [note-id]
```
Delete an existing note.
```
> delete-note [note-id]
```
Show a list of all notes.
```
> all-notes
```
Show a specific note.
```
> note [note-id]
```
Search notes by text or tag.
```
> search-notes [-tag] [search-term]
```
Add a tag to a note.
```
> tag-note [note-id] [tag]
```
Remove tag(s) from a note.
```
> untag-note [note-id] [-all|tag-name]
```


## Help

The `help` command is used to get information about available commands in the bot. It can be used with or without arguments.

**Usage without arguments:**

```
> help
```

This will display a list of all available commands, along with a brief description of each command.

**Usage with arguments:**

```
> help [command_name]
```

This will display detailed information about the specified command, including its usage syntax, arguments, and a description of what it does.

**Examples:**

```
> help
# Displays a list of all available commands

> help add-contact
# Displays detailed information about the `add-contact` command

> help phone
# Displays detailed information about the `phone` command
```

*Please make sure to follow the specified syntax for each command. For further assistance, use the help command followed by the specific command name.*