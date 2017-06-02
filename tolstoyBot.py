from pymorphy2 import MorphAnalyzer
import numpy as np
import json,telebot, conf, flask, re

# имя бота в телеграмм: @voina_i_mir_bot 

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)
morph = MorphAnalyzer()

def regex(word):
    word = re.findall('([.?!,:;]+)', word)
    sign = ''.join(word)
    return sign

def opening(path):
    file = open(path, "r", encoding = "utf-8")
    text = file.read()
    file.close()
    return text

def writing(text):
    file = open(r"/home/perugia/mysite/words_base.txt", "w", encoding = "utf-8")
    file.write(text)
    file.close

def matching(tags_lemma, tags_indeed):
    global morph
    dictionary_json = json.loads(opening(r"/home/perugia/mysite/words_base.txt"))
    if tags_lemma in dictionary_json:
        word_lemma =  str(np.random.choice(dictionary_json[tags_lemma], size=None, replace=True, p=None))
        word_lemma = morph.parse(word_lemma)[0]
        word_indeed = word_lemma.inflect(tags_indeed)
        if word_indeed == None:
            return "None"
        else:
            word_indeed = word_lemma.inflect(tags_indeed).word
            return word_indeed

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.send_message(message.chat.id, 'Привет, я бот, который переводит высказывание на язык Льва Толстого')

@bot.message_handler(func = lambda m: True)
def len_message(message):
    global morph
    message_out = []
    message_words = message.text.split(" ")
    for word in message_words:
        word_clean = word.strip(',!?./@%^:*_-+=<>|")\(')
        word_parsed = morph.parse(word_clean)
        word_lemma_tags = word_parsed[0].normalized.tag.cyr_repr
        word_real_tag = str(word_parsed[0].tag)
        tags = word_real_tag.split(',')
        set_tags = set()
        for tag in tags:
            tag=tag.split(' ')
            for tag_little in tag:
                set_tags.add(tag_little)
        word_out = matching(word_lemma_tags, set_tags)
        if word_out == "None":
            message_out.append(word+regex(word))
        else:
            message_out.append(word_out + regex(word))
    bot.send_message(message.chat.id,  (' ').join(message_out))

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
