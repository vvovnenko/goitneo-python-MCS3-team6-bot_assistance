# goitneo-python-final-project-team-6

## Address Book and NoteBook Bot
This is a simple bot application for managing contacts and notes. It provides various commands to add, edit, and search contacts, as well as manage notes.

## Address Book Commands

- Create a new contact in the address book with a phone, or add a phone to an existing contact. - add [contact_name] [phone]
- Change contact phone number.
- change-phone [contact_name] [old_phone] [new_phone]
- Show contact phone number. - phone [contact_name]
- Add contact birthday. - add-birthday [contact_name] [birthdate]
- Show contact birthday. - show-birthday [contact_name]
- Show all contacts. - all-contacts
- Delete contact. - del-contact [contact_name]
- Search contacts on all fields. - search-contact [word]
- Show all birthdays in the next week period. - birthdays
- Show contacts with a birthday in N days. - birthdays-in-days [days]
- Show contacts with a birthday on a specific date. - birthdays-by-date [date]
- Add email to a contact. - add-email [contact_name] [email]
- Add address to a contact. - add-ad [contact_name] [address]

## NoteBook Commands

- Add a note to the NoteBook. - add-note
- Edit an existing note. - edit-note [note-id]
- Delete an existing note. - delete-note [note-id]
- Show a list of all notes. - all-notes
- Show a specific note. - note [note-id]
- Search notes by text or tag. - search-notes [-tag] [search-term]
- Add a tag to a note. - tag-note [note-id] [tag]
- Remove tag(s) from a note. - untag-note [note-id] [-all|tag-name]

## Please make sure to follow the specified syntax for each command. For further assistance, use the help command followed by the specific command name.