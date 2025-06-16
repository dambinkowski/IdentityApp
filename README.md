# CM3070 project


## Enviroment 
MacBook Pro 14-inch 2024 16GB/512GB  
macOS 15.4.1  
visual studio code 

### Installing Python 
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  
adding brew to path  
    echo >> /Users/d/.zprofile  
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/d/.zprofile  
    eval "$(/opt/homebrew/bin/brew shellenv)"  
brew install python  

which python3  
if developer tools version then change to brew by  
nano ~/.zprofile  
export PATH="/opt/homebrew/bin:$PATH"  
source ~/.zprofile  
python3 --version  
Python 3.13.3  
which python3  
/opt/homebrew/bin/python3  

### Setting django 
python3 -m venv venv  
source venv/bin/activate  
pip install django  
Successfully installed asgiref-3.8.1 django-5.2.1 sqlparse-0.5.3  

### Create Project 
django-admin startproject miamash

### Create App struccture
python manage.py startapp core
python manage.py startapp web
python manage.py startapp api 

### instal DRF (Django Rest Framework)
pip install djangorestframework 

### Superuser
python manage.py createsuperuser
root
test123123

