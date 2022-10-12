from requests import get
from bs4 import BeautifulSoup

def get_blog_articles():
    ''' 
    no input
    scrapes the top page of the codeup website for title and summary of blogs
    returns a list of dictionaries
    '''
    #set variables
    url2 = "https://codeup.com/blog/"
    lst=[]
    headers = {'User-Agent': 'Codeup Data Science'} # Some websites don't accept the pyhon-requests default user-agent
    response = get(url2, headers=headers)
    #make soup
    soup=BeautifulSoup(response.content)
    #set for article
    articles = soup.select("article")
    #goes through and grabs title and summary from article
    for art,_ in enumerate(articles):
        # print(art)
        ##url
        lst.append({"title":(articles[art].select("h2")[0].text.strip()),
                    "summary": (articles[art].select("p")[1].text.strip())
                    })
    return lst



def get_news_articles(topics=["Business","Sports","Technology","Entertainment"]):
    ''' 
    takes in list of topics (optional)
    goes to inshorts website, finds pages for topics, goes to that page
    makes a list of dictionaries from headline, summary article, and category
    returns list
    '''
    #set variables
    url3 = "https://inshorts.com/en/read"
    art_list=[]
    #make the soup
    soup_main = BeautifulSoup(get(url3).content)
    articles = soup_main.select("ul")
    #go through the possible categories
    for i in range(0,len(articles[0].find_all("li"))):
        #print(i)
        #if find match to topics, go to that page and makes new soup
        if articles[0].find_all("li")[i].text in topics:
            url = "https://inshorts.com"+articles[0].find_all("a")[i]["href"]
            soup_sub = BeautifulSoup(get(url).content)
            #look for headline
            title = soup_sub.find_all("span",{"itemprop":"headline"})
            #look for summary article
            summary = soup_sub.find_all("div",{"itemprop":"articleBody"})
            #set them to a list for all on page
            for j in range(0,len(summary)):
                art_list.append({"title":title[j].text,
                                "summary":summary[j].text,
                                "category":articles[0].find_all("li",)[i].text})
    return art_list
