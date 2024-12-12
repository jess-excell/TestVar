# TestVar
TestVar is a web-based flashcard app developed for CCCU Programming Frameworks and Languages Assessment 1.

## Features
- Create, read, update and delete flashcards, flashcard sets and flashcard collections
- Leave comments and reviews on public sets to ask questions, suggest improvements, etc.

## Requirements
- Python 3.12+
- Django 4.2+
- DjangoRestFramework 3.15+

## Getting started
### Installation
1. Clone plf-a1
2. Install the dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run all database migrations
   ```bash
   py manage.py makemigrations
   py manage.py migrate
   ```
4. Set up a superuser
   ```bash
   py manage.py createsuperuser
   ```

### Usage
#### Run the server
```bash
py manage.py runserver
```
The api urls are all prefaced with api/, e.g. /api/users/ and /api/comments/.

To run the server on a specific port (e.g. 3000), run
```bash
py manage.py runserver 3000
```
#### Testing
To run all tests:
```bash
py manage.py test
```
Note: it is possible to run the tests in parallel using ```py manage.py test --parallel auto```, but this has had issues in the past so it is not recommended.

To run individual tests 
```bash
py manage.py test (app name).tests.(test file name)
```

For example, to run test_endpoint_sets in the api tests:
```bash
py manage.py test api.tests.test_endpoint_sets
```
