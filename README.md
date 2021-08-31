# PowerX Vehicle Rental
Final Project for the subject Fundamentals in Python (Intermediate) in PowerX Program

- Contributors: [Muhammad Azmi Zainudin](https://github.com/azkmee)

- Evaluators: Oka Kurniawan, Kenny Choo

Software Documentation: <a href="docs/html-docs/index.html" target="_blank">Click Here</a>

## Setup

### Install Git

You need to have Git to do the project. Download and install the software according to your OS:

- Windows: [Git for Windows](https://git-scm.com/download/win)
- Mac OS: [Git for MacOS](https://git-scm.com/download/mac)

### Downloading Repository and enter into folder

Clone the mini project repository from Github. On your terminal or Git Bash, type the following:

```shell
$ git clone git@github.com:AlkaffAhamed/PowerX-Vehicle-Rental.git
$ cd PowerX-Vehicle-Rental
```

### Create Virtual Environment

**You should open Anaconda Prompt to do the following steps.**

Go to the root folder `PowerX-Vehicle-Rental`.

```shell
> cd %USERPROFILE%\PowerX-Vehicle-Rental    <- Windows
$ cd ~/PowerX-Vehicle-Rental                <- MacOS/Linux
```

From the root folder, i.e. `mp_sort`, create virtual environment called `virtenv`.

```shell
$ python -m venv virtenv
```

A folder called `virtenv` will be created. Now, activate the virtual environment.

```shell
> virtenv\Scripts\activate      <- Windows
$ source virtenv/bin/activate   <- MacOS/Linux
```

You should see the word `virtenv` in your prompt something like:

```shell
(virtenv) folder>     <- Windows
(virtenv) user$       <- MacOS/Linux
```

_To exit the virtual environment at the end of this mini project, simply type:_

```shell
> deactivate
```

### Install Python Packages

Install the necessary packages for this mini project. From the root folder, i.e. `mp_sort`, type the following:

For Windows:

```shell
> pip install -U --force-reinstall -r requirements.txt
```

For MacOS/Linux: (For Linux, you might need to type pip3 instead)

```shell
$ pip install -U --force-reinstall -r requirements.txt
or
$ pip3 install -U --force-reinstall -r requirements.txt
```

The above steps will install the following packages:

- Flask
- Transcrypt 
- Flask-SQLAlchemy
- Flask-Migration
- Flask-Bootstrap
- and some other packages

## Compiling and Running

### Compile `clientlibrary.py` 

**Make sure you have:** 

1. **Activated** your Virtual Environment 
2. **Installed** the libraries in `requirements.txt`

Go to the root folder `PowerX-Vehicle-Rental`.

```shell
> cd %USERPROFILE%\PowerX-Vehicle-Rental    <- Windows
$ cd ~/PowerX-Vehicle-Rental                <- MacOS/Linux
```

Now, we can go to the location of `clientlibrary.py` under `app/static/`.

```shell
$ cd app/static
```

Type the following:

```shell
$ python -m transcrypt -b clientlibrary.py
```

Make sure you see the the `__target__` folder created successfully. You can check by typing: `ls` command

### Database Migrations 

Go to the root folder `PowerX-Vehicle-Rental`.

```shell
# If you are in app/static/
cd ../../

# Otherwise
> cd %USERPROFILE%\PowerX-Vehicle-Rental    <- Windows
$ cd ~/PowerX-Vehicle-Rental                <- MacOS/Linux
```

You should see `application.py` in this root folder. Run the following commands:

```shell
$ flask db init
$ flask db migrate
$ flask db upgrade
```

You should see a file called `app.db` and a folder `migrations`. 

### Running the program 

**Make sure you have:** 

1. **Compiled** `clientlibrary.py`  into the JavaScript file
2. **Database Migration** successfully completed

Go to the root folder `PowerX-Vehicle-Rental` and run the command below: 

```shell
$ flask run
```

An output similar to below will be produced: 

```shell
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Open any browser and copy paste the URL (this case, it is `http://127.0.0.1:5000/`)

