# Overview

This is a version of the classic Snake Game using Python and the Arcade library. I created this to demonstrate how to use the Arcade library to create a game that uses Sprite classes, collisions, and sound effects, as well as to learn to use this library myself.

To play the game, you must execute the main.py file. The snake moves automatically in the direction its head is facing. You can control its direction using the keyboard arrows: up, down, left, and right, which move the snake in the corresponding direction. The goal is for the snake to eat as much food (apples) as possible. The snake must avoid colliding with itself. 

Every time the snake eats an apple, the snake grows, and a new apple appears randomly on the game screen. Also, every time your score reaches a multiple of 200 (e. g. 200, 400, 600, etc), the game speed increases up to a speed limit. In this way, as the snake grows larger and moves faster, it is harder to handle.

When the snake collides with itself, the game is over. Your final score will be displayed, and two buttons will appear, which will allow you to either restart the game or quit the game.

Video demonstration: [Software Demo Video](https://youtu.be/uRL3UWxGMEE)

# Development Environment

* Visual Studio Code
* Git / GitHub
* Python 3.11.10 64-bit
* Arcade 2.6.17


# Useful Websites

* [Visual Studio Code](https://code.visualstudio.com/)
* [Python 3.11 Reference Manual](https://docs.python.org/3.11/)
* [Arcade 2.6.17 Documentation](https://api.arcade.academy/en/latest/)
* [Arcade Academy](https://learn.arcade.academy/en/latest/)
* [Python Arcade Tutorial](https://www.youtube.com/playlist?list=PLP6KYkkXj-QbBP0He1Ot5wGgtPbR9hqxR)
* [Arcade Tutorial - RealPython](https://realpython.com/arcade-python-game-framework/)


# Future Work

* Add colliding walls to increase difficulty
* Add music
* Add more sound effects
* Increment functionality so that more than one apple appears at a time
* Improve visual graphics
* Add functionality to save the highest score record