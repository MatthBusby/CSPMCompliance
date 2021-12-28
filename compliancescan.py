import requests
import json


apiKey = input("Please enter your API Key: ")
apiSecret = input("Please enter your API Secret: ")
email = input("Please enter email: ")\
print("aws, azure, gcp") 
provider = input("Please enter a cloud provider from the list above: ")
headers = {
    'Accept': 'application/json',
    }
if provider == "aws":
    Cloud = requests.get('https://api.dome9.com/v2/CloudAccounts', auth=(apiKey, apiSecret))
elif provider == "azure":
    Cloud = requests.get('https://api.dome9.com/v2/AzureCloudAccount', params={}, headers = headers, auth=(apiKey, apiSecret))
elif provider == "gcp":
    Cloud = requests.get('https://api.dome9.com/v2/GoogleCloudAccount', headers=headers, auth=(apiKey, apiSecret))

json_dataaccount = json.loads(Cloud.text)

for i in range(len(json_dataaccount)):
    print("name:   "+json_dataaccount[i]['name']+ "       id: "+json_dataaccount[i]['id'])

targetID = input("Please enter the desired Target: (please use the targetID)" )

print("Loading rulesets...")
ruleset = requests.get('https://api.dome9.com/v2/Compliance/Ruleset', params={}, headers = headers, auth=(apiKey, apiSecret))

json_datascan = json.loads(ruleset.text)


for i in range(len(json_datascan)):
    if json_datascan[i]['cloudVendor'] == provider:
        print("id:"+str(json_datascan[i]['id'])+ "    name:   "+json_datascan[i]['name'])
ruleId = input("Please enter the desired Ruleset: " )


data = '{"name":"Notificati11on policy","description":"Test Description","scheduledReport":{"emailSendingState":"Disabled","scheduleData":{"cronExpression":"0 0 16 1/1 * ? *","recipients":["test@test.com"]}},"changeDetection":{"emailSendingState":"Enabled","snsSendingState":"Disabled","externalTicketCreatingState":"Disabled","emailData":{"recipients":["'+email+'"]},"snsData":{"snsTopicArn":"","snsOutputFormat":"JsonWithFullEntity"},"ticketingSystemData":{"systemType":"ServiceNow","domain":"","user":"","pass":"","projectKey":"","issueType":""}},"gcpSecurityCommandCenterIntegration":{"state":"Disabled","projectId":"","bucketName":""}}'

ComplianceNotification= requests.post('https://api.dome9.com/v2/Compliance/ContinuousComplianceNotification', headers=headers, data=data, auth=(apiKey, apiSecret))

payload = {}
payload = json.loads(ComplianceNotification.text)
notificationID = payload["id"]

payload = '[  {    "targetId": "'+targetID+'",    "targetType": "'+provider+'",    "rulesetId": '+ruleId+',    "notificationIds": [      "'+notificationID+'"    ]  }]'

CompliancePolicy = requests.post('https://api.dome9.com/v2/ContinuousCompliancePolicyV2', params={

}, headers = headers, data=payload, auth=(apiKey, apiSecret))

print(CompliancePolicy.json())
print()
print(CompliancePolicy)

