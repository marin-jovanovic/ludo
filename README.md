# ludo

work in progress


Welcome to the Ludo repository! Ludo is a classic board game for two to four players, in which the players race their four tokens from start to finish according to the roll of a dice.

This repository contains the source code for a Ludo game implemented in Python (Django) and JS (Vue) using Postgres as database. 
The game features a GUI built with Vue, and it allows users to play against each other or against an AI opponent.

## Getting Started

To run the game, clone the repository and navigate to the root directory:

    git clone https://github.com/marin-jovanovic/ludo.git
    cd ludo

Install the required dependencies:

    python manage.py makemigrations
    python manage.py migrate
    pip install -r requirements.txt
    npm i 

Run the game:

    python manage.py runserver
    npm run serve

## Gameplay

To start a new game, click the "New Game" button in the main menu. Select the number of players (either 2, 3, or 4) and the number of AI opponents (if any).

Each player takes turns rolling the dice and moving their tokens according to the rules of the game. The first player to get all of their tokens to the finish wins the game.

## Acknowledgements

This game was developed as a project for the Web course at the Faculty of Electrical Engineering and Computer Science, University of Maribor.

## License


This project is licensed under the MIT License - see the LICENSE file for details.
