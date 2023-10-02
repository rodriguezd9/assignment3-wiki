from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, name):
    return render(request, "encyclopedia/wiki.html", {
        "entry": util.get_entry(name)
    })
