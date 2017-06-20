import urllib.request, json, telebot, conf, flask
from telebot import types
import numpy as np


cq = []

def opening(path):
    file = open(path, "r", encoding = "utf-8")
    text = file.read()
    file.close()
    return text

def writing(text):
    file = open ("/home/milano/mysite/answers.txt", "w", encoding = "utf-8")
    file.write(text)
    file.close

# имя бота в телеграмм: @iomdin_bot

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.send_message(message.chat.id, 'Привет, я бот, который выдает тебе опросы Иомдина, вызывай комманду /play для нового опроса, /result для просмотра результатов!')

@bot.message_handler(commands=['play'])
def question(message):
    ids = []
    req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=17283336&count=100&access_token={}'.format(conf.ACCESS_TOKEN))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    for i in range(100):
        try:
            if str(data["response"][i]["attachments"][0]["type"]) == "poll":
                print(data["response"][i]["attachments"][0])
                ids.append(data["response"][i]["attachments"][0]["poll"]["poll_id"])
        except:
            continue
    print(ids)

    #выбираем рандомный

    id_quiz = np.random.choice(ids, size=None, replace=True, p=None)

    req = urllib.request.Request('https://api.vk.com/method/polls.getById?owner_id=17283336&poll_id={}&access_token={}'.format(str(id_quiz), conf.ACCESS_TOKEN))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    question = str(data["response"]["question"])
    print(question)
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    for i in range(len(data["response"]["answers"])):
        answer = str((data["response"]["answers"][i]["text"]))
        print(answer)
        bn = types.KeyboardButton(str(answer))
        keyboard.add(bn)
    bot.send_message(message.chat.id, question, reply_markup=keyboard)
    all_questions = json.loads(opening('/home/milano/mysite/answers.txt'))
    if question not in all_questions:
        all_questions[question] = {}
        cq.append(question)
    else:
        cq.append(question)
    writing(json.dumps(all_questions, sort_keys=True, indent=4))

@bot.message_handler(content_types=['text'])
def answer(message):
    text = message.text
    all_questions = json.loads(opening('/home/milano/mysite/answers.txt'))
    if text in all_questions[cq[0]]:
        all_questions[cq[0]][text] += 1
    else:
        all_questions[cq[0]][text] = 1
    cq.clear()
    writing(json.dumps(all_questions, sort_keys=True, indent=4, ensure_ascii=False))
    bot.send_message(message.chat.id, 'Ответ записан! Еще опрос /play ')

@bot.message_handler(commands=['result'])
def result(message):
    total_string = ''
    result = json.loads(opening('/home/milano/mysite/answers.txt'))
    for question in result:
            total_string+= str(question) +'\n\n'
            for answer in result[question]:
                total_string += str(answer) +  ": " + str(result[question][answer]) + '\n'
            total_string += "\n\n"
    bot.send_message(message.chat.id, total_string)

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

