

def uploadData(event, context):
	client = boto3.resource('dynamodb')
	table = client.table("Jerry_Rice_Stats")
