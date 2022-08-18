<div align="center">
  <a href="https://qwaver.io">
    <img src="https://qwaver.io/media/qwaver-header.jpg" alt="qwaver logo">
  </a>

**Turn queries into easy-to-use tools your teammates can share.**

Parameterize! Visualize! Collaboratize?!

[![Join the chat at https://gitter.im/qwaver-io/community](https://badges.gitter.im/qwaver-io/community.svg)](https://gitter.im/qwaver-io/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
<a href="https://github.com/brianrisk/qwaver/graphs/contributors">
<img src="https://img.shields.io/github/contributors/brianrisk/qwaver.svg">
</a>

qwaver links: [Intro](#the-fascinating-story) • [Help!](#help) • [Installation](#installation) • [Thanks](#thank-yous)

<a href="https://qwaver.io">
    <img src="https://qwaver.io/media/three-screen-shots.jpg" alt="qwaver logo">
  </a>
</div>

## The Fascinating Story
If you're like me, you have hundreds of queries stored in your DB admin tool for several connected DBs. A lot your time
is spent searching through them, altering WHERE clauses, exporting the results, plotting charts, and emailing the
results (chart + data + query for validation). Often you've got others on your team doing the exact same thing
re-inventing the wheel left and right.

Then this happens:

Boss: Hey, do you have time for business question involving our database?

You: Sure!  Give me 20 minutes..

17 minutes later...

You: Here you go!  See attached chart and data!

Boss: Thanks!  could you do like 100 similar variations with different time periods and countries?

Your skills as a query artist were definitely needed that first time, but the second time the need comes from that
person you're helping not having any experience with queries at all.

* **Q:** Don't other tools out there help with this?
  * **A:** Yeah, but they all require you (shudder) learn a new platform. Be it a "simple" markup language (lookin' at you,
Looker) or some sort of intricate UI designed more for dashboards than actually getting insights. You already know your
query language, let's leverage that strength!

## Help!

Helping with this project will make you one of the cooler people that I know. How can I (meaning you) do that?

* Easy:  Give this project a ⭐️!
* Easy:  Kick the tires.  [qwaver.io](https://qwaver.io) has the latest version running.
* Easy:  Edit this file and make a PR to add any feature requests.
* Easy:  If you're in the code and see where something could be improved, but can't make the improvement right then,
  add  `# TODO` comment with a helpful description of what needs to be done and submit a PR.

## The Data Model
* The hierarchy is like this:
  * Org -> Database -> Query -> Result
  * Each "->" represents a one-to-many relationship
* Users and Organizations
  * User and Organization have a many-to-many relationship with the connection defined by UserOrganization
    * Each organization can have many users
    * Each user can belong to many organizations
  * When using Qwaver, a user has a selected organization defined in their profile

### Feature requests
#### Big, important things:
* First time user flow:
    * create user
    * create / join organization (if invites apply)
    * create database if none in organization
* An invitation system allowing people to invite others to their organization and for people to review/accept/decline
  invitations
* JS charts on pages
* qwavers (esp. those with parameters) can be APIs as well
* Query collections -- user-defined lists of queries that all conform to a given topic

#### Small but cool things:
* set query type to: automatic, table, bar chart, line chart, pie or pivot
* test database connection when adding new database
* webpage preview when sharing results via slack or email
* flag queries -- if their results do no align with their title/description or are wrong in any other way
    * Search results should not include flagged queries
    * The author of a flagged query should be given an alert
* track average execution time for queries
* For pie charts with more than 20 pie slices; make single slice be sum of the remainder
* Add comments, likes
* create 404 page
* create exceptions table and log exceptions
* creat easy way to leave feedback

#### Issues:
* query parameters no longer recommending last specified

### General improvements
If you see any ways that the app could be improved in these ways, let's work on it!

* data security -- of paramount importance. In no way do we want a user to have access to data from an organization to
  which they do not belong
* performance -- This needs to be SNAPPY!
* HTML/CSS styling
* unit tests
* support for more databases

## Installation
qwaver is already up and running on [qwaver.io](https://qwaver.io)

If you want to run locally:

```
pip install -r requirements.txt
python3 manage.py collectstatic --no-input
python3 manage.py createsuperuser
python3 manage.py makemigrations
python3 manage.py migrate
```


Run python server, go to localhost

`python3 manage.py runserver`


Environment variables:
```
DJANGO_SETTINGS_MODULE=qwaver.settings
SECRET_KEY=[your secret key]
```


## Thank yous
* Much of the user management code has been based on the snippets made available
  by [Corey Schafer](https://github.com/CoreyMSchafer/code_snippets). He made
  an [excellent tutorial on learning Django](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)
  by walking through how to make a blog with many users. qwaver is basically a blog but for queries so it was a nice
  starting point!  

