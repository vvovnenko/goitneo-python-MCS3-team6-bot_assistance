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
        if len(new_value) < constant.TAG_LEN:
            raise ValidationException(
                f"Note tag should be at least {constant.TAG_LEN} characters")
        self._value = new_value


class Note:
    def __init__(self, id):
        self.id = int(id)
        self.text = None
        self.tags = []

    def add_text(self, textString):
        self.text = Text(textString)

    def get_trimmed_text(self, text, max_len=10):
        return text if len(text) <= max_len else text[:max_len] + "..."

    def add_tag(self, tag):
        tags = [tag.value for tag in self.tags]
        if tag in tags:
            raise DuplicateException(f"Tag #{tag} already exists")
        self.tags.append(Tag(tag))

    def has_tags(self, search_tags):
        return any(search_tag in [tag.value for tag in self.tags] for search_tag in search_tags)

    def __str__(self):
        return f"ID: {self.id:>4}|Text: {self.get_trimmed_text(self.text.value, 50):<50}|Tags: {' '.join(f'#{t.value}' for t in self.tags)}"


class NoteBook(UserDict):
    def add_note(self):
        note = Note(self.next_id())
        self.data[id] = note
        return note

    def find(self, id):
        try:
            return self.data[int(id)]
        except KeyError:
            raise NotFoundException(f"Note with id [{self.id}] is not found")
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
        if len(self.data) == 0:
            return 1
        return max([int(id) for id in self.data.keys()]) + 1
