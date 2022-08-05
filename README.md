<div style="text-align: center">
  <a href="https://qwiki.dev">
    <img src="https://qwiki.dev/media/qwiki-logo.png" alt="qwiki logo">
  </a>

**Turn queries into easy-to-use tools your teammates can share.**

Parameterize! Visualize! Collaboratize?!


<a href="https://github.com/brianrisk/qwiki/graphs/contributors">
<img src="https://img.shields.io/github/contributors/brianrisk/qwiki.svg">
</a>

qwiki links: [Intro](#the-fascinating-story) • [Help!](#help) • [Installation](#installation) • [Thanks](#thank-yous)
</div>

## The Fascinating Story

[![Join the chat at https://gitter.im/qwiki-dev/community](https://badges.gitter.im/qwiki-dev/community.svg)](https://gitter.im/qwiki-dev/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

If you're like me, you have hundreds of queries stored in your DB admin tool for several connected DBs. A lot your time
is spent searching through them, altering WHERE clauses, exporting the results, plotting charts, and emailing the
results (chart + data + query for validation). Often you've got others on your team doing the exact same thing
re-inventing the wheel left and right.

This lead to the development of qwiki (think: "query wiki").

Hey, do you have time for business question involving our database?

Sure!  Give me 20 minutes..

17 minutes later...

Here you go!  See attached chart and data!

Thanks!  could you do like 100 more with different time periods and countries?

Your skills as a query artist were definitely needed that first time, but the second time the need comes from that
person you're helping not having any experience with queries at all.

**Q:** Don't other tools out there help with this?
**A:** Yeah, but they all require you (shudder) learn a new platform. Be it a "simple" markup language (lookin' at you,
Looker)
or some sort of intricate UI designed more for dashboards than actually getting insights. I mean: you already know your
query language, can't we just stick with that??

## Help!

Helping with this project will make you one of the cooler people that I know. How can I (meaning you) do that?

* Easy:  Give this project a ⭐️!
* Easy:  Kick the tires.  [qwiki.dev](https://qwiki.dev) has the latest version running.
* Easy:  Edit this file and make a PR to add any feature requests.
* Easy:  If you're in the code and see where something could be improved, but can't make the improvement right then,
  add  `# TODO` comment with a helpful description of what needs to be done and submit a PR.

### Feature requests
#### Big, important things:
* First time user flow:
    * create user
    * create / join organization (if invites apply)
    * create database if none in organization
* An invitation system allowing people to invite others to their organization and for people to review/accept/decline
  invitations
* JS charts on pages
* qwikis (esp. those with parameters) can be APIs as well
* Query collections -- user-defined lists of queries that all conform to a given topic

#### Small but cool things:
* set query type to: automatic, table, bar chart, line chart, pie or pivot
* test database connection when adding new database
* webpage preview when sharing results via slack or email
* flag queries -- if their results do no align with their title/description or are wrong in any other way
    * Search results should not include flagged queries
    * The author of a flagged query should be given an alert
* card layout for home page
    * https://getbootstrap.com/docs/4.0/components/card/
    * use .card-columns in parent div
    * use .stretched-link:
    * https://stackoverflow.com/questions/54404865/make-bootstrap-card-entirely-clickable
* track average execution time for queries

### General improvements
If you see any ways that the app could be improved in these ways, let's work on it!

* data security -- of paramount importance. In no way do we want a user to have access to data from an organization to
  which they do not belong
* performance -- This needs to be SNAPPY!
* HTML/CSS styling
* unit tests
* support for more databases

## Installation
qwiki is already up and running on [qwiki.dev](https://qwiki.dev)

If you want to run locally:

* manage.py
    * createsuperuser
    * makemigrations
    * migrate

Run python server, go to localhost

## Thank yous
* Much of the user management code has been based on the snippets made available
  by [Corey Schafer](https://github.com/CoreyMSchafer/code_snippets). He made
  an [excellent tutorial on learning Django](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)
  by walking through how to make a blog with many users. qwiki is basically a blog but for queries so it was a nice
  starting point!  

