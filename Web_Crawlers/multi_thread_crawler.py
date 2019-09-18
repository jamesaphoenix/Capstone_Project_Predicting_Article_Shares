## Importing Libraries For Multi-threading
import requests
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

class MultiThreadScraper:
 

    def __init__(self, links, data_dict):
        self.pool = ThreadPoolExecutor(max_workers=20)
        self.scraped_pages = set([])
        self.to_crawl = Queue()
        self.start_url = 'https://gatheringdreams.com/affiliate-marketing-for-dummies/'
        self.to_crawl.put(self.start_url)
        self.links = ['https://www.entrepreneur.com/article/319017',
                     'https://maybethisway.com/blogging-tips/intro-affiliate-marketing/']
        
        self.data_dict = data_dict
    
    
    def technical_page_metrics(self, req):
        #Page_Size_In_Bytes
        page_size_in_bytes = len(req.content)

        text = fulltext(req.text)

        #Plain_text_size
        plain_text_size = len(text)

        #plain_text_rate --> plaintext rate value (plain_text_size / page_size)
        plain_text_rate = (plain_text_size / page_size_in_bytes) * 100

        #Encoding 
        encoding = req.encoding

        #Detecting SSL Encryption
        if 's' in req.url:
            SSL = True
        else:
            SSL = False
            
        self.data_dict['Page_Size_In_Bytes'].append(page_size_in_bytes)
        self.data_dict['Plain_Text_Size'].append(plain_text_size)
        self.data_dict['Plain_Text_Rate'].append(plain_text_rate)
        self.data_dict['Encoding'].append(encoding)
        
        if SSL == True:
            self.data_dict['SSL'].append(1)
        else:
            self.data_dict['SSL'].append(0)
            
        
    def get_article_links(self, article_text, soup):
        soup = BeautifulSoup(article_text)
        body_links = soup.find_all('a')
        number_of_links = len(body_links)
        #Links To Text Ratio
        Links_To_Text_Ratio = len(body_links) / len(article_text)
        return body_links, number_of_links, Links_To_Text_Ratio
        
 
    def parse_links(self, html):
        for url in self.links:
            if url not in self.scraped_pages:
                self.to_crawl.put(url)
        self.links.pop(0)
        
 
    def scrape_info(self, html, status_code):
        article = self.article
        article.download()
        article.parse()
        
        #Scraping Article Metrics
        author = article.authors
        publish_date = article.publish_date
        text = fulltext(html)
        article_text = article.text
        article_top_image = len(article.top_image)
        article_movies = len(article.movies)
        article_is_media_news = article.is_media_news()
        favicon = article.meta_favicon
        has_top_image = article.has_top_image()
        number_of_images = len(article.images)
        is_valid_body = article.is_valid_body()
        
        #Article NLP
        article.nlp()
        main_keywords = article.keywords
        lexicon_count = textstat.lexicon_count(article_text, removepunct=True)
        
        #Extracting Sentences
        sentences = nltk.sent_tokenize(article_text)
        number_of_sentences = len(sentences)
        
        
        #Extract Article Readability Scores
        Flesch_Reading_Ease_formula = textstat.flesch_reading_ease(article_text)
        Flesch_Kincaid_Grade_Level = textstat.flesch_kincaid_grade(article_text)
        FOG_Scale = textstat.gunning_fog(article_text)
        SMOG_Index = textstat.smog_index(article_text)
        ARI_Index = textstat.automated_readability_index(article_text)
        
        
        #BeautifulSoup Extraction
        soup = BeautifulSoup(html)
        #Get Title Tag Of Page
        title_text = soup.title.getText()
        #Title Tag Length In Characters
        title_tag_length = len(title_text)
        # First get the meta description tag
        description = soup.find('meta', attrs={'name':'og:description'}) or soup.find('meta', attrs={'property':'description'}) or soup.find('meta', attrs={'name':'description'})
        # If description meta tag was found, then get the content attribute and save it to db entry
        description = description.get('content')
        
        #Extract Text Metrics From Article Text
        body_links , number_of_links,  Links_To_Text_Ratio = self.get_article_links(article_text, soup)
        
        
        #### Dictionary Inserts #####
        self.data_dict['HTML_Content'].append(html)
        self.data_dict['Full_Text'].append(text)
        self.data_dict['Authors'].append(author)
        self.data_dict['Publish_Date'].append(publish_date)
        self.data_dict['Article_Text'].append(article_text) 
        self.data_dict['Article_Text_Length'].append(len(article_text))
        
        if has_top_image == True:
            self.data_dict['Has_Top_Image'] .append(1)
        else:
            self.data_dict['Has_Top_Image'].append(np.nan)

        if article_movies != 0:
            self.data_dict['Number_of_Movies'].append(article_movies)
        else:
            self.data_dict['Number_of_Movies'].append(0)

        if article_is_media_news == True:
            self.data_dict['Article_Is_Media_News'].append(1)
        else:
            self.data_dict['Article_Is_Media_News'].append(0)

        if favicon == True:
            self.data_dict['Website_Has_Favicon'] .append(1)
        else:
            self.data_dict['Website_Has_Favicon'] .append(0)
            
        if number_of_images != 0:
            self.data_dict['Number_Of_Images'].append(number_of_images)
        else:
            self.data_dict['Number_Of_Images'].append(0)

        if is_valid_body == True:
            self.data_dict['Is_Valid_Body'].append(1)
        else: 
            self.data_dict['Is_Valid_Body'].append(0)
        
        ### NLP Features
        self.data_dict['Setences_Text'].append(sentences)
        self.data_dict['Number_Of_Sentences'].append(number_of_sentences)
        self.data_dict['Lexicon_Count'].append(lexicon_count)
        
        ### Readability Scores   
        self.data_dict['Flesch_Reading_Ease_formula'].append(Flesch_Reading_Ease_formula)
        self.data_dict['Flesch_Kincaid_Grade_Level'].append(Flesch_Kincaid_Grade_Level)
        self.data_dict['FOG_Scale'].append(FOG_Scale)
        self.data_dict['SMOG_Index'].append(SMOG_Index)
        self.data_dict['ARI_Index'].append(ARI_Index)
        
        self.data_dict['Title_Text'].append(title_text)
        self.data_dict['Title_Tag_Length'].append(title_tag_length)
        
        if description:
            self.data_dict['Meta_Description'].append(description)
            self.data_dict['Meta_Description_Length'].append(len(description))
        else:
            self.data_dict['Meta_Description'].append(np.nan)
            self.data_dict['Meta_Description_Length'].append(0)
            
        ### Additional Page Features
        if len(body_links) != 0:
            master_dict['Body_Content_Links'].append(body_links)
        else:
            master_dict['Body_Content_Links'].append(0)
            
        if number_of_links != 0:
            master_dict['Number_Of_Links'].append(number_of_links)
        else:
            master_dict['Number_Of_Links'].append(0)
            
        if Links_To_Text_Ratio != 0:
            master_dict['Links_To_Text_Ratio'].append(Links_To_Text_Ratio)
        else:
            master_dict['Links_To_Text_Ratio'].append(0)
 
   
    def post_scrape_callback(self, res):
        result = res.result()
        self.data_dict['URL'].append(result.url)
        status = result.status_code
        if result and result.status_code == 200:
            self.parse_links(result.text)
            self.scrape_info(result.text, status)
            self.technical_page_metrics(result)
 
   
    def scrape_page(self, url):
        try:
            res = requests.get(url, timeout=(3, 30))
            self.article = Article(url)
            return res
        except requests.RequestException:
            return
 
    
    def run_scraper(self):
        while True:
            try:
                target_url = self.to_crawl.get(timeout=6)
                if target_url not in self.scraped_pages:
                    print("Scraping URL: {}".format(target_url))
                    self.scraped_pages.add(target_url)
                    job = self.pool.submit(self.scrape_page, target_url)
                    job.add_done_callback(self.post_scrape_callback)
            except Empty:
                return
            except Exception as e:
                print(e)
                continue
