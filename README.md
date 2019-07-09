![alt text](logo.png)
> Utility for dowloading blogs of various Japanese idols

## Table of Contents (Optional)

- [Requirements](#requirements)
- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation

### Clone

```shell
git clone https://github.com/iequivocality/bemiho.git
```

### Set-up

**Requirements**
- python 3.7

**Install virtualenvwrapper (Optional)**
- pip install virtualenvwrapper
- mkdir -p ~/Envs

- Add the following into your ~/.bash_profile file.
- export WORKON_HOME=~/Envs
- source /usr/local/bin/virtualenvwrapper.sh

**Re-open Terminal**
```shell
git clone https://github.com/iequivocality/bemiho.git
mkvirtualenv bemiho/
pip install -r requirements.txt
python bemiho.py
```

## Features
> ✔️ Supported content and groups

### Supported Groups
- Hinatazaka46

### Supported Content
- Photo download
- Blog download to .docx
- All download

## Usage
> 💎 How to get your idol photos, fast...

## Terminal Arguments

| Complete    | Shorthand | Function   |
| ----------- | --------- | ----- |
| --group     | -g        | Specifies group (required) |
| --member    | -m        | Specifies member of a group (required) |
| --output    | -o        | Specifies output folder where all contents are saved (default ./output) |
| --content   | -c        | Specified which data is fetched from content |
| --firstpage | -f        | Specified the first page from which data is fetched |
| --lastpage  | -l        | Specified the last page from which data is fetched, this will changed to page count |

## Contributing
> ⭐️ Starring this repository is enough. But, if you want to contribute...

### Step 1

- **Option 1**
    - 🍴 Fork this repo!

- **Option 2**
    - 👯 Clone this repo to your local machine using `https://github.com/iequivocality/bemiho.git`

### Step 2

- **HACK AWAY!** 🔨🔨🔨

### Step 3

- 🔃 Create a new pull request using <a href="https://github.com/iequivocality/bemiho/compare" target="_blank">`https://github.com/iequivocality/bemiho/compare`</a>.

## Future Development
- Adding other blogs Sakamichi groups and some chika idol groups
- Logging improvements
- Metadata for photo and blog data
- Selenium support for more complicated cases
