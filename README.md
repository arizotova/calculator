# Python Calculator + HTTP API
## Usage
1. Install the dependencies 
    ```shell
    pip install -r requirements.txt
    ```
2. Run the server
    ```shell
    python app.py
    ```
3. Send a request with expression to be evaluated
    ```shell
   curl -X POST -H "Content-Type: application/json" -d '{"expression": "-4 * ((17 - -5 * 1 + 3) / 2.5) / 4"}' http://localhost:5000/evaluate
   ```