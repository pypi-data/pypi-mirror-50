#### Tele
Telegram bot library.  

view [readthedocs](https://tele.readthedocs.io)  
[GitLab](https://gitlab.com/2411eliko/tele)  
[pypi](https://pypi.org/project/telepy/)  
##### Installation

requires python 3 + to run.

`pip3 install telepy`

```python 
from Tele import *


@bot('text')
def echo(update):
    update.reply(update.text)


account('TOKEN')
bot_run()

```
