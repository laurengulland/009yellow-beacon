how to set up
 - install node
 - install mongodb (Tablet: 32-bit Windows: https://www.mongodb.org/dl/win32/i386)
 - Tablet/Windows: [Edit Environmental Variables for Your Account]>
 - on a terminal, run npm install

how to run
on one terminal:
- create a data/db/ folder
- then run: mongod --dbpath data/db/

on another terminal:
- then run: npm start
- if terminal complains that the port is taken, go on task manager and kill the node process

go on browser and and go to http://localhost:3001/
