# Site d'autrice

1. [Using the app locally](#local-use)
   - [Installing the app](#installing)
   - [Launching the app](#launching)
   - [Linting and testing](#linting-and-testing)
   - [Good practices](#good-practices)
2. [Setting up the app in o2switch (our heberger)](#setting-the-app-in-o2switch)
3. [TO-DO](#to-do)
   - [Must-have](#must-have)
   - [Nice to have](#nice-to-have)
   - [Last priority](#last-priority)
4. [Version history](#version-history)
5. [Useful commands](#useful-commands)
6. [Credits](#credits)
7. [Random notes](#random-notes)


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

### Linting and testing
To use Ruff, our linter/formatter:
```bash
ruff check   # Lint all files in the current directory.
ruff format  # Format all files in the current directory.
```

To use Django's integrated Unittest implementation:
```bash
python manage.py test tests # all tests
python manage.py test tests.accounts.test_birthdays # a specific TestCase
python manage.py test tests.archives.ArchivesIndexTestCase # a specific TestCase (bis)
python manage.py test tests.archives.ArchivesIndexTestCase.test_cannot_access_private_story # a specific test
```

To use coverage so as to get a report about test coverage:
```bash
python -m coverage run manage.py test
# Then, to get a detailled report:
python -m coverage html
```

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


## TO-DO (v. 0.723)
### Road to 0.724:
- [QUALITY] ProfilePostTestCase to complete
- [QUALITY] Commit hook to run tests for modified files only?
- [QUALITY] Warn if coverage level lowered?
- [STORIES] Update test for editing and publishing chapters
- [STORIES] Tests exports with test text. Try saying that many times very quickly

### Road to 0.8: various fixes
- [STORIES] Add detailled error return when a form is invalid (chapter, story)
- [STORIES] Bigger emojis?
- [STORIES] Better story_card element display flexibility
- [STORIES] Better way for authors to know which reactions were shown for which chapter (perhaps chapter number?)
- [STORIES] Improve story button display on very small screens
- [STORIES] Fix clap button

### Must-have
- [ARCHIVES] Post : preview fic
- [STORIES] Ensure automatic ebook folder cleaning up, just in case
- [STORIES] Post comment (ongoing: lacking view + checks)
- [STORIES] User Comment
- [WRITER] Add buttons to filter rants

### Nice to have
- [STORIES] If reacting fails, a small error message
- [STORIES] Add settings buttons to stories themselves
- [STORIES] Custom covers
- [PROMPTS] Search prompts through text
- [STORIES] Replace ratings as instances by rating as choices? 

### Last priority
- [PINE] (Mobile) : Rearrange banner
- [PINE] (Mobile) Mobile : 50 % of page as a mosaic
- [PINE] (Computer) Commissions : final page
- [PINE] (Mobile) Commissions : final page
- [PROMPTS] Properly implement [error messages](https://docs.djangoproject.com/en/5.1/ref/contrib/messages/)

## Version history
### 0.723: improve archives test cover
- [QUALITY] Add Voiture Noire Prompts tests
- [QUALITY] Handle Story visibility tests
- [QUALITY] More chapter tests
- [QUALITY] More stories tests
- [QUALITY] More reaction + clapping tests
- [QUALITY] Various test improvements
- [STORIES] Fix future chapter visibility (front & back)
- [STORIES] Fix delete URL ambiguity
- [STORIES] Unlogged users can't see the reaction buttons anymore

### 0.722: improve test cover
- [QUALITY] Add Coverage
- [QUALITY] Configure Coverage
- [QUALITY] Add Writer tests
- [QUALITY] Add Gadget tests

### Version 0.721: make posting more convenient (part 1)
- [STORIES] Redirect toward posted story
- [STORIES] Redirect toward posted chapter

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
(In prod) To run statics and clear them, in case the files got corrupted (don't forget to restart afterwards!):
`python manage.py collectstatic --clear`

To export the db, app by app, into a json format suitable for fixture:
`python manage.py dumpdata voiture_noire --settings=core.settings > voiture_noire/fixtures/voiture_noire.json`


## Code credits
[Rich text editor](https://codepen.io/BibekOli/pen/abRgbVW)

[PLAY A SOUND WHEN KEY IS PRESSED](https://stackoverflow.com/questions/12578379/play-a-sound-when-a-key-is-pressed)
