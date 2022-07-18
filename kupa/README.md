# kupa
vkrecepts in django

DONE:
	* client:
		* add
		* edit
		* img:
			* view
			* del
			* add
		* del:
			* images
	* record:
		* del
		* edit
	* calendar:
		* full

TODO:
	* index.date - onchange
	* client: sort.date
	* record: add (from client_view and index)
	Now: слева - клиент, справа - время, чуть ниже - длительность и описание. И педаль Создать

HOWTO:
	* on changing models:
		./manage.py makemigrations medrec
		./manage.py migrate
