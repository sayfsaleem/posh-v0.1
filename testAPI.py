import http.client
import json

# Replace these values with your actual server and endpoint details
server_host = "127.0.0.1"
server_port = 8000
api_endpoint = "/api/customer-scan/"

# Replace this with the actual barcode you want to test
barcode_to_test = "1"
token = "a2bc8c643c97ff209b5d4fed0d2ea2db49e7ff3a"  # Replace with your actual authentication token

# Replace this with the actual barcode you want to test

# Request payload
data = json.dumps({"barcode": barcode_to_test})
headers = {"Content-Type": "application/json", "Authorization": f"Token {token}"}

# Establish a connection to the server
conn = http.client.HTTPConnection(server_host, server_port)

# Send a POST request
conn.request("POST", api_endpoint, body=data, headers=headers)

# Get the response
response = conn.getresponse()

# Read and print the response
response_data = response.read().decode("utf-8")
print(response_data)

# Close the connection
conn.close()
