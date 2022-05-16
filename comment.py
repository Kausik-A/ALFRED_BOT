import requests
import random
import sys
import os

auth=("Kausik-A","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")
#url = f'https://api.github.com/repos/Kausik-A/Alfred/issues/19/comments'
url = f"{sys.argv[1]}"
verified_reviewers = os.environ.get('reviewers').split()
element = random.sample(verified_reviewers,2)
print(element) 
data = {"body": f"Thank you for your contribution, I recommend to cc @{element[0]} and @{element[1]} in the comments as reviewers."}
print(requests.post(url, auth=auth, json=data))