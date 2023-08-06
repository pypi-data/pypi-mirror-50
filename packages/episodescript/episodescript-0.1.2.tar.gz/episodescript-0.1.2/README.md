episodescript
=============
[![travis](https://travis-ci.org/kota7/episodescript.svg?branch=master)](https://travis-ci.org/kota7/episodescript)[![pypi](https://badge.fury.io/py/episodescript.svg)](https://pypi.org/project/episodescript/)

Retrieve TV Show Scripts.


## Install

* From PyPi.

```bash
$ pip install episodescript
```

* Alternatively, recommended for Conda users.

```bash
$ conda install -y beautifulsoup4 'html5lib<1'
$ pip install episodescript --no-deps
```

* Alternatively, from GitHub.
```bash
$ git clone https://github.com/kota7/episodescript
$ pip install ./episodescript
```


## Use the console command

```bash
$ episode-script the-mentalist 2 6

TV show script for the-mentalist, Season 2, Episode 6
-------------------------------------------------
Black Gold and Red Blood
-------------------------------------------------
So we got Kirby Hines, 29-year-old.
 Local boy, welder.
...
```
  
Or, if you want to read lines step by step:
  
```bash
$ episode-script the-mentalist 2 6 | less
```

### Search the TV shows by keyword

Use `--search` option to search TV shows.

```bash
$ episode-script --search friends

* Searching TV shows with keyword `friends`...
9 match
                                      title |                                      id
 ------------------------------------------------------------------------------------
                Best Friends Forever (2012) |               best-friends-forever-2012
               Best Friends Whenever (2015) |              best-friends-whenever-2015
 Foster's Home for Imaginary Friends (2004) | fosters-home-for-imaginary-friends-2004
                                    Friends |                                 friends
                Friends from College (2017) |               friends-from-college-2017
                      Friends with Benefits |                   friends-with-benefits
           Friends with Better Lives (2014) |          friends-with-better-lives-2014
                   Just Good Friends (1983) |                  just-good-friends-1983
  Thomas The Tank Engine And Friends (1984) | thomas-the-tank-engine-and-friends-1984
 ------------------------------------------------------------------------------------
```



## Use in a python script

```python
>>> from episodescript import scrape_episode_scripts
>>> title, script = scrape_episode_scripts("sherlock", 1, 3)
>>> print(title)
The Great Game
>>> print(script)
Just tell me what happened
 from the beginning.

  We had been to a bar,
  nice place, and, er, I got chatting
  with one of the waitresses,
 and Karen weren't happy with that, so
....
```


## Note

This program relies on the website [TV Show Episode Script](https://www.springfieldspringfield.co.uk/tv_show_episode_scripts.php).
