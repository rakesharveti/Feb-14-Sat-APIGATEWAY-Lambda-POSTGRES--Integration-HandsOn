#!/bin/bash

mkdir package
pip install -r requirements.txt -t package
cp lambda_function.py package/
cd package
zip -r ../lambda-deployment.zip .
