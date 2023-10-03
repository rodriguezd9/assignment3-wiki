import random
import markdown2
from django.http import Http404
from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    entry_content = util.get_entry(title)

    if entry_content is not None:
        html_content = markdown2.markdown(entry_content)

        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "content": html_content
        })
    else:
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "content": f"Entry '{title}' not found"
        })


def random_entry(request):
    entries = util.list_entries()
    if entries:
        random_entry_name = random.choice(entries)
        random_entry_content = util.get_entry(random_entry_name)
        if random_entry_content is not None:
            html_content = markdown2.markdown(random_entry_content)
            return render(request, "encyclopedia/random_entry.html", {
                "entry": {
                    "title": random_entry_name,
                    "content": html_content
                }
            })


def edit_entry(request, title):
    entry_content = util.get_entry(title)

    if entry_content is not None:
        return render(request, "encyclopedia/edit_entry.html", {
            "title": title,
            "content": entry_content
        })


def save_entry(request, title):
    if request.method == 'POST':
        updated_content = request.POST.get('content')
        util.save_entry(title, updated_content)
        return redirect('entry', title=title)
    else:
        raise Http404("Invalid request method")
