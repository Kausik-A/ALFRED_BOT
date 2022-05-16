import sys
import requests
import json 
import os
import random

verified_approvers = os.environ.get('approvers').split()
verified_reviewers = os.environ.get('reviewers').split()
random_approvers = random.sample(verified_approvers,2)
print(verified_approvers)
print(verified_reviewers)
def check_permission(flag, user):
    if flag == 1 and user in verified_reviewers:
        return True
    elif flag == 2 and user in verified_approvers:
        return True
    else:
        return False

auth=("Kausik-A",os.environ.get('API_ACCESS_KEY'))
url = f"{sys.argv[1]}/labels"
comment_string = str(sys.argv[2])

# add lgtm label
def add_lgtm():
    data = {"labels": ["lgtm"]}
    requests.post(url, auth=auth, json=data)
    print("lgtm added")

    comment_data = {"body": f"The PR is reviewed, I recommend to cc @{random_approvers[0]} and @{random_approvers[1]} in the comments as approvers."}
    requests.post(f"{sys.argv[1]}/comments", auth=auth, json=comment_data)
    

#remove lgtm label
def remove_ltgm():
    requests.delete(f"{url}/lgtm", auth=auth)
    requests.delete(f"{url}/ready-for-merge", auth=auth)
    print("lgtm removed")

# add approved label
def add_approval():
    url_2 = requests.get(url, auth=auth)
    all_labels = []
    for i in url_2.json():
        all_labels.append(i["name"])

    if "lgtm" in all_labels:
        data = {"labels": ["ready-for-merge"]}
        requests.post(url, auth=auth, json=data)
        print("approved")

    else:
        print("Please add lgtm label first")
    
#remove approval label
def remove_approval():
    requests.delete(url+"/ready-for-merge", auth=auth)
    print("approved removed")


if comment_string == "/lgtm":
    if check_permission(1,sys.argv[3]):
        add_lgtm()
    else:
        print("You are not allowed to add lgtm")
elif comment_string == "/lgtm_cancel":
    if check_permission(1,sys.argv[3]):
        remove_ltgm()
    else:
        print("You are not allowed to remove lgtm")
elif comment_string == "/approve":
    if check_permission(2,sys.argv[3]):
        add_approval()
    else:
        print("You are not allowed to add approve")
elif comment_string == "/approve_cancel":
    if check_permission(2,sys.argv[3]):
        remove_approval()
    else:
        print("You are not allowed to remove approve")

