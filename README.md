### Koffie Labs Backend Coding Challenge

#### Objective

Implement a simple [FastAPI](https://fastapi.tiangolo.com) backend to decode VINs, powered by the [vPIC API](https://vpic.nhtsa.dot.gov/api/) and backed by a [SQLite](https://www.sqlite.org/index.html) cache.

#### Time Expectation

We expect this challenge to take you 3-5 hours to complete - one or two evenings.

#### Requirements

Your application should contain three (3) routes:

`/lookup`

This route will first check the SQLite database to see if a cached result is available. If so, it should be returned
from the database.

If not, your API should contact the vPIC API to decode the VIN, store the results in the database, and return the
result.

The request should contain a single string called "vin". It should contain exactly 17 alphanumeric characters.

The response object should contain the following elements:

- Input VIN Requested (string, exactly 17 alphanumeric characters)
- Make (String)
- Model (String)
- Model Year (String)
- Body Class (String)
- Cached Result? (Boolean)

`/remove`

This route will remove a entry from the cache.

The request should contain a single string called "vin". It should contain exactly 17 alphanumeric characters.

The response object should contain the following elements:

- Input VIN Requested (string, exactly 17 alphanumeric characters)
- Cache Delete Success? (boolean)

`/export`

This route will export the SQLite database cache and return a binary file (parquet format) containing the data in the
cache.

No additional input/data should be required to make the request.

The response object should be a binary file downloaded by the client containing all currently 
cached VINs in a table stored in parquet format.

#### Build Setup and Deploy

Use FastAPI as your web framework. You may structure your project as you wish.

You do not need to deploy your code, but you should be prepared to have a conversation about how to do so.

When you're ready to submit your work to us, create a git repo, push your results, and send us the link.

#### Our Evaluation

- Basic functionality
- Code quality
- Error handling
- Documentation (readme/comments/tests)
- Ability to explain your implementation decisions

Please feel free to be creative and add any embellishments or additional functionality you would like to show off!

#### Test VINs

You may use the following test VINs. We encourage you to try VINs you may find from other sources!

`1XPWD40X1ED215307`
`1XKWDB0X57J211825`
`1XP5DB9X7YN526158`
`4V4NC9EJXEN171694`
`1XP5DB9X7XD487964`
