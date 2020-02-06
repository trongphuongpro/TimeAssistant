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
		result = None
		
	# with open("data.txt", "w") as f:
	#  	json.dump(result, f)

	return result


def getTasks():
	result = getData()

	if result is None:
		return None

	data = dict()

	for r in result:
		try:
			task, time = r["content"].split(':')

			if len(time.split('h')) == 2:
				totalTime = int(float(time.split('h')[0]) * 60)

				if time.split('h')[1] != '':
					totalTime += int(time.split('h')[1])

				data[r["id"]] = {"task": task, "expect": totalTime}
		except:
			pass

	return data


def getEvents():
	result = getData()

	if result is None:
		return None

	data = dict()

	for r in result:
		try:
			task, time = r["content"].split(':')

			if len(time.split('.')) == 2:
				h, m = map(int, time.split('.'))

				data[r["id"]] = {"task": task, "expect": datetime.time(h,m,0)}

		except:
			pass

	return data


if __name__ == '__main__':
	print(getTasks())
	print(getEvents())