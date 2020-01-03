#!/usr/bin/python3

# for Zabbix Low Level Discovery
# discover ec2 instances.

import boto3
import sys
import json

args = sys.argv

region = ''
key = ''
secret = ''

ec2 = boto3.client(
  'ec2',
  region_name=region,
  aws_access_key_id=key,
  aws_secret_access_key=secret
)
response = ec2.describe_instances()["Reservations"]

#出力形式(本来は改行を入れてはいけない)
#{
#  "data": [
#    { "{#KEY_NAME1}": "VALUE" },
#    { "{#KEY_NAME2}": "0" }
#  ]
#}
item = []

for instance in response:
  #instance id
  temp = instance["Instances"][0]["InstanceId"]
  if temp != args[1]:
    continue

  item.append({"{#INSTANCE_ID}" : instance["Instances"][0]["InstanceId"] })
  
  #state
  item.append({"{#STATE}" : instance["Instances"][0]["State"]["Name"]})

  #private IP address
  item.append({"{#PRIVATE_IP}" : instance["Instances"][0]["PrivateIpAddress"]})

  #private DNS name
  item.append({"{#PRIVATE_DNSNAME}" : instance["Instances"][0]["PrivateDnsName"]})

  #tag
  #タグは辞書型の要素を持つ配列
  tags = instance["Instances"][0]["Tags"]
  for tag in tags:
    # 要素: Key, Valueの２つ
    if tag['Key'] == 'Name':
      #Nameはホスト名として扱う
      item.append({"{#HOSTNAME}" : tag['Value']})
    else:
      #それ以外のタグはそのまま
      item.append({"{#TAG}" : {tag['Key']: tag['Value']}})

discovery = {"data": item}
json.dump(discovery, sys.stdout)
#debug
#json.dump(discovery, sys.stdout,indent=2)