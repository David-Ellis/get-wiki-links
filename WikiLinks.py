import bs4
import requests
import re
import os
import csv

def get_headers(extra_headers = None):
    '''
    Make a list of the headers with any headers beyond the default first
    '''
    fieldnames = ["Title", "Date", "Source", "URL", "Description", "Image"]
    
    # Add any extra headers
    if extra_headers != None:
        assert type(extra_headers) == list, "Error: extra headers should be in a list"
        for header in extra_headers[::-1]:
            fieldnames.insert(0,header)
            
    return fieldnames

def make_csv(file_name, extra_headers = None):
    '''
    Create a new csv file with default headers + any addional headers given
    '''
    with open(file_name, mode='w', newline='\n') as csv_file:
        fieldnames = get_headers(extra_headers)
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

def checkPage(url):
    '''
    Check if page exists
    '''
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, features="lxml")
    
    refs = soup.find_all(class_ = 'reference-text')    
    
    if len(refs) == 0:
        return False
    else:
        return True
    
def getWikiRefs(url, progress = False):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, features="lxml")
    
    linkElems = soup.find_all(class_ = 'reference-text')
    wikiRefs = []

    for i, elem in enumerate(linkElems):
        #print(elem, "\n\n")
        wikiRefs.append(wikiref(elem))
        if progress == True:
            print("{} of {} complete".format(i+1, len(linkElems)), end = "\r")
        
    if len(wikiRefs) == 0:
        print("Error: No references found.")
        
    return wikiRefs
    
def getSource(text):
    text = str(text)
    text = text.replace("\n", "")
    try:
        match = re.findall(r"<i>(.+?)</i>", text)[0]
        match = re.sub(r"\s\s+", "", match)
    except:
        match = None
    return match

def get_date(soup):
    #class="reference-accessdate"
    try:
        
        date = soup.find(class_="reference-text").text
        date = date.replace("\n", "")
        date = re.findall(r"\d+?\s+?(\w+)?\s+?\d{4}", date)[0]
        date = date.replace("\'" , "")
        
    except:
        date = None
    return date

def get_image(soup):
    try:
        # try to find og image
        image = soup.find("meta",  property="og:image")["content"]
    except:
        image = None
    return image

def get_description(soup):
    try:
        # try to find og description
        try:
            description = soup.find(attrs={"name":"description"})["content"]
        except:
            description = soup.find(attrs={"name":"og:description"})["content"]
    except:
        # try to get first paragraph
        description = soup.find("p").string
        
    description = re.sub(r"\s\s+", "", description)
        
    if description[-1] != ".":
        description += "."
    
    return description
        
def source_page_info(url):
    if url[-4:].lower() == ".pdf":
        image = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/PDF_file_icon.svg/800px-PDF_file_icon.svg.png"
        description = "Downloadable pdf."
    else:
        try:
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.content, features="lxml")
            image = get_image(soup)
            description = get_description(soup)
        except:
            image = None
            description = None
            
    return image, description

def get_input(text):
    accepted = False
    while accepted == False:
        input_text = input(text)
        check = input("Is this correct? [y/n] :").lower()
        if check == "y":
            accepted = True
    return input_text

def get_title(soup, ref_url):
    title_html = soup.find(class_ = "external text")
    try:
        title_text = title_html.string
        title_text = re.sub(r"\s\s\s+", '', title_text)
        title_text = re.sub(r"\"", '', title_text)
        title_text  = re.sub(r"\n","", title_text)
    except:
        try:
            res = requests.get(ref_url)
            soup = bs4.BeautifulSoup(res.content, features="lxml")
            title_text = re.match(r"<title>(.*?)</title>", str(soup.title)).group(1)
            title_text = re.sub(r"\s\s+","", title_text)
            title_text  = re.sub(r"\n","", title_text)
        except:
            title_text = None
    return title_text
        
def get_link(soup):
    title_html = soup.find(class_ = "external text")
    try:
        link = title_html.get('href')
    except:
        try:
            link = soup.get('href')
        except:
            link = None
    return link
    
class wikiref:
    def __init__(self, html):
        soup = bs4.BeautifulSoup(html.prettify(), features="lxml")
        self.html = str(soup)
        
        
        # get url
        self.link = get_link(soup)
        
        # get title
        self.title = get_title(soup, self.link)
        
        # get source name
        self.source = getSource(soup.find(class_ = "reference-text"))
        
        # get image and description
        if self.link != None:
            self.image, self.description = source_page_info(self.link)
        
        # get date
        self.date = get_date(soup)
        
    def print_ref(self):
        print("Title:\t", self.title,
          "\nSource:\t", self.source, 
          "\nDate:\t", self.date, 
          "\nURL:\t", self.link,  
          "\nImage:\t", self.image,
          "\nDesc:\t", self.description,
          "\n")
        
    def update(self, entry):
        if entry == "title":
            self.title = get_input("New title:")
        elif entry == "link":
            self.link = get_input("New url:")
        elif entry == "source":
            self.source = get_input("New source name:")
        elif entry == "description":
            self.description = get_input("New description:")
        elif entry == "date":
            self.date = get_input("New date:")
        elif entry == "image":
            self.image = get_input("New image url:")
        else:
            Exception("Cannot update wikiref. Entry not recognised.")
            
    def save(self, file_name, extra_headers = None, extra_items = None):
        
        # If the file doesn't exist then ask if we should make one
        if not os.path.isfile(file_name):
            print("Save file does not exist.")
            make_new = input("Make new file \" {} \" ? [y/n]".format(file_name)).lower()
            if make_new == "y":
                #make new file
                make_csv(file_name, extra_headers = extra_headers)
            else:
                Exception("No file to save too.")
        
        self.append_csv(file_name, extra_headers, extra_items)
        
    def append_csv(self, file_name, extra_headers = None, extra_items = None):
        fieldnames = get_headers(extra_headers)
        with open(file_name,'a', newline='\n') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = fieldnames, 
                                    delimiter=';', quoting = csv.QUOTE_NONNUMERIC, quotechar='"')

            row = {"Title" : self.title,
                   'Source': self.source, 
                   'Date'  : self.date, 
                   "URL"   : self.link,
                   "Image" : self.image, 
                   "Description" : self.description}

            if extra_headers != None:
                assert extra_items != None, "Error: No items for extra headers"
                for header, item in zip(extra_headers, extra_items):
                    row[header] = item
            writer.writerow(row)
