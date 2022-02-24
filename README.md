# todos

[![Build Status](https://app.travis-ci.com/KabakiAntony/todos.svg?branch=develop)](https://app.travis-ci.com/KabakiAntony/todos) [![Coverage Status](https://coveralls.io/repos/github/KabakiAntony/todos/badge.svg?branch=develop)](https://coveralls.io/github/KabakiAntony/todos?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/765e3273d918653417df/maintainability)](https://codeclimate.com/github/KabakiAntony/todos/maintainability)


[API DOCUMENTATION](https://katodos.docs.apiary.io/#)

## what is todos
todos is a basic app for capturing things that I need to be done for a given day or given time duration , it's aim albeit being a simplistic app is to showcase the understanding of REST API design principles,it will include Travis Ci which is going to help in the build process for continous integration and deployment. The project is going to be hosted on Heroku for the Rest API and the frontend will hosted on github pages.


## Setup and installation

1. Set up virtualenv

   ```bash
        virtualenv venv
   ```

2. Activate virtualenv on linux and windows  as below

   ```bash
      LINUX/MAC

       source venv/bin/activate or 
       . venv/bin/activate

      WINDOWS

      . venv\Scripts\activate
      
   ```

3. Install dependencies

   ```bash
        pip install -r requirements.txt
   ```

4. Database initialization and configuration.

The project uses PostgreSQL to persist data and if you wish to use the same you can [get it here](https://www.postgresql.org/download/) ,it supports different Operating Systems just follow the prompts for the different cases under each selection. To make your life easier you may also want to install pgAdmin it is an Open Source postgres administration platform, rather you will use it to create and manage database instances for Postgres, I highly suggested you install that also and if sold on it you can [get pgAdmin here](https://www.pgadmin.org/download/)

Once you have successfully installed both then, Create both **todos** and **todos_test_db** - the usage is straight forward I believe. After creating databases then run the below command, it will apply the migrations to the database.

   ```bash
      flask db upgrade

   ```

5. Running tests 

You can run tests to assertain that the setup works

   ```bash
      python -m pytest --cov=app/api

   ```

6. Start the server

   ```bash
      flask run or python wsgi.py 
   ```

<details>
<summary>todos endpoints</summary>

METHOD       | ENDPOINT      |  DESCRIPTION
------------ | ------------- | ------------
POST  |  /users/signup  | signup a user
POST  |  /users/verify  | verify a user email
POST  |  /users/signin  | signin a user
POST  |  /users/forgot  | send reset password link
PUT   |  /users/update-password |change/update a user password
POST  |  /todos         | create a new todo
GET   |  /todos         | get all todos for a user
PUT   |  /todos/{id}    | edit / update a todo given its id
GET   |  /todos/{id}    | get a specific todo given it's id
DELETE|  /todos/{id}    | delete a todo given it's id


</details>

<details open>

Incase of a bug or anything else use any on the below channels to reach me

[Find me on twitter](https://twitter.com/kabakikiarie) OR  drop me an email at kabaki.antony@gmail.com.
