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

| Complete    | Shorthand |       |
| ----------- | --------- | ----- |
| --group     | -g        |       |
| --member    | -m        |       |
| --output    | -o        |       |
| --content   | -c        |       |
| --firstpage | -f        |       |
| --lastpage  | -l        |       |