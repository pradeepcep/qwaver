# Qwaver Feature Requests
Add something below!

## Documentation
- Need to document instant pivot charts feature

## Issues
- buttons on clone page
- have form checks for load csv table name

## TODO
- configure email server, re-enable email verification code in register.py and middleware.py
- do not allow query creation (AI or otherwise) or show those menu items if a database has not been set up

## General improvements

If you see any ways that the app could be improved in these ways, let's work on it!

- data security - of paramount importance. We don't users to have access to data from an organization to which they do not belong
- HTML/CSS styling
- unit tests
- support for more databases

## Efficiency

- In `query_version.py`, make spans cover contiguous changed characters, not individual characters

## UI
- Remove parameters that are commented out from UI
- Center column names in output
- Name previous query versions
- Name previous result versions

## UX
- Cleaner error handling
- Feedback to show a query is running (Loading bar or circle animation, etc.)
- Add notification when query is done running (like DataGrip)
- Badges for accomplishments -- eg. "creator", "pivoter", "chart master"

## Analytics
- User Stats
    - Results viewed per day
    - Results viewed per hour
    - Queries created per day
    - Cruise made per hour
    - Total queries made
    - Total results viewed

## Coding Queries
- Exequeue for single-param queries: Create a queue of parameter names and execute the query with those parameters in sequence while storing the results in the version control section
- "Starters": pre-defined sets of queries and collections if a database is for a common CMS
- Query collections -- user-defined lists of queries that all conform to a given topic
- JS charts on pages
- Support `ctrl+x/command+x` as a shortcut to create comments
- Linked collections– queries that take exactly one parameter: the id of a related object.
- Result differences
    - Subtract result tables from each other. 
        - The above works when the table has the same number of rows, when they have two columns, and when the second column is numeric
    * "order by column" that takes a string for a column name or, if integer, col index
- Chaining: combine search results from one database into the query of another.
    - Example: one day the base returns IDs and the other query on a different database uses those IDs

## DB Connection
- Hide database credential password with bullet characters
- Permissions
    - Ability to add different DB users to a given database: one that can alter on that can not
    - User permissions: org edit; DB edit; query edit, query create
    - User database permissions assigns to them the appropriate db user
    - only org admins can
        - see DB menu
        - edit or add DB
        - make invitations
    - only query creators and org admins can
        - see the edit buttons
        - delete
- DB Explorer
    - list tables, list columns, list running queries, kill query
- Read-only mode to disable CRUD functionality
- Manage DB connection (instead of removing current one or setting up a new one)
- De-deuplicate DB Connections: Don't allow for two DB connections (for each user) with the same name
    - Currently, you're able to hit the submit button as many times as you want and create multiple of the same connection, but that shouldn't be possible

## Small Things
- returned row count added to result model; show this in results sidebar on query page
- https (helping set that on the DigitalOcean server)
- after the user signs up, the next screen is they accept a Terms of Service (apache 2.0)
- For the database configuration, have both users be optional, but if there is not a loser who can alter tables, then certain functionality like load CSV will be off
- drop-down menu to select organization if there is more than one org for the user
- pretty API urls: qwaver.io/api/org-slug/query-name-slug (unique field, similar to in Referral)
- disable queries; don't delete them
- scatter plot charting
- ability to make queries public (where the world can use them)
- update success and error counts in results
- save exact query run with result; view that shows this
- track average execution time for queries
- have parent reference in queries.Query model (if the query was cloned from another)
- set query type to: automatic, table, bar chart, line chart, pie or pivot
- webpage preview when sharing results via slack or email (e.g. add open graph social previews to results. This will
  necessitate making an image url)
- flag queries -- if a user determines their results do not align with their title/description or are wrong in any other way
    - Search results should not include flagged queries
    - The author of a flagged query should be given an alert
- Add comments, likes, stars
- create 404 page
- create easy way to leave feedback
- parameters:
    - country or date selector when param is {country} or {date}
    - For parameters set maximum and minimum and numeric values
- list users in an organization
- automatically add a limit to every query
- Have a result search where are the searches are the input fields for a given query. 
  No search option if there are no input fields.
- as a person changes parameters, the API url updates
- limit CSV upload to MB and give warning if more than 1000 lines
- reset API key
- settings and properties:
  - is_public:  all queries and results are accessible by non-members
  - query result update frequency -- saved results are returned if a query is performed within the time limit.
    e.g. a query is performed with the parameter value "cat".  Then, 10 seconds later, someone else also
    searches with "cat".  If the update frequency is 1 minute, then the results of the first query are returned.
