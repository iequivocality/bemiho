# bemiho
Download utility for Japanese idols

**Requirements**
python 3.7

**Set-up**

**Install virtualenvwrapper**
- pip install virtualenvwrapper
- mkdir -p ~/Envs

- Add the following into your ~/.bash_profile file.
- export WORKON_HOME=~/Envs
- source /usr/local/bin/virtualenvwrapper.sh

**Re-open Terminal**
- git clone https://github.com/iequivocality/bemiho.git
- pip install -r requirements.txt
- python bemiho.py

**Terminal Arguments**

| Shorthand | Full        |       |
| --------- |:-----------:| -----:|
| -g        | --group     |       |
| -m        | --member    |       |
| -o        | --output    |       |
| -c        | --content   |       |
| -f        | --firstpage |       |
| -l        | --lastpage  |       |