import random
import markdown2
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from . import util

from django.http import HttpResponseRedirect
from .forms import NewEntryForm
from django.contrib import messages


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
            

def create_entry(request):
    entries = util.list_entries()
    if request.method != 'POST':
        return render(request, "encyclopedia/create_entry.html", {"form": NewEntryForm()})

    form = NewEntryForm(request.POST)
    if not form.is_valid():
        return render(request, "encyclopedia/create_entry.html", {"form": form})

    title = form.cleaned_data["title"]
    content = form.cleaned_data["content"]
    if util.get_entry(title) is not None:
        messages.error(request, 'Entry already exists!')
        return redirect("index")

    util.save_entry(title, content) # save the entry
    messages.success(request, 'Entry created successfully!')
    print(util.list_entries())  # check the entries when rendering the index page
    print(util.get_entry(title))

    return render(request, "encyclopedia/index.html", {
        "title": title,
        "content": content,
        "entries": util.list_entries()
    })


def edit_entry(request, title):
    entry_content = util.get_entry(title)

    if entry_content is not None:
        return render(request, "encyclopedia/edit_entry.html", {
            "title": title,
            "content": entry_content
        })


def save_entry(request, title):
    if request.method != 'POST':
        raise Http404("Invalid request method")

    updated_content = request.POST.get('content')
    util.save_entry(title, updated_content)
    return redirect('entry', title=title)


