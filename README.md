## MyJournal Project

### Getting Started

To get started with this project, follow these steps:

1. **Clone the repository:**
git clone https://github.com/x3m4llk0/MyJournal.git


2. **Install the required dependencies:**
You can use pip to install the dependencies mentioned in the requirements.txt file:
pip install -r requirements.txt


3. **Set up your environment:**
Make sure that you have all the necessary services installed and configured correctly (for example, PostgreSQL, Redis).

4. **Fill out the .env and .env-cont files:**
If you need to create your own Secret Key:

Code to generate a random secret key on Windows:
```python
from secrets import token_bytes
from base64 import b64encode
print(b64encode(token_bytes(32)).decode())
```
If you have Linux/MacOS, you can open a terminal and run this command:
```shell
openssl rand -base64 32
```
5. Run the tests:
You can execute the test scripts using pytest:
```shell
pytest
```
or
```shell
pytest -v -s -W ignore::DeprecationWarning
```
6. To run the application in Docker, use the following commands:
```shell
docker-compose build
docker-compose up
```
After Docker is started, the application endpoints are available at:
http://127.0.0.1:8000/docs/

Feel free to modify and enhance the application based on your requirements!