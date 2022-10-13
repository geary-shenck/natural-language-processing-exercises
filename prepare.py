
def remove_stopwords(article_processed,words_to_add=[],words_to_remove=[]):
    ''' 
    takes in string, and two lists
    creates list of words to remove from nltk, modifies as dictated in arguements
    prints result of processing
    returns resulting string
    '''
    from nltk.corpus import stopwords
    #create the stopword list
    stopwords_list = stopwords.words("english")
    #modify stopword list
    [stopwords_list.append(word) for word in words_to_add]
    [stopwords_list.remove(word) for word in words_to_remove]
    #remove using stopword list
    words = article_processed.split()
    filtered_words = [w for w in words if w not in stopwords_list]
    #filtered_words =[word for word in article_processed if word not in stopwords_list]
    print("removed ",len(article_processed)-len(filtered_words), "words")
    #join back
    article_without_stopwords = " ".join(filtered_words)
    return article_without_stopwords

def lemmatize(article):
    ''' 
    input article
    makes object, applies to string, and returns results
    '''
    import nltk
    #create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    #use lemmatizer
    lemmatized = [wnl.lemmatize(word) for word in article.split()]
    #join words back together
    article_lemmatized = " ".join(lemmatized)
    return article_lemmatized

def stem(article):
    ''' 
    input string
    create object, apply it to the each in string, rejoin and return
    '''
    import nltk
    #create porter stemmer
    ps = nltk.porter.PorterStemmer()
    stems = [ps.stem(word) for word in article.split()]
    #join words back together
    article_stemmed = " ".join(stems)
    return article_stemmed

def tokenize(article0):
    ''' 
    input string
    creates object, returns string after object affect
    '''
    import nltk
    #create the tokenizer
    tokenize = nltk.tokenize.ToktokTokenizer()
    #use the tokenizer
    article = tokenize.tokenize(article0,return_str=True)
    return article

def basic_clean(article0):
    ''' 
    input string
    lowers cases, makes "normal" characters, and removes anything not expected
    returns article
    '''
    import unicodedata
    import re
    #lower cases
    article = article0.lower()
    ## decodes to change to "normal" characters after encoding to ascii from a unicode normalize
    article = unicodedata.normalize("NFKD",article).encode("ascii","ignore").decode("utf-8")
    # removes anything not lowercase, number, single quote, or a space
    article = re.sub(r'[^a-z0-9\'\s]','',article)
    return article

def basic_pipeline(codeup=True,news=True,words_keep=[],words_drop=[]):
    '''
    
    '''
    import acquire
    import pandas as pd

    #acquire
    news_df = pd.DataFrame(acquire.get_news_articles())
    codeup_df = pd.DataFrame(acquire.get_blog_content("https://codeup.com/blog/"))

    if codeup:
        codeup_df.rename(columns={"content":"original"},inplace=True)
        codeup_df["clean"] = [remove_stopwords(tokenize(basic_clean(each)),words_to_add=words_keep,words_to_remove=words_drop) for each in codeup_df.original]
        codeup_df["stemmed"] = [stem(each) for each in codeup_df.clean]
        codeup_df["lemmatized"] = [lemmatize(each) for each in codeup_df.clean]

    if news:
        news_df.rename(columns={"content":"original"},inplace=True),news_df.drop(columns="category",inplace=True)
        news_df["clean"] = [remove_stopwords(tokenize(basic_clean(each)),words_to_add=words_keep,words_to_remove=words_drop) for each in news_df.original]
        news_df["stemmed"] = [stem(each) for each in news_df.clean]
        news_df["lemmatized"] = [lemmatize(each) for each in news_df.clean]

    return codeup_df,news_df
    