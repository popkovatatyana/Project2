
# coding: utf-8

# In[61]:

import urllib.request, json, telebot, conf, flask, re
from telebot import types
import numpy as np

def opening(path):
    file = open(path, "r", encoding= "utf-8")
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

#здесь мы выделяем опросы с страницы Иомдина

# req = urllib.request.Request('https://api.vk.com/method/wall.get?owner_id=17283336&count=100&access_token={}'.format(conf.ACCESS_TOKEN))
# response = urllib.request.urlopen(req) 
# result = response.read().decode('utf-8')
# data = json.loads(result)
# for i in range(50):
#     try:
#         if str(data["response"][i]["attachments"][0]["type"]) == "poll":
#             print(data["response"][i]["attachments"][0])
#     except:
#         continue


app = flask.Flask(__name__)      

@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    bot.send_message(message.chat.id, 'Привет, я бот, который выдает тебе опросы Иомдина, вызывай комманду /play для нового опроса')

@bot.message_handler(commands=['play'])
def question(message):
    #полученные айди опросов:
    ids = [256179179, 255234161, 241773314, 239179729, 232090487, 217357533]
    all_questions = {}
    
    #выбираем рандомный 
    
    id_quiz = np.random.choice(num, size=None, replace=True, p=None)
    
    #Дело в том, что я не могу получить доступ к опросам из-за нововведений вк. 
    #Я пыталась получить код доступа и на друзей и на стену, но он все равно не дает к ним доступ... 
    
    req = urllib.request.Request('https://api.vk.com/method/polls.getById?owner_id=2314852&poll_id={}&access_token={}'.format(str(id_quiz), conf.ACCESS_TOKEN))
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    data = json.loads(result)
    question = str(data["response"]["question"])
    print(question)    
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    for i in range(len(data["response"]["answers"])):
                answer = str((data["response"]["answers"][i]["text"]))
                answer = types.KeyboardButton(answer)
                keyboard.add(answer)
    
    #Записываем ответ в базу данных
    all_questions = json.loads(opening('/home/milano/mysite/answers.txt'))
    if question not in all_question:
        all_questions[question] = []
        all_questions[question].append(message.text)    
    else:
        all_questions[question].append(message.text)  
    writing(json.dumps(all_questions, sort_keys=True, indent=4))
    bot.send_message(message.chat.id ,question,reply_markup=keyboard)
    

@app.route('/', methods=['GET', 'HEAD'])
def index():
    #не смогла выставить результаты на PAW, потому что постоянно всплывала ошибка с render_template
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



# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[4]:

import urllib.request, json, telebot, flask, re
from telebot import types


result


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



