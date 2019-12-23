import json
import boto3
import os
from boto3.dynamodb.conditions import Key
from botocore.vendored import requests

def lambda_handler(event, context):
    # TODO implement
    bucket = 'cloud-project-fridge'
    key = 'veggies.jpg'
    print(event)

    #ADDING COGNITO CODE HERE
    new_client = boto3.client('cognito-idp')
    answer = new_client.admin_get_user(UserPoolId='us-east-1_nJdQZS1Kp', Username = 'vineet_v')
    print("answer = ", answer)

    latitiude = str(event['lat'])
    longitude = str(event['lon'])
    time = str(event['time'])
    choice = event['r_choice']


    find_image = boto3.client('rekognition', 'us-east-1')
    response = find_image.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':key}})
    mod_response = response['Labels']
    #print("mod_response is: ", mod_response)
    #print(" \n\n response is:", response)
    available = []
    for each in mod_response:
        #print(each["Name"])
        available.append(each["Name"])

    cut_list = ['Vegetable', 'Hot Dog' , 'Plant', 'Food', 'Fruit', 'Produce', 'Meal', 'Lunch', 'Sweets', 'Confectionery', 'Snack', 'Dish', 'Platter', 'Cafeteria', 'Restaurant', 'Buffet']
    for each in available:
        if each in cut_list:
            available.remove(each)
        else:
            continue

    for each in available:
        if each in cut_list:
            available.remove(each)

    for each in available:
        if each in cut_list:
            available.remove(each)

    seperator = ','
    new_str = seperator.join(available)
    new_str1 = seperator.join(latitiude)
    new_str2 = seperator.join(longitude)
    new_str3 = choice

    # Database part begins ----------------------------------------------------------------

    ingredientsList = new_str
    print("Ingredients List is : ",ingredientsList)
    userTypeChoice = new_str3
    print("User Type Choice is : ",userTypeChoice)
    dynamodb = boto3.resource('dynamodb')
    receipeTable = dynamodb.Table('receipe')
    receipeResponse = receipeTable.query(KeyConditionExpression=Key('ingredients').eq(ingredientsList), FilterExpression=Key('typequery').eq(userTypeChoice))
    if len(receipeResponse['Items']) > 0:
        dishSuggestion = receipeResponse['Items'][0]['dish']
        cookReceipe = receipeResponse['Items'][0]['receipe']
        unavailableList = receipeResponse['Items'][0]['tobuy']

    else:
        dishSuggestion = 'No Suggestion!'
        cookReceipe = 'Nothing to cook!'
        unavailableList = 'Dont know if you have to buy anything!'



    # Database part ends -----------------------------------------------------------------------

    messageAttributes={
        'availableItems': {
            'DataType':'String',
             'StringValue' : ingredientsList
        },
        'itemsToBuy': {
            'DataType':'String',
            'StringValue': unavailableList

        },

        'latitiude': {
            'DataType': 'String',
            'StringValue': latitiude
        },
        'longitude': {
            'DataType': 'String',
            'StringValue': longitude
        },
        'choice': {
            'DataType': 'String',
            'StringValue': userTypeChoice
        },
        'itemToCook':{
            'DataType': 'String',
            'StringValue' : dishSuggestion
        },
        'receipe':{
            'DataType': 'String',
            'StringValue' : cookReceipe
        }
    }

    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/382782476131/cloud-project-queue'
    delaySeconds = 15
    messageBody = "test message "

    response = sqs.send_message(QueueUrl = queue_url,
                                DelaySeconds = delaySeconds,
                                MessageAttributes = messageAttributes,
                                MessageBody = messageBody)
    print("available: ", available)
    print("response: ", response)


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
