# ntfb 
A notification bot for running python functions or code blocks, requiring a telegram bot token and chatID.


## Usage

Create a bot through telegram, get its token and chatid.

Set env variables:

~~~zsh
export JUPYBOT_TOKEN='yourtoken'
export JUPYBOT_CHATID='yourchatid'
~~~

Install [ntfb](https://pypi.org/project/ntfb/):

~~~zsh
pip install ntfb
~~~

Use it in the end of code blocks or as a decorator:

~~~python
from ntfb import NtbMark
from ntfb import NtfBot

@NtbMark
def add(x,y):
    return x+y

add(1,1)
nb = NtfBot()
nb('hello')
~~~