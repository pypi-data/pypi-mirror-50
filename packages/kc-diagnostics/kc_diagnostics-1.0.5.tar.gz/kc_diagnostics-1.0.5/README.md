# Diagnostics Pypi
Fawad Mazhar <fawad.mazhar@nordcloud.com> 2019

## Overview
A python package that can be included into your serverless projects. This package is tailored for AWS lambda.  

The package generates necessary alerts based on incoming message. It first reads a configuration file and based on that, it returns alerts along with the available translations. 

## Runtime
Python v2.7

## Pre-requisites
You will need to install:
  * Python
  * pip
  
## Install
```
pip install kc-diagnostics
```

## Getting Started
```
from kc_diagnostics import diagnostics
alerts = diagnostics( dumped_json )
```

## Prerequisites for the consuming application
Install dependenies
```
  pip install boto3 pathlib
```
Export required environment variables:
```
export AWS_REGION=
export BUFFERS_TABLE_NAME=
export TRIGGERS_TABLE_NAME=
```
Make sure these dynamodb tables exist in your desired AWS account.

Add permissions to your lambda function. For example:
```
Effect: Allow
Action:
  - dynamodb:Query
  - dynamodb:Scan
  - dynamodb:GetItem
  - dynamodb:PutItem
  - dynamodb:UpdateItem
  - dynamodb:BatchGetItem
Resource:
  - {"Fn::Join": ["", ["arn:aws:dynamodb:", {"Ref": "AWS::Region"}, ":", {"Ref":"AWS::AccountId"}, ":table/${BUFFERS_TABLE_NAME}"]]}
  - {"Fn::Join": ["", ["arn:aws:dynamodb:", {"Ref": "AWS::Region"}, ":", {"Ref":"AWS::AccountId"}, ":table/${TRIGGERS_TABLE_NAME}"]]}  
```

## Available Translations
```
German
Spanish
French
Italian
Portuguese
```