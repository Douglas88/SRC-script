import requests

headers = {"Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IjQ5OTc0NDE4N0BxcS5jb20iLCJpYXQiOjE1NTM5Mjk4MTAsIm5iZiI6MTU1MzkyOTgxMCwiZXhwIjoxNTUzOTczMDEwfQ.vL3-PGNheuoAQ5Lan7HZyTGd70NDpl7gxHUh7f1jI0c"}
url = "https://api.zoomeye.org/host/search?query=phpStudy+Country%3ACN&page="
f = open("ip.txt", "a+")
for i in range(1,2):
    print(i)
    target = url + str(i)
    try:
        response = requests.get(target, timeout = 1, headers = headers)
        print(response.text)
        matches = response.json()["matches"]
        for result in matches:
            ip = result["ip"]
            f.write(ip + "\n")
    except BaseException as e:
        continue
f.close()

