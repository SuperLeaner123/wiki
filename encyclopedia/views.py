import random
import markdown2
from django.shortcuts import render, redirect
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    
    html_content = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return redirect("index")
    
    entries = util.list_entries()
    
    for entry_name in entries:
        if query.lower() == entry_name.lower():
            return redirect("entry", title=entry_name)
    
    matching_entries = [entry_name for entry_name in entries if query.lower() in entry_name.lower()]
    
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "entries": matching_entries
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        
        if not title or not content:
            return render(request, "encyclopedia/new_page.html", {
                "error": "Both title and content are required.",
                "title": title,
                "content": content
            })
        
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/new_page.html", {
                "error": "An entry with this title already exists.",
                "title": title,
                "content": content
            })
            
        util.save_entry(title, content)
        return redirect("entry", title=title)
        
    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        util.save_entry(title, content)
        return redirect("entry", title=title)
        
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
        
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    entries = util.list_entries()
    if entries:
        selected_page = random.choice(entries)
        return redirect("entry", title=selected_page)
    return redirect("index")


def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": f"The requested page '{title}' was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })