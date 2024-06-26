## Project_Management_Api

First, create a folder on your computer. Then open a terminal to that folder.
<br>
### Spet 1:
Now, clone the repository by using:
```
git clone https://github.com/salmanfarshy/Project.git
```
Then, create an `env` file by using:
```
python -m venv env
```
And active the file by using

For Windows
```
.\env\Scripts\activate
```
For Linux/Mac
```
source env/bin/activate
```
or
```
source env\bin\activate
```
Now, install some libraries by using:
```
pip install django djangorestframework djangorestframework-simplejwt
```
<br>

### Spet 2:
Now, relocate to the `Project` folder by using:
```
cd Project
```
Now, migrate the database by using:
```
python manage.py migrate
```
Finally, run the server by using:
```
python manage.py runserver
```

Now, to play with these APIs follow the link below.
- https://docs.google.com/document/d/1aoN-ar2vsoaM0u-aIYEhzw1GPOd_Wy1mfeBWWDzoccA/edit?usp=sharing
