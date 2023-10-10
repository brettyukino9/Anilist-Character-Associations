import csv
import json
import os
import webbrowser
from pip._vendor import requests
import sys
import math
import time
# arg 1 = name
# arg 2 = other specified character (list users with both)

start = time.time()
map = {}
crossover_count_map = {}
username = "higui"
specified = sys.argv[1]
other_specified = ""
if(len(sys.argv) >2) :
    other_specified = sys.argv[2]

# Make query to get user Id
queryOld = '''
query($name:String){User(name:$name){id}}
'''

# Define our query variables and values that will be used in the query request
variablesOld = {
    'name': username
}

url = 'https://graphql.anilist.co'

# Make the HTTP Api request to get the user id of the username
response = requests.post(url, json={'query': queryOld, 'variables': variablesOld}).json()
userId = response['data']['User']['id']

# Define our query variables and values that will be used in the query request
variables = {
    'userId': userId
}

# Get all user favorites
users = {}
queries = {}
pages = 10 #1200 users per page, 24 a's on a page, 50 users per a
for i in range(1, pages+1) : 
  # 1 = 1,25 = (i-1) * 25 - (i-2) = i * 25 - (i -1 )
  # 2 = 25, 49 = (i-1) * 25 - (i-2) = i * 25 - (i -1 )
  # 3 = 49, 73 = (i-1) * 25 - (i-2) = i * 25 - (i -1 )
  # 4 = 73, 97 = (i-1) * 25 - (i-2) = i * 25 - (i -1 )
  idk = ''
  for x in range((i-1) * 25 - (i-2), i * 25 - (i -1 )) :
    toAdd = "a"+str(x)+''': Page(page: '''+str(x)+''') {
      following(userId: $userId, sort: ID) {
        ...stuff
      }
    }
    '''
    idk = idk+toAdd

  query ='''
    query ($userId: Int!) { '''+idk+ ''' User(id: $userId) {
      ...stuff
    }
  }

  fragment stuff on User {
    name
    favourites {
      characters1: characters(page: 1) {
        nodes {
          name {
            full
          }
        }
      }
      characters2: characters(page: 2) {
        nodes {
          name {
            full
          }
        }
      }
      characters3: characters(page: 3) {
        nodes {
          name {
            full
          }
        }
      }
      characters4: characters(page: 4) {
        nodes {
          name {
            full
          }
        }
      }
    }
  }
  '''
  users[i] = requests.post(url, json={'query': query, 'variables': variables}).json()
#   print(users[i])

print("done with api requests after {sec} seconds".format(sec = time.time() - start))
# Go through everyones favorites
user_count = 0
both_specified = []
for x in range(1, pages * 25 - (pages -1 )) :
    num = math.floor((x-1)/24)+1
    for user in users[num]['data']['a'+str(x)]['following'] :
        of_interest_found = 0
        name = user['name']
        user_count +=1
        chars_found_before_of_interest = []
        for y in range(1,5) :
            for i in user['favourites']['characters'+str(y)]['nodes']:
                char = i['name']['full']
                if(char == specified) :
                    of_interest_found=1
                else:
                    if(of_interest_found) :
                        if(char == other_specified) :
                            both_specified.append(name)
                        if(char in crossover_count_map) :
                            crossover_count_map[char] = crossover_count_map[char] + 1
                        else :
                            crossover_count_map[char] = 1
                    else:
                        chars_found_before_of_interest.append(char)
                if(char in map) :
                    map[char] = map[char] + 1
                else :
                    map[char] = 1
        if(of_interest_found) :
            for char in chars_found_before_of_interest:
                if(char == other_specified) :
                    both_specified.append(name)
                if(char in crossover_count_map) :
                    crossover_count_map[char] = crossover_count_map[char] + 1
                else :
                    crossover_count_map[char] = 1
          

# res = {key: val for key, val in sorted(map.items(), key = lambda ele: ele[1], reverse = True)}
# [print(key,':',value) for key, value in res.items()]
res2 = {key: val for key, val in sorted(crossover_count_map.items(), key = lambda ele: ele[1], reverse = True)}
# [print(key,':',value) for key, value in res2.items()]

# Figure out how liking the specified character affects the accuracy; report the biggest changes
new_chances_map = {}
lifts = {}
for key, value in res2.items() :
    if(crossover_count_map[key] < 7) :
        continue
    chance_normally = map[key] / user_count
    chance_given_specified = crossover_count_map[key] / map[specified]
    new_chance = chance_given_specified / chance_normally
    new_chances_map[key] = new_chance

    support_x_or_y = (map[specified]+map[key]-crossover_count_map[key])/user_count
    support_x = map[specified]/user_count
    support_y = map[key]/user_count
    lifts[key] = support_x_or_y/ (support_x * support_y)


res3 = {key: val for key, val in sorted(new_chances_map.items(), key = lambda ele: ele[1], reverse = True)}
res4 = {key: val for key, val in sorted(lifts.items(), key = lambda ele: ele[1], reverse = True)}


with open('Results/'+specified+' results.txt', 'w', encoding='utf8') as f:
    f.write("Most likely characters someone will like if they like "+specified+"\n")
    f.write("-----------------------------------------------------------------------\n")
    for key, value in res3.items() :
        f.write(key+' : '+str(value)+"x\n")

with open('Results/'+specified+' lift results.txt', 'w', encoding='utf8') as f:
    f.write("Most likely characters someone will like if they like "+specified+"\n")
    f.write("-----------------------------------------------------------------------\n")
    for key, value in res4.items() :
        f.write(key+' : '+str(value)+"x\n")

if(other_specified != "") :
    print("People with both {n1} and {n2} favorited".format(n1=specified, n2=other_specified), both_specified)
print("done with script after {sec} seconds".format(sec = time.time() - start))