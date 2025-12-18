# Automated QA interview

## General
The following folder contains an example app - UserSite.
It is a simple Django app that controls users and whether they like chocolate.
It uses SQLite as a DB for simplicity.

* Try to keep your code organized: functions, comments, etc.
* Feel free to use the internet for whatever you need.
* Feel free to ask questions, try not to get stuck on something for too long, just ask.

## Tasks
1. Open the codespaces, run the app (using `docker compose up -d`), and explore the endpoints through the browser (`<codespace URL>/userapp/users/`)
> Note the endpoints and their jsons while exploring.
2. Create a testing setup in your preferred method (Django unittest, PyTest, PlayWright) that reads the user list (`/users/`) to ensure your env is running.
> You can do this in a new terminal in the codespace.
3. Create a test that adds a new user, verifies it was created, deletes the user, and verifies it was deleted. 
4. Create a test to ensure all the likes_chocolate options are covered and other values aren't received.
5. Check for edge cases in the age_first_taste_chocolate (edge cases are your decision).
6. Bring up a GitHub action that runs the test.

## API Endpoints

1. **List All Users**
   
   - **Method:** `GET`
   - **Endpoint:** `/userapp/users`
   - **Description:** Returns a list of all users in the database.

2. **Add a New User**
   
   - **Method:** `POST`
   - **Endpoint:** `/userapp/users`
   - **Description:** Adds a new user to the database.

3. **Get a User**
   
   - **Method:** `GET`
   - **Endpoint:** `/userapp/users/<id>`
   - **Description:** Gets a user's info.

4. **Update a User**
   
   - **Method:** `PUT/PATCH`
   - **Endpoint:** `/userapp/users/<id>`
   - **Description:** Updates a user's info.
  
5. **Delete a User**
   
   - **Method:** `DELETE`
   - **Endpoint:** `/userapp/users/<id>`
   - **Description:** Removes a user from the database based on their ID.

Good luck! :-)
