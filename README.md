# CITS3200 Project Group 9

Event Management System

Creation of a secure web-based shop front for event attendees:
to book his/her attendance (including partner, children);
to register contact details;
to indicate no fees involved;
to enable uploading images/text; and
to interface with printer to generate badges
Security of data is an important consideration.

IP Exploitation Model

The IP exploitation model requested by the Client is: Creative Commons (open source) http://creativecommons.org.au/

CC BY SA 4.0
https://creativecommons.org/licenses/by-sa/4.0/

---

# How to run on Heroku

1. Create a heroku project. 

2. Clone the GEMS git repo

3. With heroku CLI, replace `<project>` with the name of your project then run,
```
heroku git:remote -a <project>
```

4. Now push the code to heroku; 
```
git push heroku main
```

5. Now setup stripe (Refer to documentation below)


---

# How to run locally

1. Make sure you have python installed.

    ```
    python3
    ```

2. Create a virtual environment

    MacOS/Linux

    ```
    python3 -m venv venv
    ```

    Windows

    ```
    py -m venv venv
    ```

3. Activate the venv
    MacOS/Linux

    ```
    source venv/bin/activate
    ```

    Windows

    ```
    venv\Scripts\activate
    ```

4. Install the requirements

    ```
    pip install -r requirements.txt
    ```
5. (Optionally) you can run our unit tests
    MacOS/Linux
    
    ```
    python3 unit_tests.py
    ```

    Windows

    ```
    py unit_tests.py
    ```

6. Run the application
    * Production server

        ```
        gunicorn app:app
        ```

        The application will now be running at http://localhost:8000/


    * Development

        ```
        flask run
        ```

        The application will now be running at http://localhost:5000/

7. Now setup stripe (Refer to documentation below)


---

# Stripe Setup
To use stripe, you will need to set some environment variables.

### stripe.env (MacOS/Linux/Windows)
Create a file called `stripe.env` in the base directory. 
```
STRIPE_SECRET="<Your Stripe Secret>"
STRIPE_WEBHOOK_SECRET="<Your Webhook Secret>"
```

### MacOS/Linux

```
export STRIPE_SECRET="<Your Stripe Secret>"
export STRIPE_WEBHOOK_SECRET="<Your Webhook Secret>"
```

### Windows (Powershell)
```
$env:STRIPE_SECRET="<Your Stripe Secret>"
$env:STRIPE_WEBHOOK_SECRET="<Your Webhook Secret>"
```

### Heroku
```
heroku config:set STRIPE_SECRET="<Your Stripe Secret>"
heroku config:set STRIPE_WEBHOOK_SECRET="<Your Webhook Secret>"
```

Your stripe secret will be located in the developer section of the stripe dashboard, under API keys. 


To get the webhook secret, you need to create a new webhook in the stripe dashboard. The URL should either be the url to your webpage, if you are using a heroku free plan it could be something like: `https://yourAppNameHere.herokuapp.com/home`. 
The webhook listens for the `checkout.session.completed` and `checkout.session.expired` events. 
Once the webhook has been created you can find the signing secret. 