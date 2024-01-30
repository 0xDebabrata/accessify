## Local Setup

You must have python3 installed on your local system to contribute to the project.

To start the server, clone the repository and get into the server directory using change directory (`cd`) command in linux.

```
cd server
```

Now create a python virtual environment, install the required packages and execute the `main.py` file by executing the following commands.

```sh
python3 -m venv accessify
source ./accessify/bin/activate
pip install -r requirements.txt
python main.py
```

<!-- ```sh
cd server
uvicorn main:app --reload --port 8080
``` -->

You can also run the project using Docker by executing the following command inside `server` directory directly.

```sh
docker-compose up
```
