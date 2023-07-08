import ebooklib
from ebooklib import epub
import os
from bs4 import BeautifulSoup

BASE_PATH = 'books/'

# Extract ebook into chapters

def chapter_to_str(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), 'html.parser')
    text = [para.get_text() for para in soup.find_all('p')]
    return ' '.join(text)

for root, dirs, files in os.walk(BASE_PATH, topdown=False):
    for name in files:
        if not(name.endswith(".epub")):
            continue
        book = epub.read_epub(BASE_PATH + name)
        chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        
        chapter_texts = {}
        for c in chapters:
            print(c.get_name())
            chapter_texts[c.get_name()] = chapter_to_str(c)

        for idx, title in enumerate(chapter_texts):
            name = os.path.splitext(name)[0]
            if not os.path.exists('books/' + name):
                os.makedirs('books/' + name)
            file_name = 'books/' + name + '/chapter_' + str(idx) + '.txt'

            if len(chapter_texts[title]) < 500:
                print('skipping... ', file_name, title, len(chapter_texts[title]))
                continue
            print('saving... ', title, file_name)

            # Save title to file
            with open(file_name, 'w') as f:
                f.write(chapter_texts[title])
            