set oShell = WScript.CreateObject("WScript.shell")
oShell.run "mongod"
wScript.Sleep 2000
oShell.run "npm start --prefix C:/Users/Joseph/code/009yellow-beacon/v3_Final/test_website"
WScript.Sleep 2000
oShell.run "python C:/Users/Joseph/code/009yellow-beacon/v3_Final/queen_controller.py"
WScript.Sleep 2000
oShell.run """C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"""
WScript.Sleep 2000
oShell.SendKeys "{F11}"