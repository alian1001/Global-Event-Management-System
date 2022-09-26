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

# How to build the application

## Make sure you have python installed.

```
python3
```

## Create a virtual environment with this command

```
python3 -m venv venv
```

## Create a virtual environment with this command (Windows)

```
py -m venv venv
```

## Once your in the web directory run this command (Mac or Linux)

```
source venv/bin/activate
```

### Once your in the web directory run this command (Windows)

```
venv\Scripts\activate
```

## Once in the virtual environment run this command

```
pip install -r requirements.txt
```

## Configure the Stripe API key

### MacOS/Linux (Untested)

```
export STRIPE_SECRET="<Stripe Secret Key>"
```

### Windows (Powershell)

```
$env:STRIPE_SECRET="<Stripe Secret Key>"
```

## Finally, run the application with this command

```
flask run
```

The application will now be running at http://localhost:5000/
