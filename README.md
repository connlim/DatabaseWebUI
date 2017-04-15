# DatabaseWebUI
Flask app to display and search a database on a webpage

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python 3, pip, and virtualenv

Install Python 3 and pip through your system.

To install virtualenv

```
pip install virtualenv
```

### Installing

#### Windows
Run all the commands below in a Command Prompt

Create a new virtual environment
```
> virtualenv venv
```

Activate the virtual environment
```
> venv\Scripts\activate
```

Install required packages
```
> pip install -r requirements.txt
```

Set the flask app environment variable
```
> set FLASK_APP=flaskapp
```

Run the app
```
> flask run
```
Visit `localhost:5000` to view the app

