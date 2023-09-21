from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from . import util
from django import forms
from django.urls import reverse
from random import randint 
from markdown2 import Markdown

class SearchForm(forms.Form):                       #creating a class which takes forms from Django
    search_result = forms.CharField(label="Search")

class CreateEntry(forms.Form):                      #creating a class which takes forms from Django
    new_entry = forms.CharField(label="Title")

markdowner = Markdown()
entries = util.list_entries()
search_results = []

def index(request):
     search_results = []
     if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data["search_result"]

            if util.get_entry(search_query):
                return HttpResponseRedirect(reverse('title', args=[search_query]))
            
            else:
                # If no matching entry is found, perform a substring search
                for entry in entries:
                    if search_query.lower() in entry.lower():
                        search_results.append(entry)
                return render(request, "encyclopedia/search_results.html", {
                    "search_results": search_results
                })
    
     return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm(),
        "search_results": search_results
    })

def title(request, subject):
    title = None
    word = subject.split()
    if word:
        first_word = word[0]
    for entry in entries:
        if entry.lower() == first_word.lower():
            title = entry
            break
    # entry_content = util.get_entry(subject)
    # #checks if the title matches the # of markdown so it can be removed, without duplicating titles
    # lines = entry_content.split('\n')
    # if lines[0].strip() == title:
    #     entry_content = '\n'.join(lines[1:])
    entry_content = util.get_entry(subject)

# Remove lines starting with #
    entry_lines = entry_content.split('\n')
    entry_lines = [line for line in entry_lines if not line.strip().startswith("#")]

# Join the remaining lines back together
    entry_content = '\n'.join(entry_lines)

    html_content = markdowner.convert((entry_content))
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "subject": html_content
    })

def new(request):
    #comment test
    if request.method == "POST":
        new_form = CreateEntry(request.POST)
        if new_form.is_valid():
            new_title = new_form.cleaned_data["new_entry"]
            title_entry = request.POST.get("title_entry")

            for entry in entries:                       #if new_title is same as entries
                if new_title.lower() == entry.lower():
                    return HttpResponse("Already exists")
            
            util.save_entry(new_title, title_entry)
            # return redirect('title', subject=new_title)
            return render(request, "encyclopedia/title.html", {
                "title": new_title,
                "subject": markdowner.convert(title_entry)
            })

    return render(request, "encyclopedia/new.html", {
        # "form": SearchForm(),
        "new_form": CreateEntry()
    })

def edit(request,title):
    subject = util.get_entry(title)
    if request.method == "POST":
        
        for entry in entries:
            if entry.lower() == title.lower():
                title = entry
    # if request.method == "POST":
    #      util.save_entry(title, subject)
    #      return redirect('title', subject=title)
        edited_content = request.POST['edit_page']
        util.save_entry(title, edited_content)
        return redirect('title', subject=title)
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "subject": subject
    })

def random(request):
    a = 0
    b = len(entries)
    title_no = entries[randint(a,b)]
    # return HttpResponse("What is this?")
    return render(request, "encyclopedia/title.html", {
        "title": title_no,
        "subject": util.get_entry(title_no)
    })
    
    



   



    





