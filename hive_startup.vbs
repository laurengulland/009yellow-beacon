set oShell = WScript.CreateObject("WScript.shell")
oShell.run "mongod"
wScript.Sleep 2000
oShell.run "npm start --prefix C:/Users/Joseph/code/009yellow-beacon/v3_Final/test_website"
WScript.Sleep 2000
oShell.run "python C:/Users/Joseph/code/009yellow-beacon/v3_Final/hive_controller.py"
WScript.Sleep 2000
oShell.run """C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"""
WScript.Sleep 4000
oShell.sendKeys "{F6}"
WScript.Sleep 200
oShell.sendKeys "localhost:3001"
WScript.sleep 200
oShell.sendKeys "{ENTER}"
WScript.Sleep 200
oShell.SendKeys "{F11}"