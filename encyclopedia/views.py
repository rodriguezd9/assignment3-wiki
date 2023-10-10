import random

import markdown2
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect

from . import util
from .forms import NewEntryForm, SearchForm


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


def search(request):
    if 'q' in request.GET:
        query = request.GET['q']
        entries = util.list_entries()
        
        # if query in entries:
        matches = [entry for entry in entries if query.lower() in entry.lower()]

    
        # Check if there are no matches
        if not matches:
            messages.error(request, 'Nothing matches your search!')
        
        return render(request, "encyclopedia/search_results.html", {"matches": matches})
    else:
        messages.error(request, 'No search query provided!')
        return render(request, "encyclopedia/search_results.html", {"form": SearchForm()})
