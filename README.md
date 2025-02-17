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

Qwaver is already up and running on [qwaver.io](http://qwaver.io/ref/github).  (It's free)

If you want to run locally, copy the following and run it in your terminal:

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

When the server is running, go to [localhost](http://localhost:8000)

<div align="center">
<a href="http://qwaver.io/ref/github">
    <img src="http://qwaver.io/static/queries/images/three-screen-shots.jpg" alt="qwaver logo">
</a>
</div>

## Features

**Turning queries into parameterized tools**: The ability to turn queries into parameterized tools can be very useful,
as it allows you to reuse queries with different input parameters without having to rewrite the underlying SQL. This can
make it easier to use your queries in different contexts, and can help you to avoid making mistakes when modifying
complex queries.

**Automatically creating charts**: allows you to quickly visualize and understand your data. This can be particularly
useful if you are working with large or complex datasets, as it can help you to identify trends and patterns that may
not be immediately apparent from the raw data.

**Saving a history of query edits**: Being able to save a history of query edits can be very useful, as it allows you to
review and revert to previous versions of your queries if necessary. This can be especially helpful if you make a
mistake while editing a query, or if you need to compare different versions of a query to understand how it has evolved
over time.

**Saving a history of query results**: 
Some queries take hours or minutes to run.
Qwaver saves query results allowing you to easily see previous output.
This can be particularly useful if you are tracking changes in data over time, or if you are working with data that is
updated on a regular basis.

**Instant Pivot Charts**:

**CSV Table Loading**:
Save time and frustration by using Qwaver to load your CSV files into your database with ease.
Simply upload your CSV file and our tool will handle the rest, automatically creating a new table and importing all of the data from the file.
No need to worry about complex database schemas or manual data entry - Qwaver does all the heavy lifting for you.

**API**:  Qwaver makes it easy to turn your SQL queries into an API with no programming required.
When you save an SQL query you've made, Qwaver automatically creates an API endpoint.
If you added parameters to your query, those become the endpoint variables.

**Searchable queries**:  As a data scientist or analyst, you write hundreds of queries.
Qwaver's search tool makes finding the queries you need easy.

### Configurations

The above installation will run with default settings using a local sqlite database. However, if you'd like to run with
a different configuration:

Duplicate the file `settings-template.ini` in the `qwaver`
directory (the same directory that contains `settings.py`) and rename to
`settings.ini`. Update the settings for your particular environment..

## Intro video:

[![Qwaver Intro](http://img.youtube.com/vi/0jPneT1IkNI/0.jpg)](http://www.youtube.com/watch?v=0jPneT1IkNI "Qwaver Intro")

## Help!

Helping with this project will make you one of the cooler people that I know. How can I (meaning you) do that?

* Easy:  Give this project a ⭐️!
* Easy:  Kick the tires.  [qwaver.io](http://qwaver.io/ref/github) has the latest version running.
* Easy:  Fork the repo, edit this file (README.md) and make a PR to add any feature requests.
* Easy:  If you're in the code and see where something could be improved, but can't make the improvement right then,
  add  `# TODO` comment with a helpful description of what needs to be done and submit a PR.

### Feature requests

* add something!

#### Big, important things:

* JS charts on pages
* qwavers (esp. those with parameters) can be APIs as well
* Query collections -- user-defined lists of queries that all conform to a given topic
* "Starters": pre-defined sets of queries and collections if a database is for a common CMS
* "Linked collections". linked collections are all of queries that take exatly one parameter: the id of a related
  object.
* Badges for accomplishments -- eg. "creator", "pivoter", "chart master"
* EZ API
    * pretty API urls: qwaver.io/api/org-slug/query-name-slug
* User Stats:
    * Results are viewed per day
    * Results viewed per hour
    * Quarries made per day
    * Cruise made per hour
    * Total queries made
    * Total results are viewed
* permissions
    * Be able to add different db users to a given database: one that can alter on that can not
    * user permissions: org edit; DB edit; query edit, query create
    * user database permissions assigns to them the appropriate db user
* Database explorer:
    * list tables, list columns, list running queries, kill query
* Result differences
    * a user can can take the tables produced by two results and subtract them from each other. 
    * The above table difference works when the table has the same number of rows, when they have two columns, and when the second column is numeric.

#### Small but cool things:

* after the user signs up, the next screen is they accept a Terms of Service (apache 2.0)
* Add “read only“ user fuels to database set up.
* update success and error counts in results
* save exact query run with result; view that shows this
* track average execution time for queries
* have parent reference in queries.Query model (if the query was cloned from another)
* set query type to: automatic, table, bar chart, line chart, pie or pivot
* webpage preview when sharing results via slack or email (e.g. add open graph social previews to results. This will
  necessitate making an image url)
* flag queries -- if their results do not align with their title/description or are wrong in any other way
    * Search results should not include flagged queries
    * The author of a flagged query should be given an alert
* Add comments, likes, stars
* create 404 page
* creat easy way to leave feedback
* email verification
* parameters:
    * a country or date selector when param is {country} or {date}
    * For parameters set maximum and minimum and numeric values
* pre-populate for a new database two queries:
    * list public tables
    * list columns given a table name
    * list running queries
    * kill query
* list users in an organization
* automatically add a limit to every query
* disable queries; don't delete them
* https (helping set that on the DigitalOcean server)
* drop-down menu to select organization if there is more than one org for the user
* Have a result search where are the searches are the input fields for a given query. No search option if there are no input fields.
* A way to be able to combine search results from one database into the quarry of another. For example, one day the base returns IDs and the other query on a different database uses those IDs.
* Make hard-coded instances of "http://qwaver.io" from an environment variable
* as a person changes parameters, the API url updates
* On the query error page link to the GitHub issues page. Set up a default 500 error page during the same.
* For the database configuration, have both users be optional, but if there is not a loser who can alter tables, then certain functionality like load CSV will be off
* ability to make queries public (where the world can use them)
* deactivate queries, don't delete them
* limit CSV upload to MB and give warning if more than 1000 lines

### Issues:

* uploading files or profile images may overwrite each other with name collision
* buttons on clone page

### Video ideas:
* setting up a database with https://elephantsql.com/

### Efficiency:

* in query_version.py, make spans cover contiguous chaged characters, not individual characters

### General improvements

If you see any ways that the app could be improved in these ways, let's work on it!

* data security -- of paramount importance. In no way do we want a user to have access to data from an organization to
  which they do not belong
* HTML/CSS styling
* unit tests
* support for more databases

## Thank yous

* Much of the user management code has been based on the snippets made available
  by [Corey Schafer](https://github.com/CoreyMSchafer/code_snippets). He made
  an [excellent tutorial on learning Django](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)
  by walking through how to make a blog with many users. qwaver is basically a blog but for queries so it was a nice
  starting point!  

