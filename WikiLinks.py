import bs4
import requests
import re

def getWikiRefs(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.content, features="lxml")
    linkElems = soup.find_all(class_ = 'reference-text')
    wikiRefs = []

    
    for elem in linkElems:
        #print(elem, "\n\n")
        wikiRefs.append(wikiref(elem))
        
    return wikiRefs
    
def getSource(text):
    text = str(text)
    #print(text, "\n")
    text = text.replace("\n", "")
    text = text.replace(".", "")
    match = re.search(r"</a>.*?<span class=\"reference-accessdate\">", text).group()
    #print(match)
    match = re.sub(r'(<.*?>|\s{2,})', '', match)
    match = re.sub(r'\(.*?\)', '', match)
    match = re.sub(r'\d{1,2}\s+\w+\s+20\d{2}', '', match)
    return match

def get_date(soup):
    #class="reference-accessdate"
    date = soup.find(class_="reference-accessdate").text
    date = re.sub(r"\.", "", date)
    date = re.sub(r"\s\s+", "", date)
    date = re.sub(r"Retrieved", "", date)
    date = re.sub(r"(\w+)(\d{4})", r"\1 \2", date)
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

class wikiref:
    def __init__(self, html):
        soup2 = bs4.BeautifulSoup(html.prettify(), features="lxml")
        self.html = str(soup2)
        title_html = soup2.find(class_ = "external text")
        
        # get url
        self.link = title_html.get('href')
        
        # get title
        title_text = title_html.string
        title_text = re.sub(r"\s\s\s+", '', title_text)
        self.title = re.sub(r"\"", '', title_text)
        
        # get source name
        self.source = getSource(soup2.find(class_ = "reference-text"))
        
        # get image and description
        self.image, self.description = source_page_info(self.link)
        
        # get date
        self.date = get_date(soup2)
        
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