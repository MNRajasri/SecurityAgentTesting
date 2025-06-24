import requests
import json
import hashlib
import hmac
import base64
import datetime

# Replace with your details
workspace_id = "79053fef-9a76-4921-991b-fbc3e5a4c99c"  # Log Analytics Workspace ID
shared_key = "tzpUQ2TQP/m8eA3PM5Fbw0t9dXg+Lyn7Y/9qA3cSIy7R+Dp5gFrBMwnEGH46T5w0aPt1GrEFT469AV7LPvlM3A=="  # Get from Workspace > Agents > Primary Key
log_type = "NetworkflowCustomLog"  # Custom table name (without _CL)

# Sample data payload matching your DCR schema
data = [
    {
        "timestamp": "2025-06-17T14:30:00Z",
        "sourceIP": "192.168.1.10",
        "destinationIP": "10.0.0.1",
        "sourcePort": 443,
        "destinationPort": "80",
        "protocol": "TCP",
        "bytes": 1000,
        "packets": 15,
        "sourcePortUsage": "HTTPS",
        "destinationPortUsage": "HTTP",
        "history": "Allowed",
        "nsg_name": "TestNSG",
        "rule_name": "Allow_HTTP",
        "priority": 100,
        "direction": "Inbound",
        "access": "Allow"
    }
]

# Convert to JSON
body = json.dumps(data)
body_bytes_length = len(body)

# Get current RFC1123 date
rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

# Build signature
string_to_hash = f"POST\n{body_bytes_length}\napplication/json\nx-ms-date:{rfc1123date}\n/api/logs"
bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
decoded_key = base64.b64decode(shared_key)
encoded_hash = base64.b64encode(
    hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()
).decode()

signature = f"SharedKey {workspace_id}:{encoded_hash}"

# Build request headers
uri = f"https://{workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01"
headers = {
    "Content-Type": "application/json",
    "Authorization": signature,
    "Log-Type": log_type,
    "x-ms-date": rfc1123date,
    "TimeGenerated": "timestamp"  # Maps your 'timestamp' to TimeGenerated
}

# Make request
response = requests.post(uri, data=body, headers=headers)

# Output
print("Response Code:", response.status_code)
if response.status_code != 200:
    print("Response Content:", response.text)
else:
    print("✅ Data successfully sent.")
