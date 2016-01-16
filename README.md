# determinator

Build18 2016 project code

This is the code for an intelligent football, which combines data from an embedded IMU with machine learning to provide user data and determine the identity of the person who threw the ball.

The Build18 Football folder contains the arduino code for the project.  An arduino mini hooked up to the IMU in the football uses the library to perform some processing of the data before transmitting it to a listening computer via an XBee.

The imuValueExtractors module provides functions to parse strings from the serial input of the XBee, and return data values corresponding to different readings by the IMU.

serialtest2.py provides the backbone logic for the program, reading data from the serial connection and working to analyze it and determine when the football is thrown.  The program also ties throw data to users for machine learning which it uses to try to predict which user (of those who have recorded data) threw the ball.

interface.py provides the frontend of the program, with an MVC framework.  The user navigates to a screen where they can decide whether to record data for a new user, or receive ML predictions on throws by returning users.  The interface also displays throw statistics after each throw, and announces when users record highscores (strongest throw, farthest throw, most airtime).

config.py holds a set of globals to be shared between the backend and the front end.  The frontend refers to config when updating statistics, and the backend writes data to variables in config.

niceQ.py is a second module providing a special queue designed for holding past data and creating moving averages for comparison purposes.  These are useful when trying to determine whether a user is making a throw.
