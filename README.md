# Webcam games

This project aims to create mini-games in Python using the recognition algorithms of the Mediapipe library. For the moment, only a Connect 4 has been implemented.

## Usage
### Clone the project
```
git clone https://github.com/mousqtr/WebcamGames.git
```
or download and extract the .zip file

### Create and activate the virtual environment in the folder
```
cd WebcamGames
python -m venv venv
venv\Scripts\activate.bat
```
### Install the libraries 
```
pip install -r requirements.txt
```
### Run the program
```
python main.py
```

## Preview

<img src="/resources/images/preview.png?raw=true" alt="preview" style="width: 400px;"/>

## Connect 4
### Default mode

Use the left and right arrows to move the disk laterally. Once the column is selected, use the down arrow to drag the disc.

<img src="/resources/images/connect4_1.png?raw=true" alt="connect4_1" style="width: 400px;"/>

### Hand control mode

Place your hand over a disc to pick it up. Once caught, place the hand on top of a column and click on the Space key to drop the disc.

<img src="/resources/images/connect4_2.png?raw=true" alt="connect4_2" style="width: 400px;"/>
