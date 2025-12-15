# project-work

### Repository Setup

1. Create a Git repository named project-work.
2. Inside the repository, include:
    - A Python script named Problem.py which generates the problem through the class constructor and the baseline solution. 
    - A Python file named s<student_id>.py that contains a function named solution(p:Problem) which receives as input an instance of the class Problem which generates the problem.
    - A folder named src/ containing all additional code required to run your solution.
    - A TXT file named base_requirements.txt containing the basic python libraries that you need to run the code to generate the problem.


### Main File Requirements (s<student_id>.py)

1. Import the class responsible from Problem.py for generating the problem in your code.
2. Implement a method called solution() to place in s<student_id>.py that returns the optimal path in the following format: 
```python
[(c1, g1), (c2, g2), …, (cN, gN), (0, 0)]
```
where:
- c1, …, cN represent the sequence of cities visited.
- g1, …, gN represent the corresponding gold collected at each city.


### Rules
1. The thief must start and finish at (0, 0).
2. Returning to (0, 0) during the route is allowed to unload collected gold before continuing.
3. Don't forget to change the name of the file s123456.py provided as an example ;).

### Notes
- It is not necessary to push the report.pdf or log.pdf in this repo.
- It is mandatory to upload it in "materiale" section of "portale della didattica" at least 168 hours before the exam call.
- For well commented codes, I can't ensure a higher mark but they would be very welcome.
- In case you face any issue or you have any doubt text me at the email giuseppe.esposito@polito.it and professor Squillero giovanni.squillero@polito.it.