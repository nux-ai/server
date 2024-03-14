
## Setup
We use poetry for dependency management. Make sure to install it first before proceeding.
Poetry Installation: https://python-poetry.org/docs/

Follow these steps to set up the project:

1. **Create a virtual environment**
   ```
   poetry env use python3.10
   ```

2. **Activate the virtual environment**
   ```
   poetry shell
   ```

3. **Install the requirements**
   ```
   poetry install
   ```

4. **Run the local server**
   ```
   poetry run uvicorn main:app --reload --port 8081
   ```
    or
    ```
    poetry run python3 -m uvicorn main:app --reload
    ```

## Docker Commands:

docker build --platform linux/amd64 -t nux-ai/parse:latest .

docker run -p 8001:8001 nux-ai/parse:latest