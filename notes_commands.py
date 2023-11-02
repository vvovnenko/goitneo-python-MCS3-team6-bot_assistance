from command_handler import command
from storage import storage
from exceptions import ValidationException, BotSyntaxException, DuplicateException, NotFoundException

def get_syntax_error_message(expected_command):
    return f'Incorrect syntax, enter command in the following format: "{expected_command}"'

@command(name='add-note')
def add_note():
    notes = storage.notes
    note = notes.add_note()
    text = input("Enter note text: ")
    note.add_text(text)
    return f"Note [{note.id}] created."


@command(name='edit-note')
def edit_note(args):
    notes = storage.notes
    if len(args) == 0:
        raise BotSyntaxException(get_syntax_error_message("edit-note [id]"))
    note = notes.find(args[0])
    text = input("Enter new text: ")
    note.add_text(text)
    return f"Note [{note.id}] updated."


@command(name='delete-note')
def delete_note(args):
    notes = storage.notes
    if len(args) == 0:
        raise BotSyntaxException(
            get_syntax_error_message("delete-note [id]"))
    id = args[0]
    notes.delete_note(args[0])
    return f"Note [{id}] deleted."


@command(name='all-notes')
def show_notes(args):
    notes = storage.notes
    return "\n".join([f"{note}" for note in notes.values()])


@command(name='note')
def get_note(args):
    notes = storage.notes
    if not args:
        raise BotSyntaxException(get_syntax_error_message("note [id]"))
    note = notes.find(args[0])
    return f"id: {note.id}\ntext: {note.text}"


@command(name='search-notes')
def search_notes(args):
    notes = storage.notes
    if not args:
        raise BotSyntaxException(get_syntax_error_message(
            "search-notes [search-string]"))
    if args[0] == '-tag':
        if len(args) < 2:
            raise BotSyntaxException(
                get_syntax_error_message("search-notes -tag [tag]"))
        search_tags = args[1:]
        result = notes.search_by_tags(search_tags)
    else:
        result = notes.search(args)

    return "\n".join(str(note) for note in result) if result else "Nothing found"


@command(name='tag-note')
def add_note_tag(args):
    notes = storage.notes
    try:
        id, tag = args
    except:
        raise BotSyntaxException(
            get_syntax_error_message("tag-note [id] [tag]"))

    note = notes.find(id)
    note.add_tag(tag)
    return f"Tag #{tag} added to note {note.id}"
