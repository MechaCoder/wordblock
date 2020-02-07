# WordBlock

## Motivation

WordBlock is an app that works is a very similar way, another property app word bar, but this is built using completely different technology and meant to be more open and more 'hackable'.

## Build status

### V1.2

* Unittesting Framework added.
* Screen Manager introduced.
* tided up the modual.
* added a setting panels to make Create and delete functions.
* added a defeault URL for first use.
* added a new setting that allows users to set eather all caps and lower.
* I removed the game clock becouse it killed app proformance
* the display words are now weighted to provide to provide a weighting to words the users have used before

### v1.3

* Proformace has been imporved.
* added a more intellgent window width
* bug fixs and improvesments

### v1.4

* You can know edit the weighting of words enableing you to custom which words come up first.
* the importer for webpages has now been changed to be asyncs.
* A new deploy script to automate the release cycle.

### v1.5

* there was an error in the build projects that now this problem has be sorted.
* a popUp to inform the use when the url import has finished
* I have added a new shearch fuction to the edit menu that greatly improves the proformace of the Application.
* Ad i have added a splah screen to improve the welcomeing experience.

## Code style

useing standard `flake8`

### built with

* Python3.7
* Kirvy Gui Framework
* TinyDB
* beautifulsoup 4
* fuzzywuzzy
* pyttsx3

### How to run

#### 1 - From Repo

if you useing the repo then the project's dependcy are useing pipenv, to run simply run run `pipenv install` and `pipenv run run`. if you see an error you can get a tutoral [here](https://www.youtube.com/watch?v=zDYL22QNiWk)

#### 2 - From installer

you can also run `pipenv run build`. that will build the project, as an installer this means that you should be able to run the project as a single file. i recermend that you do this on the system you want use it on.
