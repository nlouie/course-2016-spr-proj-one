import requests # import sodapy
import json
import pymongo
import prov.model
import datetime
import uuid

def map(f, R):
    return [t for (k,v) in R for t in f(k,v)]


def reduce(f, R):
    keys = {k for (k,v) in R}
    return [f(k1, [v for (k2,v) in R if k1 == k2]) for k1 in keys]


def jsonGetAll(addr, limit = 50000, offset = 0):
	r = requests.get(addr + "&$limit=" + str(limit) + "&$offset=" + str(offset))
	if len(r.json()) < 1000:
		return r.json()
	else:
		j = r.json()
		offset += limit
		while len(r.json()) == limit:
			r = requests.get(addr + "&$limit=" + str(limit) + '&$offset=' + str(offset))
			j = j + r.json()
			offset += limit
			print(len(j))
		return j

'''

# Until a library is created, we just use the script directly.
exec(open('../pymongo_dm.py').read())

# Set up the database connection.
client = pymongo.MongoClient()
repo = client.repo
repo.authenticate('alice_bob', 'alice_bob')

# Retrieve some data sets (not using the API here for the sake of simplicity).
startTime = datetime.datetime.now()

'''

# Retrieve json files.
j = jsonGetAll('https://data.cityofboston.gov/resource/effb-uspk.json?department=Boston%20Police%20Department')
m = map(lambda k, v: [('2012', float(v['total_earnings']))] if v['department'] == 'Boston Police Department' else [], [("key", v) for v in j])
f0 = reduce(lambda k,vs: (k, sum(vs)/len(vs)), m)

# Retrieve json files.
j = jsonGetAll('https://data.cityofboston.gov/resource/54s2-yxpg.json?department=Boston%20Police%20Department')
m = map(lambda k, v: [('2013', float(v['total_earnings']))] if v['department'] == 'Boston Police Department' else [], [("key", v) for v in j])
f1 = reduce(lambda k,vs: (k, sum(vs)/len(vs)), m)

# Retrieve json files.
j = jsonGetAll('https://data.cityofboston.gov/resource/4swk-wcg8.json?department_name=Boston%20Police%20Department')
m = map(lambda k, v: [('2013', float(v['total_earnings']))] if v['department_name'] == 'Boston Police Department' else [], [("key", v) for v in j])
f2 = reduce(lambda k,vs: (k, sum(vs)/len(vs)), m)()

f = f0 + f1 + f2
f = map(lambda k, v: [(k, {'avg_salary': v})], f)

# Retrieve json files.
#j = jsonGetAll("https://data.cityofboston.gov/resource/7cdf-6fgx.json?")
#m = map(lambda k, v: [(k, 1)], [(v['year'], v) for v in j])
#f2 = reduce(lambda k, vs: (k, sum(vs)), m)

f3 = [('2014', 88058), ('2015', 49760), ('2013', 87052), ('2012', 43186)]
f3 = map(lambda k, v: [(k, {'incidenct_count': v})], f3)

# Retrieve json files.


