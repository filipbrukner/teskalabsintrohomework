# Notes

**src/main.py** currently has a solution that isn't asynchronous or using the
recommended library

After 3-4 hours of looking through documentation I couldn't create a working
pipeline using **_examples/example-csv.py_** even if I directly copied video
tutorial

To change to solution using recommended library I need to:

- figure out how to read file (using examples either doesn't work or raises
  runtime Errors)
- figure out how to transform the actual data
- (maybe) figure out how to store data (if different from current version)

I might focus more on making current version asynchronous over making
recommended database work tomorrow

**resources/db.json** is a TinyDB database, it appends upon opening a file
so a refactorization to check if it already exists is necessary