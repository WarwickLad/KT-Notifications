import json
import os
import urllib
import boto3
from boto3.dynamodb.conditions import Key
import decimal
from random import seed
from random import randint

print('Loading message function...')


def send_to_sns(message, context):

    # The lambda is structured into 4 sections: 
    # 1) configure DynamoDB query, based on random quote search
    # 2) configure S3 with random image URL extraction
    # 3) configure SMS payload using DB quote and image URL
    # 4) send message payload to SNS topic
    
    # DynamoDB table setup
    dynamodbClient = boto3.resource('dynamodb')
    dynamodbTable = dynamodbClient.Table('<ENTER TABLE NAME HERE>')
    randomItem = randint(1, <ENTER MAX RANGE OF TABLE>)
    dynamodbResponse = dynamodbTable.query(
        KeyConditionExpression = Key('ID').eq(randomItem)    
    )
    for i in dynamodbResponse['Items']:
        dynamodbResponseItem = i['Quote']
    
    # S3 setup and random image path selection
    basePath = '<ENTER PATH TO S3 BUCKET>'
    randomFolder = randint(1, <ENTER NUMBER OF SUB FOLDERS>)
    if randomFolder == 1:
        S3Folder = '<ENTER SUB FOLDER/FILE BASE>'
    elif randomFolder == 2:
        S3Folder = '<ENTER SUB FOLDER/FILE BASE>'
    else:
        S3Folder = '<ENTER SUB FOLDER/FILE BASE>'
    pathItems = (basePath, S3Folder, str(randomItem),'.jpg')
    fullPath = "".join(pathItems)
    
    # Configure SMS message payload
    messageElements = (dynamodbResponseItem ,' - ', str(fullPath))
    fullMessage = "".join(messageElements)

    # Configure SNS message
    
    sns = boto3.client('sns')
    sns.publish(
        TopicArn = '<ENTER SNS TOPIC ARN>',
        Subject = 'Encouraging message!',
        Message = fullMessage
    )

    return ('Sent a message to an Amazon SNS topic.')