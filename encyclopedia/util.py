import re

from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    if default_storage.exists(filename):
        with default_storage.open(filename, 'w') as f:
            f.write(content)


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        lowercase_title = title.lower()
        all_entries = [entry.lower() for entry in default_storage.listdir("entries")[1]]

        if f"{lowercase_title}.md" in all_entries:
            f = default_storage.open(f"entries/{title}.md")
            return f.read().decode("utf-8")
        else:
            return None
    except FileNotFoundError:
        return None
