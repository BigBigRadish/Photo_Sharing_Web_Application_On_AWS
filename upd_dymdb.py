
#
#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
# 
#  http://aws.amazon.com/apache2.0/
# 
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb',region_name='cn-north-1',aws_access_key_id='AKIAVLSEBUAJRL52NPMZ', aws_secret_access_key='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')

table = dynamodb.Table('hire2020-hire-luozhukun1031')
print(table.table_status)
# title = "The Big New Movie"
# year = 2015
# #record user ip , date, time , photo name, photo url into DynamoDB when customer upload photo.
# response = table.put_item(
#    Item={
#         'year': year,
#         'title': title,
#         'info': {
#             'plot':"Nothing happens at all.",
#             'rating': decimal.Decimal(0)
#         }
#     }
# )

# print("PutItem succeeded:")
# print(json.dumps(response, indent=4, cls=DecimalEncoder))
