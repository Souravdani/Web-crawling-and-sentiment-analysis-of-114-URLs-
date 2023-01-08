
import pandas as pd
import numpy as np
import requests 
from bs4 import BeautifulSoup

# urls
inputdata= pd.read_csv("C:\\Users\\Soura\\Downloads\\Input.csv")
urls= list(inputdata["URL"])
len(urls)




################################# EXTRACTION #############################
for i in range(len(urls)):
    
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"}
    r= requests.get(urls[i],headers= headers)   # GET request for getting the website data
    html_content= r.content  # HTML code of the website

    soup= BeautifulSoup(html_content, 'html.parser') # Parsing the HTML content of the website
    if soup.find(attrs= {"class":"td-post-content"}) is None:
        print(i,urls[i])
    else:
        txt= soup.find(attrs= {"class":"td-post-content"}).text
        
    text=txt.replace('\n',' ')

    title= soup.title.get_text()
    #title= title[0:15]
    #title.replace("|"," ")
 




############################# ANALYSIS ################################



from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import re




## Sentence count per article
sentence_length= []
all_articles= []
for i in range(114):
    with open(f"text{i+1}.txt", 'r', encoding='utf-8', errors="replace") as in_file:
        content = in_file.read()
    content= content.lower()
    all_articles.append(content)
    sentences= sent_tokenize(content)
    length= len(sentences)
    sentence_length.append(length)
    
print(sentence_length, end="")
print(all_articles[1])


## STOPWORDS
file= ["Auditor","Currencies","DatesandNumbers", "Generic","GenericLong","Geographic","Names"]
all_stopwords=set()
for ele in file:
    with open(f"StopWords_{ele}.txt") as file:
        stopfile= file.read()
        stopfile= stopfile.lower()
        stopfile=stopfile.replace('\n',' ').replace("|","")
        tok_words= word_tokenize(stopfile)
        all_stopwords.update(tok_words)
print(all_stopwords)

       
    
## Cleanined tokenized articles without puncuations and stopwords
cleaned_articles= [0]*114
stopwords= list(all_stopwords)
for i in range(len(all_articles)):
    article= word_tokenize(all_articles[i])
    for w in stopwords:
        cleaned_articles[i]= all_articles[i].replace('?','').replace('.','').replace(',','').replace('!','')
    article_tokens= word_tokenize(all_articles[i])
    tokens_without_sw= [word for word in article_tokens if not word in all_stopwords]
    cleaned_articles[i]= tokens_without_sw
print(cleaned_articles[0])



## Word count and average word length per article
words = []
avg_word_len=[]
for ele in all_articles:
    ele= ele.replace('?','').replace('.','').replace(',','').replace('!','')
    tok_words= word_tokenize(ele)
    count=0
    for i in tok_words:
        count+=len(i)
    avg_word_len.append(count/(len(tok_words))) #Sum of the total number of characters in each word/Total number of words
    words.append(len(tok_words))

avg_sentence_len= np.array(words)/np.array(sentence_length)


## Word count per cleaned article
words_cleaned=[]
for ele in cleaned_articles:
    words_cleaned.append(len(ele))  
len(words_cleaned)



## CALCULATING SYLABBLE, COMPLEX WORD COUNT
sylabble_counts=[]
complex_word_count=[]
for article in all_articles:
    tokenized_article= word_tokenize(article)
    sylabble_count=0
    complex_count=0
    for word in tokenized_article:
        count=0
        for i in range(len(word)):
            if(word[i]=='a' or word[i]=='e' or word[i] =='i' or word[i] == 'o' or word[i] == 'u'):
                count+=1
            if(i==len(word)-2 and (word[i]=='e' and word[i+1]=='d')):
                count-=1
            if(i==len(word)-2 and (word[i]=='e' and word[i]=='s')):
                count-=1
            sylabble_count+=count    
        if(count>2):
            complex_count+=1
    sylabble_counts.append(sylabble_count)
    complex_word_count.append(complex_count)
           


## CALCULATING PERSONAL PRONOUNS
PP = []
pp= {"i","we", "my","ours","us"}
for ele in all_articles:
    ele= word_tokenize(ele)
    pp_count=0
    for word in ele:
        if word in pp:
            pp_count+=1
    PP.append(pp_count)



## POSITIVITY/NEGATIVITY SCORE
negative_words=set()
with open("negative-words.txt") as file:
    neg= file.read()
    neg= neg.lower()
    neg=neg.replace('\n',' ').replace("|","")
    tok_words= word_tokenize(neg)
    negative_words.update(tok_words)



positive_words=set()
with open("positive-words.txt") as file:
    pos= file.read()
    pos= pos.lower()
    tok_words= word_tokenize(pos)
    positive_words.update(tok_words)



neg_score=[]
pos_score=[]
for ele in cleaned_articles:
    neg_count=0
    pos_count=0
    for word in ele:
        if word in negative_words:
            neg_count+=1
        elif word in positive_words:
            pos_count+=1
    neg_score.append(neg_count)
    pos_score.append(pos_count)
    

  

## CREATING DATAFRAME FOR THE WORK
data= urls
df= pd.DataFrame(data,columns=['URL'])
df["sentences"]= sentence_length
df["raw_words"]= words
df["avg_word_len"]= avg_word_len
df["avg_word_len"]= round(df["avg_word_len"],3)
df["cleaned_words"]= words_cleaned
df["avg_no_of_words_per_sentence"]= round((df["raw_words"]/df["sentences"]),0)
df["sylabble_counts"]= sylabble_counts
df["sylabble_per_word"]= df['sylabble_counts']/ df["raw_words"]
df["sylabble_per_word"]= round(df["sylabble_per_word"],2)
df["complex_word_count"]= complex_word_count
df["complex_word_percent"]= round(100* (df["complex_word_count"])/(df["raw_words"]))
df["fog_index"]= 0.4*((df["avg_no_of_words_per_sentence"]) + df["complex_word_percent"]) 
df["personal_pronouns"]= PP
df["positive_score"]= pos_score
df["negative_score"]= neg_score

df["polarity_score"]= (df["positive_score"]- df["negative_score"])/((df["positive_score"]+df["negative_score"]) + 0.000001)
df["polarity_score"]= round(df["polarity_score"],3)

df['subjectivity_score'] = (df['positive_score'] + df['negative_score'])/( (df["cleaned_words"]) + 0.000001)
df['subjectivity_score']= round(df["subjectivity_score"],3)


df.to_excel("data_.xlsx",index= True)











