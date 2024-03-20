from django.shortcuts import render
import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from . import util
from .forms import NewPageForm



def converter(title):
    md_file = util.get_entry(title)
    markdown_trans = markdown.Markdown()
    if md_file == None:
        return None
    else:
        return markdown_trans.convert(md_file)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def render_wiki(request, title):
    html_page = converter(title)
    if html_page == None:
        return render(request, "encyclopedia/render.html", {
            "Error": "No results"
        })
    else:
        return render(request, "encyclopedia/render.html", 
                    {"wiki": html_page,
                     "name": util.get_entry(title).split()[1]})

def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        html_page = converter(title)

        if html_page is not None:
            return render(request, "encyclopedia/render.html", {
                "wiki": html_page, 
                "name": util.get_entry(title).split()[1]
            })
        else:
            is_substring = []
            entries = util.list_entries()

            for entry in entries:
                if title.lower() in entry.lower():
                    is_substring.append(entry)
            
            return render(request, "encyclopedia/search.html", {
                "entries": is_substring,
                "error": "No results"
            })

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["page_name"]
            content = form.cleaned_data["content"]
            util.save_entry(name, content)
            return HttpResponseRedirect(reverse('encyclopedia:renderwiki', args=[name]))
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form,
            })

    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": NewPageForm
        })
    
def edit(request):
    if request.method == "GET":
        name = request.GET["name"]
        content = util.get_entry(name)
        
        return render(request, "encyclopedia/edit.html", {
            "name": name,
            "content": content
        })
    else:
        name = request.POST["name"]
        content = request.POST["content"]
        util.save_entry(name, content)
        return HttpResponseRedirect(reverse('encyclopedia:renderwiki', args=[name]))

def randompage(request):
    pages = util.list_entries()
    return HttpResponseRedirect(reverse('encyclopedia:renderwiki', args=[random.choice(pages)]))