from io import BytesIO, StringIO
import os
import pycurl , json
from urllib.parse import urlencode
from os import listdir,scandir
from os.path import isfile, join
import fileinput
from bs4 import BeautifulSoup

def insert_book(bookname):
    databook ={
          "name": bookname,
          "description": "----"
        } 
        
    buffer = BytesIO()
    crlbook = pycurl.Curl()
    crlbook.setopt(crlbook.URL, 'http://192.168.1.3:6875/api/books')
    crlbook.setopt(pycurl.HTTPHEADER, ['Authorization: Token caCi3JqYB6---------------:ndPttLatqiWv--------------'])
    crlbook.setopt(crlbook.WRITEDATA, buffer)
    pfbook = urlencode(databook)
    crlbook.setopt(crlbook.POSTFIELDS, pfbook)
    crlbook.perform()
    crlbook.close()
    body = buffer.getvalue()
    book_data = json.loads(body.decode('utf-8'))
    bookid=book_data['id']
    return (bookid)

def clearpage(filename,pagebody):
    text_to_search="<span> </span>"
    replacement_text="<br>"
    htmldoc = pagebody.replace(text_to_search, replacement_text)
    soup = BeautifulSoup(htmldoc, "html.parser")
    whitelist_tag = ['a','img']
    whitelist_attr = ['src','href']

    for tag in soup.find_all():
        attrs = dict(tag.attrs)
        for attr in attrs:
            if attr not in whitelist_attr:
                del tag.attrs[attr]
    return(soup.prettify())

def insert_page(bookid,pagename,pagehtml):
    pagecontext=clearpage(pagename+'.html',pagehtml)
    datapage ={
    "book_id": bookid,
    "name": pagename,
    "html": pagecontext#soup.prettify()
    }
    crlpage = pycurl.Curl()
    crlpage.setopt(crlpage.URL, 'http://192.168.1.3:6875/api/pages')
    crlpage.setopt(pycurl.HTTPHEADER, ['Authorization: Token caCi3JqYB6---------------:ndPttLatqiWv--------------'])
    pf = urlencode(datapage)
    crlpage.setopt(crlpage.POSTFIELDS, pf)
    crlpage.perform()
    crlpage.close()

path='/mnt/d/docs/'
subfolders = [f for f in listdir(path) if not isfile(join('.', f))]
for folder in subfolders:
    if not folder[0] == '.':
        bid = insert_book(folder)
        filepath=path+folder+'/'
        for x in os.listdir(filepath):
            if x.endswith(".html"):
                with open(filepath+x, "r") as f:
                    text= f.read()
                insert_page(bid,x.split('.')[0],text)
   
