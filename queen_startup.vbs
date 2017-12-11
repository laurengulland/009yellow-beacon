set oShell = WScript.CreateObject("WScript.shell")
oShell.run "mongod --storageEngine=mmapv1 --dbpath C:/Users/009yellow/009yellow-beacon/v3_Final/test_website/data/db/"
wScript.Sleep 2000
oShell.run "npm start --prefix C:/Users/009yellow/009yellow-beacon/v3_Final/test_website"
WScript.Sleep 2000
oShell.run "python C:/Users/009yellow/009yellow-beacon/v3_Final/queen_controller.py"
WScript.Sleep 2000
oShell.run """C:/Program Files/Google/Chrome/Application/chrome.exe"""
WScript.Sleep 5000
oShell.SendKeys "{F11}"