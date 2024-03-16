import requests, subprocess, time, os

MODEL_ID = os.environ["MODEL_ID"]
INITIALIZE = False

def lambda_handler(event, context):

    inputs = event["inputs"]

    url = "http://127.0.0.1:3000/embed"

    # Define o cabeçalho para indicar que estamos enviando JSON
    headers = {"Content-Type": "application/json"}

    global INITIALIZE
    if not INITIALIZE:
         command = ["text-embeddings-router", "--json-output", "--model-id", MODEL_ID]
         process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
         for line in iter(process.stdout.readline, ''):
            print(line, end='')  # 'end' is set to '' to avoid adding additional newlines
            if '"INFO","message":"Ready","target":"text_embeddings_router"' in line:
                INITIALIZE = True
                time.sleep(0.5)
                break  # Exit t

    payload = {"inputs": inputs}
    response = requests.post(url, json=payload, headers=headers, timeout=300)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
    return response.json()

