# university-PC
Group project for university.

# Requirements
- Python >= 3.4 https://www.python.org/downloads/
- Git https://confluence.atlassian.com/bitbucket/set-up-git-744723531.html

# Install
## Linux (UNIX systems)
1. Clone the repository and change into it:
`git clone https://github.com/leyyin/university-PC.git && cd university-PC`

2. Create virtual environment:
`virtualenv -p /usr/bin/python3 env`

3. Activate environment:
`source env/bin/activate`

4. Install requirements:
`pip install -r requirements.txt`

See `Common steps` below.

## Windows
It is recommend to use the PowerShell command line in windows. (included by default from Windows 7)

1. Clone repository http://www.thegeekstuff.com/2012/02/git-for-windows/ and change into it with PowerShell.
2. Create virtual environment:
`python3 -m venv env`

3. Activate environment (assumes you have PowerShell, if not see [alternatives](https://docs.python.org/3.4/library/venv.html#creating-virtual-environments)):
`env/Scripts/Activate.ps1`

4. Install requirements:
`pip install -r requirements.txt`

See `Common steps` below.

## Common steps
5. Copy `elearning/settings_local.EXAMPLE.py` to `elearning/settings_local.py` and edit the settings to match your 
environment:
`cp elearning/settings_local.EXAMPLE.py elearning/settings_local.py`

6. Create your database tables (you must do this every time you change the models):
`python manage.py migrate`

# Run
WARNING!!! Be sure your virtual environment is activated.
Command:
`python manage.py runserver`


# Contributing

See Django 1.8 docs https://docs.djangoproject.com/en/1.8/ and the specification from the `doc/` directory inside this 
repository.
