command to run :

    ```bash
    cd app
    python -m venv env (create python virtual environment)
    pip install -r requirements.txt (pip3 if using Mac/Linux)
    uvicorn main:app --reload {if not, uvicorn main:app --reload --host 127.0.0.1 --port 8000}
    ```
