Proj2: Conway's Game of Life 

(a) what concerns you identified, and how you separated them; 
    Rules of the game:
      - LifeRules.js
      - seperate java document and class
    Layout of the board: 
      - html and css document
    User interaction: 
      - controller.js
      - seperate class for ocntroller methods
    Initialization of board and buttons
      - boardinit.js
      - board is intially populated and intialized here
      - buttons are also initialized with listeners here

(b) what the program modules are, what their dependences are on one another, and whether there are any dependences that should ideally be eliminated;
    boardInit depends: board, LifeRules, and controller --> should not rely on board directly
    controller depends: board
    LifeRules depends: board
    
(c) how you exploited functionals in your code; 
    - used filter to filter through lists of cells to evaluate which is dead or alive

(d) any interesting design ideas you had or tradeoffs that you made.
    - convenience vs seperation of concerns and dependencies
    - choosing divs over canvases for ease in selecting by IDs
