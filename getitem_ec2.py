#!/usr/bin/python3

# for Zabbix Low Level Discovery
# discover ec2 instances.

import boto3
import sys
import json

args = sys.argv

if len(args) != 3 :
  print("getitem_ec2.py [instance ID] [item name]")
  sys.exit()

region = ''
key = ''
secret = ''

ec2 = boto3.client(
  'ec2',
  region_name=region,
  aws_access_key_id=key,
  aws_secret_access_key=secret
)
response = ec2.describe_instances(
  InstanceIds=[
    args[1]
  ]
)["Reservations"][0]["Instances"][0]

#出力形式
#値そのまま

if args[2] == "PrivateIpAddress":
  #private IP address
  result = response["PrivateIpAddress"]
elif args[2] == "State":
  #state
  result = response["State"]["Name"]

elif args[2] == "PrivateDnsName":
  #private DNS name
  result = response["PrivateDnsName"]

elif args[2] == "Name":
  result = "no name"
  #tag
  #タグは辞書型の要素を持つ配列
  tags = response["Tags"]
  for tag in tags:
    # 要素: Key, Valueの２つ
    if tag['Key'] == 'Name':
      #Nameはホスト名として扱う
      result = tag['Value']
  #  else:
      #それ以外のタグはそのまま
  #    item.append({"{#TAG}" : {tag['Key']: tag['Value']}})

elif args[2] == "InstanceId":
  #instance id
  result = response["InstanceId"]
else:
  result = "no data"

print(result)