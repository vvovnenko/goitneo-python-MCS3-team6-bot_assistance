import constant
from collections import UserDict
from exceptions import ValidationException, DuplicateException, NotFoundException, NotFoundException


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Text(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if len(new_value) < constant.NOTE_TEXT_LEN:
            raise ValidationException(
                f"Note text should contain at least {constant.NOTE_TEXT_LEN} characters")
        self._value = new_value


class Tag(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        sanitized_value = new_value.lstrip('#')
        if len(sanitized_value) < constant.TAG_LEN:
            raise ValidationException(
                f"Note tag should be at least {constant.TAG_LEN} characters")
        self._value = sanitized_value


class Note:
    def __init__(self, id):
        self.id = int(id)
        self.text = None
        self.tags = []

    def add_text(self, textString):
        self.text = Text(textString)

    def get_trimmed_text(self, text, max_len=10):
        suffix = "..."
        return text if len(text) <= max_len else text[:max_len - len(suffix)] + suffix

    def add_tag(self, tag):
        tags = [tag.value for tag in self.tags]
        if tag in tags:
            raise DuplicateException(f"Tag #{tag} already exists")
        new_tag = Tag(tag)
        self.tags.append(new_tag)
        return new_tag

    def delete_tag(self, tag):
        found_tag = self.find_tag(tag)
        if not found_tag:
            error_msg = f"Note {self.id} is not tagged with {tag}"
            raise NotFoundException(error_msg)
        self.tags.remove(found_tag)

    def delete_all_tags(self):
        self.tags = []

    def find_tag(self, tag):
        return next((t for t in self.tags if t.value == tag), None)

    def has_tags(self, search_tags):
        return any(search_tag in [tag.value for tag in self.tags] for search_tag in search_tags)

    def __str__(self):
        return f"ID: {self.id:^4}|Text: {self.get_trimmed_text(self.text.value, 50):<50}|Tags: {' '.join(f'#{t.value}' for t in self.tags)}"


class NoteBook(UserDict):
    def add_note(self):
        note = Note(self.next_id())
        self.data[note.id] = note
        return note

    def find(self, id):
        try:
            return self.data[int(id)]
        except KeyError:
            raise NotFoundException(f"Note with id [{id}] is not found")
        except ValueError:
            raise ValidationException(f"Note id must be integer")

    def search(self, search_strings: []):
        result = []
        for note in self.data.values():
            if any(search_str in note.text.value for search_str in search_strings):
                result.append(note)
        return result

    def search_by_tags(self, search_tags: []):
        return list(filter(lambda note: note.has_tags(search_tags), self.data.values()))

    def delete_note(self, id):
        existing_note = self.find(id)
        if existing_note:
            self.data.pop(existing_note.id)

    def next_id(self):
        if not self.data:
            return 1
        id = max([int(id) for id in self.data.keys()]) + 1
        return id
