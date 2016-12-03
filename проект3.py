import re, urllib.request as ur, os, html.parser
#Пояснение к программе: был взят новостной сайт, с новостями, разбитыми по темам: http://www.notum.info/tema 
#Программа работает для всех тем,только нужно смотреть уровень заголовка,
#используемого в HTMl страницы по конкретной теме, и изменять в зависимости от этого уровень заголовка в регулярном выражении в моей программе 
def page_code(pageUrl):
    try:
        page = ur.urlopen(pageUrl)
        text = page.read().decode('utf-8')
    except:
        print('Error at', pageUrl)
        text = ''
    return text
    
def finding(text):
    urls = re.findall('<h3><a href="(.+?)">.+?</a></h3>', text)
    return urls


def cleaning(text):
    regTag = re.compile('<.*?>',flags = re.U|re.DOTALL)
    regEnds = re.compile('\r\n' ,flags = re.U|re.DOTALL)
    clean_t= re.sub('\xa0',' ', text)
    regScript = re.compile('<script>.*?</script>',flags = re.U|re.DOTALL) 
    regComment = re.compile('<!--.*?-->', flags = re.U|re.DOTALL)
    clean_t = regScript.sub("", text)
    clean_t = regComment.sub("", clean_t)
    clean_t = regTag.sub("", clean_t)
    clean_t = regEnds.sub(" ", clean_t)
    clean_t=html.parser.HTMLParser().unescape(clean_t)
    return clean_t

def writing(text):
    file = open('html.txt', 'w', encoding = 'utf-8')
    file.write(text)
    file.close()

def paragraphs(text):
    ready_text= re.findall('<p class="introtext">(.+?)<hr />', text, flags =re.DOTALL)
    ready_text = ''.join(ready_text)
    return ready_text

def words(text):
    clean_words = []
    words = text.split(' ')
    for word in words:
        word = word.lower()
        word = word.strip('.,?:()_-\r\n–«»...')
        clean_words.append(word)
    return clean_words

def frequency(array):
    d={}
    rare=[]
    for word in array:
        if word not in d:
            d[word] = 1
        else:
            d[word]+=1
    for key in d:
        if d[key]>1:
            rare.append(key)
    return rare

def sets(array):
    setfinal = set(array)
    return setfinal

def writing(text):
    file = open('words.txt', 'w', encoding='utf-8')
    file.write(text)
    file.close()


newsarray = finding(page_code('http://www.notum.info/tema/siriya'))
set_new = set()
set1= set()
set0=set()
set2=set()
common = []
difference = []
difference_rare=[]
for news in newsarray:
    array = words(cleaning(paragraphs(page_code('http://www.notum.info/' + str(news)))))
    if news == newsarray[0]:
        set0 = sets(array)
        set_rare0 = sets(frequency(array))
    elif news == newsarray[1]:
        set1 = sets(array)
        set_rare1 = sets(frequency(array))
    elif news == newsarray[2]:
        set2 = sets(array)
        set_rare2 = sets(frequency(array))
    else:
        continue          
set_final = set1 & set0 & set2
set_diff1 = set0^set1
set_diff2 = set1^set2
set_diff3 = set2^set0
set_diff = set_diff1|set_diff2|set_diff3

set_dif_rare1 = set_rare0^set_rare1
set_dif_rare2 = set_rare1^set_rare2
set_dif_rare3 = set_rare2^set_rare0
set_dif_rare = set_dif_rare1|set_dif_rare2|set_dif_rare3
for element in set_final:
    common.append(element)
for element in set_diff:
    difference.append(element)
for element in set_dif_rare:
    difference_rare.append(element)


writing('Слова, встречающиеся во всех новостных статьях по теме:' +'\n'+ '\n'.join(common) \
        + '\n'+ '\n' + 'Слова, не повторяющиеся более чем в одной статье:'+'\n'+ '\n'.join(difference) + '\n' + '\n'+ \
        'Слова, не повторяющиеся более чем в одной статье, с частотностью >=1:' + '\n'+ '\n'.join(difference_rare))
