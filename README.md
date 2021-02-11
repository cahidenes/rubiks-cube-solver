# Rubik's Cube Solver
Recognizes Rubik's cubes and solves with Kociemba's two-phase algorithm.

This repository implements only recognizing part. Solution part is imported [(kociemba package)](https://pypi.org/project/kociemba/)

- Aimed for stickerless cubes. Occasionally works for other cubes, worth trying.
- **Key Feature:** Recognizes cube from only two opposite corners, no specific order needed. Easy and fast.

## Demo

![Demo](demo.gif)

## Pip Installs
    pip install opencv-python
    pip install kociemba

## Doesn't Work?
- Make sure all sides of your cube is well lit
- Make sure your cube is aligned nice enough with grid lines (especially the central corner)
- Make sure your finger doesn't cover your cube
- Remove logo sticker or cover with the appropriate color
- Try again with different corners or rotations (if you have passed the first corner, you can't choose any corner)
- Try again with flat color background
- Open an issue with screenshots provided

## Possible Further Improvements
- Support for cubes with stickers
- Recognize cubes anywhere on the screen
- Better UI

_Feel free to contribute or use in your projects :)_
