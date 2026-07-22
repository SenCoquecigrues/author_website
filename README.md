# Site d'autrice

1. [Using the app locally](#local-use)
   - [Installing the app](#installing)
   - [Launching the app](#launching)
   - [Good practices](#good-practices)
2. [Setting the app in o2switch (our heberger)](#setting-the-app-in-o2switch)
3. [TO-DO](#to-do)
   - [Must-have](#must-have)
   - [Nice to have](#nice-to-have)
   - [Last priority](#last-priority)
4. [Useful commands](#useful-commands)
5. [Credits](#credits)
6. [Random notes](#random-notes)


## LOCAL USE

### Installing
This app was tested with Python 3.11, Python 3.12.3 and Python 3.14. 
Other versions were not tested.

FOR UNIX : navigate to the project's root folder from your command line
 interface, then run:

``` bash
# Create a virtual environment with the command:
python -m venv venv

# Activate it
source venv/bin/activate

# Install necessary packages:
pip install -r requirements.txt
```

Then, run:
``` bash
# Create migrations, i.e. ORM-generated files.
# pay attention that the folder migrations should exists inside each app folder
# its being ignored by git (see .gitignore file)
# can cause issues like: 
# 'CommandError: Unable to serialize database: no such table: voiture_noire_discordprofile'
python manage.py makemigrations
python manage.py migrate

# Create your superuser, i.e. your admin profile.
# Do not put in a real mail address.
python manage.py createsuperuser --username=jean --email=jean@example.com
```

Using the model shown in .env.dist, create your .env file.

Using the model shown in utils/json/author_profile.json.dist, create 
your author_profile.json file.

You can now launch the app!

### Launching
``` bash
python manage.py runserver
```

Boom.

The app should be launched from `http://127.0.0.1:8000/`; you can go to 
`http://127.0.0.1:8000/admin/` for admin options.

### Good practices
**We try to preface commits with "feat", "fix", or "chore"** for clarity's sake. Do let me know 
if you have other preferences.

**We use [PEP 8](https://peps.python.org/pep-0008/) for Python**. 
We use [Ruff](https://docs.astral.sh/ruff/installation/) as our linter/formatter.

**There are tests available**, though not all pages or functions are tested because the tests were 
added late and this is done with my spare energy and/or I'm a terrible human being.

## Setting the app in o2switch
### Package

Pick the latest version of Python.

> pip install -r requirements.txt
> pip install mysqlclient.

Indicate core/wsgi.py as the entrance point of your app.

Check that all migrations are applied.

### Change staticfiles (images, CSS, etc)
1. Run `python manage.py collectstatic`
2. Restart the app

### When making changes
1. If on the front end: run `python manage.py collectstatic`, then restart
2. If involving models: run migrations


## TO-DO (v. 0.7)
### Road to 0.721: improve error handling when posting story
- [STORIES] Redirect toward posted story
- [STORIES] Redirect toward posted chapter


### Must-have
- [WRITER] Add buttons to filter rants
- [ARCHIVES] Post : preview fic
- [STORIES] Ensure automatic ebook folder cleaning up, just in case
- [STORIES] Tests exports with test text. Try saying that many times very quickly
- [STORIES] Fix clap button
- [STORIES] Bigger emojis?
- [STORIES] Better way for authors to know which reactions were shown for which chapter
- [STORIES] Better story_card element display flexibility
- [STORIES] Add PDF support for multiple chapters
- [STORIES] Post comment (ongoing: lacking view + checks)
- [STORIES] Delete chapter
- [STORIES] User Comment
- [STORIES] Add PDF thanks to [this library](https://www.geeksforgeeks.org/creating-ebooks-with-borb-in-python/).
available [here](https://github.com/jorisschellekens/borb?tab=readme-ov-file). Instruction book can be found
[here](https://github.com/jorisschellekens/borb-examples/tree/master/chapter_001).

### Nice to have
- [STORIES] Add settings buttons to stories themselves
- [STORIES] Custom covers
- [PROMPTS] Search prompts through text
- [STORIES] Replace ratings as instances by rating as choices? 

### Quickwins
- [STORIES] Improve story button display on very small screens

### Last priority
- [PINE] (Mobile) : Rearrange banner
- [PINE] (Mobile) Mobile : 50 % of page as a mosaic
- [PINE] (Computer) Commissions : final page
- [PINE] (Mobile) Commissions : final page
- [PROMPTS] Properly implement [error messages](https://docs.djangoproject.com/en/5.1/ref/contrib/messages/)

### Version 0.72 : adding Epub fic exports
- [STORIES] Save epubs
- [STORIES] Send epubs
- [STORIES] Upon export error, send a 'sorreh ):' txt.
- [STORIES] Add AND format front buttons for epub exports
- [STORIES] Change TOC name. **WARNING**: had to customize the library for that one. We will need to create a library fork.

### Version 0.71 : adding HTML fic exports
- [STORIES] Add HTML support for oneshots
- [STORIES] Add HTML support for multiple chapters
- [STORIES] Add table of content for multi-chapters things
- [STORIES] Add AND format front buttons for html exports

### Version 0.7 : adding reaction and clapping
- [STORIES] User Clapping (calling back)
- [STORIES] User Clapping (user see interaction)
- [STORIES] User Reactions: functional back calls
- [STORIES] User Reactions: selected reactions show up on loading
- [STORIES] User Reactions: selected reactions show up on change
- [STORIES] Author can see number of claps per stories
- [STORIES] Author can see reactions per story


## Useful commands
To use Ruff, our linter/formatter:
```python
ruff check   # Lint all files in the current directory.
ruff format  # Format all files in the current directory.
```

To run the tests specific to one particular TestCase:
`python manage.py test tests.accounts.test_birthdays`
`python manage.py test tests.archives.ArchivesIndexTestCase`

(In prod) To run statics and clear them, in case the files got corrupted (don't forget to restart afterwards!):
`python manage.py collectstatic --clear`

To export the db, app by app, into a json format suitable for fixture:
`python manage.py dumpdata voiture_noire --settings=core.settings > voiture_noire/fixtures/voiture_noire.json`


## Code credits
[Rich text editor](https://codepen.io/BibekOli/pen/abRgbVW)


## Random notes
[CONVERT HTML TO PDF](https://doc.courtbouillon.org/weasyprint/stable/)

[CONVERT HTML TO PDF - PYTHON](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#python-library) => note que y a un argument pour gérer les pages !!

[pdf WITH A PAGE-AT RULE](https://developer.mozilla.org/en-US/docs/Web/CSS/@page)

[BIBLIOTHÈQUE POUR RACCOURCIS](https://www.npmjs.com/package/hotkeys-js)

[PLAY A SOUND WHEN KEY IS PRESSED](https://stackoverflow.com/questions/12578379/play-a-sound-when-a-key-is-pressed)

[INSTANCE OF RICH TEXT EDITOR](https://codingtorque.com/rich-text-editor-using-javascript/)

