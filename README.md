# Robotic Researcher
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/thomastli/robotic-researcher/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/thomastli/robotic-researcher/tree/main)
[![CodeFactor](https://www.codefactor.io/repository/github/thomastli/robotic-researcher/badge)](https://www.codefactor.io/repository/github/thomastli/robotic-researcher)
[![codecov](https://codecov.io/gh/thomastli/robotic-researcher/branch/main/graph/badge.svg?token=LBpMFr2s6k)](https://codecov.io/gh/thomastli/robotic-researcher)

The demo of the robot can be run via `main.py`

Unit tests for `robotics.py` can be run via `test_robotics.py`

## Implementation
The robot will retrieve the required information (date of birth, date of death, background) from Wikipedia via the RPA Framework and calculate the age.

As a bonus feature, the robot will also convert the retrieved information into a pandas Dataframe and perform the following analysis:
* Scientists sorted by date of birth (ascending)
* Scientists sorted by date of death (descending)
* Scientists sorted by age (ascending)
* The average age of all scientists

## Limitations 
The error handling in the submission will handle basic exceptions thrown by the RPA framework, log when errors are encountered, and attempt to recover by doing the following:

* With a missing background, the robot sets the background to "Not available"
* With a missing date of birth, the robot will set the date of birth to the current date
* With a missing date of death, the robot will set the date of death to the current date 


## Future Work
A more robust error handling and validation scheme would be ideal if future work was done on the submission. 

Also, more unit tests around edge cases would be another area of future work.
