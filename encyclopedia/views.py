from django.shortcuts import render
from . import util
from django.http import HttpResponse, HttpResponseNotFound
import markdown2 
from django import forms
from django.shortcuts import redirect
import random as rand

class NewPageForm(forms.Form):
    title = forms.CharField(label = "Title", widget = forms.TextInput(attrs = {"placeholder":"Title"}))
    content = forms.CharField(label = "Content", widget = forms.Textarea())

class EditPageForm(forms.Form):
    content = forms.CharField(label = "Content", widget = forms.Textarea())
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    if util.get_entry(name) is None:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    else:
        return HttpResponse("<title>" + str(name) + "</title>" + markdown2.markdown(util.get_entry(name)) + "<a href=\"" + str(name) + "/edit\">Edit Page</a><br><a href=\"/\">Home</a>")

def search(request):
    q = request.GET["q"]
    results = []
    if q.lower() in [x.lower() for x in util.list_entries()]:
        return entry(request, q)
    else:
        for entries in util.list_entries():
            if q.lower() in entries.lower():
                results.append(entries)
        return render(request, "encyclopedia/search.html", {
            "results": results
    })

def new(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
        if title in util.list_entries():
            return HttpResponse("<h1>An encyclopedia entry already exists with the provided title</h1>")
        else:
            util.save_entry(title, content)
            return redirect(f"/wiki/{title}")
    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm()
    })

def edit(request, name):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(name, content)
            return redirect(f"/wiki/{name}")
    return render(request, "encyclopedia/edit.html", {
        "form": EditPageForm(initial = {
            "content" : util.get_entry(name)
        }),
        "name": name
    })

def random(request):
    return redirect(f"/wiki/{rand.choice(util.list_entries())}")