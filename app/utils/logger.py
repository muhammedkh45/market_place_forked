# Basic APILog functionality
def log_request(endpoint: str, data: dict):
    print(f"Logging request to {endpoint}: {data}")

def log_response(status: int, response_data: dict):
    print(f"Logging response with status {status}: {response_data}")
