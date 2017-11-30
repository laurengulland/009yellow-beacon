BEFORE YOU PUSH ANYTHING
 - create a .gitignore file
 - inside, paste in the following

    node_modules/
    npm-debug.log
    data/db

DO THE TERMINAL STUFF IN THE TEST_WEBSITE FOLDER
how to set up
 - install node
 - install mongodb (Tablet: 32-bit Windows: https://www.mongodb.org/dl/win32/i386)
    - you might need to add mongoDB on your enviroment variables [instructions for pc only, for mac pls google]
        - search for environment variables
        - click on environment var
        - edit path
        - new 
        - find where you installed mongodb all the way down to bin
        - save
        - open a new termimnal and run mongod and see if it works
 - on a terminal, run npm install

how to run
on one terminal:
- create a data/db/ folder
- then run: mongod --dbpath data/db/

on another terminal:
- then run: npm start
- if terminal complains that the port is taken, go on task manager and kill the node process

go on browser and and go to http://localhost:3001/
