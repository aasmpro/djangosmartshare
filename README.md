# smart_web_share
a simple django app for sharing files over http / https.

this app had been written with **Python 3.6** and **Django 2**

> attention :
>
> on test, not bug free.
> i just started this project for fun, so will be glad if you use and report issues on this project.

## Features
by this app, you can simply share any directory on your local system over http / https, in short : just like a file browser.

in `Location` model, by adding a new location, system will check if the path exist, so you can have following permissions separated for 3 different user types per each **Location** object. **Admins** , **Users** ( mean normal users ) and **Anonymouse Visitors** ( public ) :

> attention : 
> 1. if you share a directory, inside another shared directory, neither **Base Directory** nor **Sub Directory** will not change each other permissions. the deepest available **Sub Directory** Location object permissions will be used for each directory.
> 2. the root path **`/`** is not available.
> 3. only directories path are allowed to be shared, not files.
> 4. commands will run as logged-in user on local system, so even if a permission like **Can Delete** be **True**, on a directory that need superuser **sudo** permission, the command will not effect, for security reasons.

permission | description
------------|------------
Active | wheather to show this directory for the allowed user or not.
Show Files | user can view Files in directory. ( only view, nothing more )
Show Directories | user can view Directories in directory.
Show Hidden Files | same as Files, fore Hidden Files.
Show Hidden Directories | same as Directories, for Hidden Directories
Can Download | if this permission be `True`, user can download shared directory and it's subdirectories in compressed files as **zip**, **tar**, **tar.gz** and **tar.bz2**. an also user allowed to download any Files in directory and it's subdirectories.
Can Upload | if this permission be `True`, user can upload Files in directory and it's subdirectories.
Can Delete | if this permission be `True`, a **Delete** button will be showed for each subdirectories and files in directory, so user can delete them.
Can Create | if this permission be `True`, an **Add** button will be showed for Directories and Files, so user can add new directory, or a file with it's content.

this app have a simple responsive front-end design, created using **Bootstrap 4** framework. by default, needed static files are in `static/css` and `static/js` directories outside of app directory for avoiding duplication. if you are planning to uses this app make sure to include these files or replacing `share/templates/base.html` styles and scripts with **Bootstrap 4** SDN.

this users are added for testing :

username | password | is superuser
---------|----------|-------------
admin | adminadmin | yes
user | useruser | no

## TO DO
this Features are planned to be added in next version :
- [ ] adding **Run Command** ability.
- [ ] adding **Copy** and **Move**.
- [ ] adding **multi upload**.
- [ ] adding **multi selecting** files and directories ability for Download or Delete.
- [ ] adding **Preview** and **Edit** abilities.
- [ ] adding **permissions** for duplicated files and directories while adding or uploading.
- [ ] changing **dirs.html** template for adding **Upload**, **Delete**, **Add** forms.
- [ ] rewriting **views** definitions.
- [ ] rewriting responsive template for a better UX / UI.

## Runnig Project on local IP
the `runserver.py` file, will run the local test server of django on local ip and `8000` port.
django settings will automatically added your local IP to `ALLOWED_HOSTS`, just run this command in where main directory of project:
```
python3.6 runserver.py
```
