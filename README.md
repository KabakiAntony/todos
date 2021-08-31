# todos


## what is todos
todos is a basic app for capturing things that I need to do during a given, day or given time duration , it's aim albeit being a simplistic app is to showcase the understanding of REST API design principles, also include pivotal tracker to help in project management, it will also include Travis Ci which is going to help in the build process for continous integration and deployment. The project is going to be hosted on Heroku for the Rest API and the frontend will hosted on github pages.


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

       venv\Scripts\activate
      
   ```

3. Install dependencies

   ```bash
        pip install -r requirements.txt
   ```


4. Running tests

   ```
      python -m pytest --cov=app/api 

        or you can use
      
      python -m nose2 -v 

      The difference is that nose2 will not run coverage you will have to invoke coverage on your own

   ```

5. Start the server

   ```
      flask run or python wsgi.py 
   ```
 NOTE "flask run" defaults to production where the debug mode is off 
        and that denies one the chance of seeing the errors that arise
        but the below settings will help override that.
   ```
      use **set** on windows and **export** on linux/mac
      set FLASK_APP=wsgi.py
      set FLASK_DEBUG=1
      set FLASK_ENV=development
       
   ``` 

<details>
<summary>todos endpoints</summary>

    Keep and eye here for the various endpoints you can use with this  backend.

</details>

<details open>

Incase of a bug or anything else use any on the below channels to reach me

[Find me on twitter](https://twitter.com/kabakikiarie) OR  drop me an email at kabaki.antony@gmail.com.
