import logging
import azure.functions as func
import requests
from azure.identity import DefaultAzureCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('FirewallRulePatcher triggered.')

    try:
        body = req.get_json()
        resource_group = body["ResourceGroup"]
        firewall_name = body["FirewallName"]
        rule_name = body["RuleName"]
        source_ip = body["SourceIP"]
        dest_port = body["DestinationPort"]
        action = body["Action"]
    except Exception as e:
        return func.HttpResponse(f"Bad request: {str(e)}", status_code=400)

    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default").token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Construct firewall rule API endpoint
    url = f"https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/{resource_group}/providers/Microsoft.Network/azureFirewalls/{firewall_name}/firewallPolicy/rules/{rule_name}?api-version=2023-02-01"

    rule_body = {
        "properties": {
            "ruleType": "NetworkRule",
            "ipProtocols": ["TCP"],
            "sourceAddresses": [source_ip],
            "destinationPorts": [dest_port],
            "action": {
                "type": action
            }
        }
    }

    response = requests.put(url, headers=headers, json=rule_body)

    if response.status_code in [200, 201]:
        return func.HttpResponse("Firewall rule applied successfully", status_code=200)
    else:
        return func.HttpResponse(f"Failed to apply rule: {response.text}", status_code=response.status_code)
