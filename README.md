<div align="center">
  <a href="http://qwaver.io/ref/github">
    <img src="http://qwaver.io/static/queries/images/qwaver-header.jpg" alt="qwaver logo">
  </a>

**Turn queries into easy-to-use tools your teammates can share.**

Parameterize! Visualize! Collaboratize?!

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![master passing](https://github.com/brianrisk/qwaver/actions/workflows/unit-test.yml/badge.svg?branch=master)
[![Join the chat at https://gitter.im/qwaver-io/community](https://badges.gitter.im/qwaver-io/community.svg)](https://gitter.im/qwaver-io/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
<a href="https://github.com/brianrisk/qwaver/graphs/contributors">
<img src="https://img.shields.io/github/contributors/brianrisk/qwaver.svg">
</a>

[Latest Build](#latest-build) •[Use Cases](#use-cases) • [Help!](#help) • [Installation](#installation)
• [Thanks](#thank-yous)

<a href="http://qwaver.io/ref/github">
    <img src="http://qwaver.io/static/queries/images/screen-record-2.gif" alt="qwaver logo">
</a>

</div>

## Latest Build

The latest code is running at [QWAVER.io](http://qwaver.io/ref/github)

## Installation

Qwaver is already up and running on [qwaver.io](http://qwaver.io/ref/github). (It's free)

If you want to run it locally, copy the following and run it in your terminal:

```bash
git clone https://github.com/brianrisk/qwaver.git
cd qwaver
pip3 install -r requirements.txt
python3 manage.py collectstatic --no-input
python3 manage.py makemigrations users
python3 manage.py makemigrations queries
python3 manage.py migrate
python3 manage.py runserver
```

Once the server is running, go to [localhost](http://localhost:8000) in your browser.

<div align="center">
<a href="http://qwaver.io/ref/github">
    <img src="http://qwaver.io/static/queries/images/three-screen-shots.jpg" alt="qwaver logo">
</a>
</div>

## Features

**Parameterized Query Tools** <br>
Add new input parameters to your queries without having to rewrite the underlying SQL. This makes it easier to use your queries in different contexts, and helps you to avoid making mistakes when modifying complex queries.

**Automatic Charts** <br>
Quickly visualize and understand your data. This is particularly useful if you work with large or complex datasets, as you can identify trends and patterns that may
not be apparent in the raw data.

**Query Edit History** <br>
Save a history of your query edits and parameters, allowing you to
review and revert to previous versions of your queries if necessary. This can be especially helpful if you make a
mistake while editing a query, or if you need to compare different versions to understand how a query evolved over time.

**Query Result History** <br>
Some queries take hours or minutes to run. Qwaver allows you to easily see previous outputs that led you to your current analysis. This can be particularly useful if you are tracking changes in data over time, or if you are working with data that is updated on a regular basis.

**CSV Table Loading** <br>
Save time and frustration by using Qwaver to load your CSV files into your database with ease. Simply upload your CSV file and our tool will handle the rest, automatically creating a new table and importing all of the data from the file.
No need to worry about complex database schemas or manual data entry - Qwaver does all the heavy lifting for you.

**API** <br>
Qwaver makes it easy to turn your SQL queries into an API with no programming required.
When you save a SQL query, Qwaver automatically creates an API endpoint.
If you added parameters to your query, those become the endpoint variables.

**Searchability** <br>
As a data scientist or data analyst, you write hundreds of queries.
Qwaver's search tool makes it easy to finding the ones you need.

## Configurations <br>

The above installation will run with default settings using a local SQLite database. However, if you'd like to run it with
a different configuration:

Duplicate the file `settings-template.ini` in the `qwaver`
directory (the same directory that contains `settings.py`) and rename to `settings.ini`. Update the settings for your particular environment..

## Video

[![Qwaver Intro Video](http://img.youtube.com/vi/0jPneT1IkNI/0.jpg)](http://www.youtube.com/watch?v=0jPneT1IkNI "Qwaver Intro Video")

## Help!

Helping with this project will make you one of the cooler people that I know. How can I (meaning you) do that?

* Easy:  Give this project a ⭐️!
* Easy:  Kick the tires.  [qwaver.io](http://qwaver.io/ref/github) has the latest version running.
* Easy:  Fork the repo, edit this file (README.md) and make a PR to add any feature requests.
* Easy:  If you're in the code and see where something could be improved, but can't make the improvement right then,
  add  `# TODO` comment with a helpful description of what needs to be done and submit a PR.

### Video ideas:
* Setting up a database with https://elephantsql.com/


See `feature_requests.md` to look at ongoing requests or add your own!

## Thank Yous

* Much of the user management code has been based on the snippets made available
  by [Corey Schafer](https://github.com/CoreyMSchafer/code_snippets). He made
  an [excellent tutorial on learning Django](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)
  by walking through how to make a blog with many users. qwaver is basically a blog but for queries so it was a nice
  starting point!  
* Styling on the main page from the free templates at [Html5Up](https://html5up.net/)
