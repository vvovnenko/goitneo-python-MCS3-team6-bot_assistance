from app.command_handler import command
from app.storage import storage
from app.exceptions import BotSyntaxException
from app.util.string_utils import get_divider


@command(name='add-note')
def add_note(args):
    """Add note to the NoteBook
    usage:
        add-note
        """
    notes = storage.notes
    note = notes.add_note()
    text = input("Enter note text: ")
    note.add_text(text)
    return f"Note [{note.id}] created."


@command(name='edit-note')
def edit_note(args):
    """Edit existing note
       usage:
           edit-note [note-id]
       arguments:
           note-id - note identifier
           """
    notes = storage.notes
    if len(args) == 0:
        raise BotSyntaxException()
    note = notes.find(args[0])
    text = input("Enter new text: ")
    note.add_text(text)
    return f"Note [{note.id}] updated."


@command(name='delete-note')
def delete_note(args):
    """Delete existing note
       usage:
           delete-note [note-id]
       arguments:
           note-id - note identifier
           """
    notes = storage.notes
    if len(args) == 0:
        raise BotSyntaxException()
    id = args[0]
    notes.delete_note(args[0])
    return f"Note [{id}] deleted."


@command(name='all-notes')
def show_notes(args):
    """Show list of all notes
       usage:
           all-notes
           """
    notes = storage.notes
    return get_divider().join([f"{note}" for note in notes.values()]) + get_divider()


@command(name='note')
def get_note(args):
    """Show note
       usage:
           note [note-id]
       arguments:
           note-id - note identifier
           """
    notes = storage.notes
    if not args:
        raise BotSyntaxException()
    note = notes.find(args[0])
    tags = ' '.join(f'#{t.value}' for t in note.tags)
    return f"id: {note.id}\ntext: {note.text}\ntags: {tags}"


@command(name='search-notes')
def search_notes(args):
    """Search notes by text or tag
       usage:
           search-notes [-tag] [search-term]
       arguments:
           -tag - search by tag mode (optional)
           search-term - text/tag to search
           """
    notes = storage.notes
    if not args:
        raise BotSyntaxException()
    if args[0] == '-tag':
        if len(args) < 2:
            raise BotSyntaxException()
        search_tags = [tag.lstrip('#') for tag in args[1:]]
        result = notes.search_by_tags(search_tags)
    else:
        result = notes.search(args)
    divider = get_divider()
    return divider + divider.join(str(note) for note in result) if result else "Nothing found" + divider


@command(name='tag-note')
def add_note_tag(args):
    """Add tag to note
       usage:
           tag-note [note-id] [tag]
       arguments:
           note-id - updated note identifier
           tag - tag to add
           """
    notes = storage.notes
    try:
        id, tag = args
    except:
        raise BotSyntaxException()

    note = notes.find(id)
    new_tag = note.add_tag(tag)
    return f"Tag #{new_tag.value} added to note {note.id}"


@command(name='untag-note')
def delete_note_tag(args):
    """Remove tag(s) from note
       usage:
           untag-note [note-id] [-all|tag-name]
       arguments:
           note-id - note to remove tag(s) from
           -all - remove all tags from note
           tag-name - remove tag by name
           """
    notes = storage.notes
    try:
        id, tag = args
    except Exception:
        raise BotSyntaxException()

    if tag == "-all":
        note = notes.find(id)
        note.delete_all_tags()
        return f"Deleted all tags from note {note.id}"

    note = notes.find(id)
    saznitized_tag = tag.lstrip('#')
    note.delete_tag(saznitized_tag)
    return f"Tag #{saznitized_tag} deleted from note {note.id}"
