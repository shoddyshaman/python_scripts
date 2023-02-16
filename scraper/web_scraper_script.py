from dotenv import load_dotenv
import psycopg2
import os
import requests
import re
from bs4 import BeautifulSoup

r = requests.get('https://www.kafaltree.com/?s=%E0%A4%89%E0%A4%AE%E0%A5%87%E0%A4%B6+%E0%A4%A4%E0%A4%BF%E0%A4%B5%E0%A4%BE%E0%A4%B0%E0%A5%80+%E0%A4%B5%E0%A4%BF%E0%A4%B6%E0%A5%8D%E0%A4%B5%E0%A4%BE%E0%A4%B8')


def get_links(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    s = soup.find_all('div', class_='bp-head')
    links = []
    for i in s:
        links.append(i.a['href'])
    return links


links = get_links(r)


def get_text(s):
    text = []
    for i in s:
        article = requests.get(i)
        soup = BeautifulSoup(article.content, 'html.parser')
        content = soup.find('div', class_='entry-content').text
        title = soup.find('h1', class_='entry-title').text
        text.append([title, content])
    return text


text = get_text(links)


r_two = requests.get('https://www.kafaltree.com/page/2/?s=%E0%A4%89%E0%A4%AE%E0%A5%87%E0%A4%B6+%E0%A4%A4%E0%A4%BF%E0%A4%B5%E0%A4%BE%E0%A4%B0%E0%A5%80+%E0%A4%B5%E0%A4%BF%E0%A4%B6%E0%A5%8D%E0%A4%B5%E0%A4%BE%E0%A4%B8')

links_two = get_links(r_two)
text_two = get_text(links_two)
# print(text_two[0])

# r_three = requests.get(
#     'https://www.kafaltree.com/page/3/?s=%E0%A4%89%E0%A4%AE%E0%A5%87%E0%A4%B6+%E0%A4%A4%E0%A4%BF%E0%A4%B5%E0%A4%BE%E0%A4%B0%E0%A5%80+%E0%A4%B5%E0%A4%BF%E0%A4%B6%E0%A5%8D%E0%A4%B5%E0%A4%BE%E0%A4%B8')

# links_three = get_links(r_three)
# text_three = get_text(links_three)

all_articles = [*text,*text_two]
cleaned_articles = []
for i in all_articles:
    clean_string = re.sub("\n", "", i[1])
    clean_string = re.sub(
        re.escape('(Satire by Umesh Tewari Vishwas)'), '', clean_string)
    clean_string = re.sub('ShareTweetWhatsApp89 Shares', '', clean_string)
    clean_string = re.sub('Kafal Tree OnlineSupport Kafal Tree .', '', clean_string)
    clean_string = re.sub('Tags:  Satire by Umesh Tewari VishwasUmesh Tewari Vishwas', '', clean_string)
    clean_string = re.sub('ShareWhatsAppTweet89 Shares', '', clean_string)
    clean_article = [i[0], clean_string]
    cleaned_articles.append(clean_article)

print(cleaned_articles[0])

# database connection

load_dotenv()  # Required to load the previously defined environment variables

# Create connection to postgres using connection string

# connection = psycopg2.connect(host=os.environ.get('PG_HOST'),
#                               port=os.environ.get('PG_PORT'),
#                               user=os.environ.get('PG_USER'),
#                               password=os.environ.get('PG_PASSWORD'),
#                               dbname=os.environ.get('PG_DATABASE'),
#                               sslmode='require')
# # Ensure data is added to the database immediately after write commands
# connection.autocommit = True
# cursor = connection.cursor()
# cursor.execute('SELECT %s as connected;',
#                ('Connection to postgres successful!',))

# for i in cleaned_articles:
#     cursor.execute("INSERT INTO Post (title,content,category,authorId,imageUrl,readingTime) VALUES (%s,%s,%s,%s,%s,%s);", (i[0],i[1],'satire',1,'https://www.kafaltree.com/wp-content/uploads/2019/02/34830159_1986292681427355_410858701839138816_n-238x300.jpg',7))

# cursor.close()

# export output to csv
import csv
with open('dad_articles', 'w', newline='') as file:
    writer = csv.writer(file)
    for i in cleaned_articles:
        writer.writerow([i[0],i[1],'satire',1,'https://www.kafaltree.com/wp-content/uploads/2019/02/34830159_1986292681427355_410858701839138816_n-238x300.jpg','7 minutes'])
        

    
