slovastick_app
==============
Research in the perception of sound information based on the Braille


demo site ---> http://словастик.рф
(after slash pass some text, for example: http://словастик.рф/abcde12345абвгд) 


Main goal of this project is create sound system for information translation, 
which will be easier in realisation than speech synthesis,
will have the ability to transmit characters alphabets of different countries
and one, universal representation for repetitive signs.

If you have some good idea and demonstration of its,
please write to me: slovastick@mail.ru


Install application:

*	Install Django 1.4, csound, sox

*	Install this Django application by using "python setup.py install", 
	or copy slovastick_app to your Django project folder

* 	Download static files from link and copy to project:
	https://www.dropbox.com/sh/ytej1rcmao4c7nj/rWUqZCYWmy

*	Add slovastick_app to your Django project in settings.py

*	include 'slovastick_app.urls' in urls.py of Django project