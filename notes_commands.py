from command_handler import command
from storage import storage
from exceptions import ValidationException, BotSyntaxException, DuplicateException, NotFoundException


def get_syntax_error_message(expected_command):
    return f'Incorrect syntax, enter command in the following format: "{expected_command}"'


@command(name='add-note')
def add_note(args):
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
        search_tags = [tag.lstrip('#') for tag in args[1:]]
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
    new_tag = note.add_tag(tag)
    return f"Tag #{new_tag.value} added to note {note.id}"


@command(name='untag-note')
def delete_note_tag(args):
    notes = storage.notes
    try:
        id, tag = args
    except:
        raise BotSyntaxException(
            get_syntax_error_message("untag-note [id] [-all|tag-name]"))

    if tag == "-all":
        note = notes.find(id)
        note.delete_all_tags()
        return f"Deleted all tags from note {note.id}"

    note = notes.find(id)
    saznitized_tag = tag.lstrip('#')
    note.delete_tag(saznitized_tag)
    return f"Tag #{saznitized_tag} deleted from note {note.id}"
