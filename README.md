# Example Script for getting sources from Wikipedia


```python
import WikiLinks as wl

url = "https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)"
wikiRefs = wl.getWikiRefs(url, progress=True)
```

    4 of 4 complete

## Print item


```python
wikiRefs[1].print_ref()
```

    Title:	 10.1007/978-1-4842-3925-4_3 
    Source:	 Website Scraping with Python: Using BeautifulSoup and Scrapy 
    Date:	 None 
    URL:	 https://doi.org/10.1007%2F978-1-4842-3925-4_3 
    Image:	 https://static-content.springer.com/cover/book/978-1-4842-3925-4.jpg 
    Desc:	 In this chapter, you will learn how to use Beautiful Soup, a lightweight Python library, to extract and navigate HTML content easily and forget overly complex regular expressions and text parsing. 
    
    

## Update item


```python
wikiRefs[1].update("date")
```

    New date: 2018
    Is this correct? [y/n] : y
    


```python
wikiRefs[1].print_ref()
```

    Title:	 10.1007/978-1-4842-3925-4_3 
    Source:	 Website Scraping with Python: Using BeautifulSoup and Scrapy 
    Date:	 2018 
    URL:	 https://doi.org/10.1007%2F978-1-4842-3925-4_3 
    Image:	 https://static-content.springer.com/cover/book/978-1-4842-3925-4.jpg 
    Desc:	 In this chapter, you will learn how to use Beautiful Soup, a lightweight Python library, to extract and navigate HTML content easily and forget overly complex regular expressions and text parsing. 
    
    

## Save items to csv file

You can add additional Headers and items to the csv file when saving.


```python
extra_headers = ["Theme"]
extra_items = ["Python"]

for item in wikiRefs:
    item.save("Example.csv", extra_headers, extra_items)
```

    Save file does not exist.
    

    Make new file " Example.csv " ? [y/n] y
    

## Loading the csv file


```python
import csv

# load all items into a list
with open("Example.csv",'r', newline='\n') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    items = [item for item in csv_reader]
        
# print second item
for key in items[1].keys():
    print(key, "\t:", items[1][key])
```

    Theme 	: Python
    Title 	: 10.1007/978-1-4842-3925-4_3
    Date 	: 2018
    Source 	: Website Scraping with Python: Using BeautifulSoup and Scrapy
    URL 	: https://doi.org/10.1007%2F978-1-4842-3925-4_3
    Description 	: In this chapter, you will learn how to use Beautiful Soup, a lightweight Python library, to extract and navigate HTML content easily and forget overly complex regular expressions and text parsing.
    Image 	: https://static-content.springer.com/cover/book/978-1-4842-3925-4.jpg
    


```python

```
