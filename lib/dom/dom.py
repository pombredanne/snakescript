import __builtin__

def elem(selector):
    prefix = selector[0]
    if prefix == "#":
        return document.getElementById(selector.substr(1))
    elif prefix == ".":
        return document.getElementsByClassName(selector.substr(1))[0]
    else:
        return document.getElementsByTagName(selector)[0]

def elems(selector):
    prefix = selector[0]
    if prefix == "#":
        return list([document.getElementById(selector.substr(1))])
    elif prefix == ".":
        return list(document.getElementsByClassName(selector.substr(1)))
    else:
        return list(document.getElementsByTagName(selector))

def html(obj, cls):
    frag = document.createDocumentFragment()
    if isinstance(obj, Object):
        e = document.createElement("div")
        if cls:
            e.setAttribute("class", cls)
        for item in obj:
            e.appendChild(html(obj[item], item))
    elif isinstance(obj, Array):
        e = document.createElement("div")
        if cls:
            e.setAttribute("class", cls)
        for item in obj:
            console.log(item)
            e.appendChild(html(item))
    else:
        e = document.createElement("span")
        if cls:
            e.setAttribute("class", cls)
        e.appendChild(document.createTextNode(obj.toString()))
    frag.appendChild(e)
    return frag

window.elem = dom.elem
window.elems = dom.elems
window.html = dom.html

