### ИНФО
Телеграм бот для получения курса валют платёжной системы мир https://mironline.ru/

### Используемые библиотеки
pytelegrambotapi (telebot)<br/>
python-dotenv<br/>
beautifulsoup4<br/>
cachetools - для кэширования обращений к сайту<br/>


### Запуск

1) git clone https://github.com/glambary/MirCurrencyRateTelegramBot.git <br/>
2) cd MirCurrencyRateTelegramBot
3) на выбор Venv / Poetry

Через Venv:<br/>
python -m venv venv<br/>
pip install -r requirements.txt 

Через Poetry:<br/>
pip install poetry==1.5.1<br/>
poetry install --no-interaction