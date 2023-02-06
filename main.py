import requests
from bs4 import BeautifulSoup
from telebot import TeleBot

bot = TeleBot(input("Enter token: "))


def extract_arg(arg):
  return arg.split()[1:]


@bot.message_handler(commands=['start'])
def start_message(message):
  text = 'Привет! \nЭто бот для удобного просмотра тегов работ с площадки artfinder.com. ' \
         '\n\n - cкопируй ссылку на художника, например: ' \
         '\nhttps://www.artfinder.com/artist/magdalena-morey/' \
         '\n - напиши каманду /artist и вставь ссылку, вот так: ' \
         '\n/artist https://www.artfinder.com/artist/magdalena-morey' \
         '\n\n Попробуй'
  bot.send_message(message.chat.id, text, disable_web_page_preview=True)
  bot.send_message(message.chat.id,
                   "/artist https://www.artfinder.com/artist/magdalena-morey",
                   disable_web_page_preview=True)


@bot.message_handler(commands=['art'])
def start_art(message):
  print(message.chat.id)
  link = extract_arg(message.text)
  get_products(link[0], message.chat.id)
  bot.send_message(message.chat.id, "Это все работы художника.")


@bot.message_handler(commands=['artist'])
def start_artist(message):
  print(message.chat.id)
  link = extract_arg(message.text)
  get_products(link[0], message.chat.id)
  bot.send_message(message.chat.id, "Это все работы художника.")


def show_tags(link, chat):
  cont = requests.get(link)
  s = BeautifulSoup(cont.text, 'html.parser')
  q = s.find_all('span', class_='badge badge-light')
  s = link + ' '
  for t in q:
    s += t.text + ' '
  bot.send_message(chat, s)


def get_products(link, chat):
  url = link + '/page-'
  count = 0
  while True:
    count += 1
    get = requests.get(url + str(count))
    if get.status_code == 200:
      soup = BeautifulSoup(get.text, 'html.parser')
      quotes = soup.find_all('div', class_='product-card')

      for q in quotes:
        a = q.find_all('a')
        show_tags('https://www.artfinder.com' + a[0]['href'], chat)
    else:
      break


print('Runing...')
bot.polling()
