#! /home/ntppro/Work/pet/bin/python

from urllib.request import Request, urlopen
import json
import datetime


token = "107d2c3d3c8f5f695d9c9841571fd88a788769bd"
ca_certificates = "/etc/ssl/certs"


def getData():
	req = Request("https://api.todoist.com/rest/v1/tasks", 
		headers={"Authorization": "Bearer {}".format(token)})

	try:
		res = urlopen(req, capath=ca_certificates).read().decode()
		result = json.loads(res)

	except:
		result = []
		
	with open("data.txt", "w") as f:
		f.write(res)

	return result


def getTasks():
	result = getData()
	data = dict()

	for r in result:
		try:
			task, time = r["content"].split(':')

			if len(time.split('h')) == 2:
				totalTime = int(time.split('h')[0]) * 60

				if time.split('h')[1] != '':
					totalTime += int(time.split('h')[1])

				data[task] = {"id": r["id"],"expect": totalTime, "actual": 0}
		except:
			pass

	return list(data.items())


def getEvents():
	result = getData()
	data = dict()

	for r in result:
		try:
			task, time = r["content"].split(':')

			if len(time.split('.')) == 2:
				h, m = map(int, time.split('.'))

				data[task] = {"id": r["id"], "expect": datetime.time(h,m,0), "actual": 0}

		except:
			pass

	return list(data.items())


if __name__ == '__main__':
	print(getTasks())
	print(getEvents())