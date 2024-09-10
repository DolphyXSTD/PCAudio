import webbrowser

def command(url = None):
    if url is None:
        pass
    else:
        webbrowser.open(url)