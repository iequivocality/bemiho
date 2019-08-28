![alt text](logo.png)
> Utility for dowloading blogs of various Japanese idols. Allows extraction for both photos and content.

> **Announcement**
> The following members will be removed by September as management
> will take down their respective blogs on August 30, 2019:
>       Nagahama Neru (Keyakizaka46)
>       Kakizaki Memi (Hinatazaka46)

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

- For Mac OSX:
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

### Supported Groups (-g or --group)
- Hinatazaka46 (日向坂46)
- Keyakizaka46 (欅坂46)
- Nogizaka46 (乃木坂46)
- The World Standard (わーすた)
- Niji no Conquistador (虹のコンキスタドール)

### Supported Content (-c or --content)
- Photo download (photos)
- Blog download to .docx (blog)
- Text only (without HTML tags and images) to .txt (no_html)
- All download (all)

## Usage
> 💎 How to get your idol photos, fast...

## Terminal Arguments

| Complete    | Shorthand | Function   |
| ----------- | --------- | ----- |
| --group     | -g        | Specifies group (required) |
| --member    | -m        | Specifies member of a group (required) |
| --number    | -n        | Number of pages needed to save |
| --output    | -o        | Specifies output folder where all contents are saved (default ./output) |
| --content   | -c        | Specified which data is fetched from content |
| --firstpage | -f        | Specified the first page from which data is fetched |
| --lastpage  | -l        | Specified the last page from which data is fetched, this will changed to page count |
| --list      |           | Lists all groups and supported members |
| --reset     |           | Resets saved data from idol's blog |

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
- Extracing blogs from LINE for individual members
- Extracting blogs from Ameblo (both groups and individual groups)
- Allow re-download through only metadata
- Selenium support for more complicated cases (such as adding Twitter support)
