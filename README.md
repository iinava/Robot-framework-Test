
# Robot Framework Project

## Description
This project is a test automation framework using Robot Framework for testing  , users can send test commands as json request.

## Installation
1. Clone the repository to your local machine:
   ```
   git clone https://github.com/iinava/Robot-framework-Test.git
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Ensure that you have Python installed and the required packages installed.
2. Run the Django server:
   ```
   python manage.py runserver
   ```
3. Send a POST request to the specified endpoint with a JSON payload containing the tests you want to execute.
4. View the results returned by the server.


#POST  API END POINT


http://127.0.0.1:8000/testai/tests/v1/execute



# JSON BODY FORMAT


{
    "tests": [
        {
            "title": "Open google.com",
            "steps": [
                "Open Browser   browser=chrome",
                "Go To    https://www.google.com "
            ]
        }
    ]
}




Feel free to contact incase any issue occurs with running the project
