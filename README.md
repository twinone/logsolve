# log-solve
Logic puzzle game solver

# Basic idea
The idea of this project is to take a phone game (like 
[Simon Tatham's Puzzles](https://play.google.com/store/apps/details?id=name.boyle.chris.sgtpuzzles&hl=en))
and solve it using a programming language (like [Prolog](http://www.swi-prolog.org/)).
Then use a capacitive pen attached to a 3D printer to solve the game on the phone.

This is just a draft for now, so here are the basic steps to reproduce a simple game solving technique:
## 1. Capture & convert the game to a prolog input file. (Capturer)
There are two ways to approach this:
* Capturing a screenshot and reading the SD card. This method reduces the problem-solving to puzzles that are predictable from the initial state.
* Using an external camera. This way we can take pictures or video while playing.

## 2. Solve the game (Solver)
Theoretically this can be done using any language or algorithm, but it will probably be using Prolog and the clpfd library.

## 3. Reproduce the solution on the phone (Executor)
Using a 3D printer we can simulate a finger that plays the game.



Obviously this is a very simple way of solving a game, and has some restrictions, discarding games that:
* Require very fast inputs are discarded
* Use more than a single finger for input, or use accelerometers, etc.



# Design and implementation


For the first design only games that can be solved with a picture of the initial state will be considered.

Since solving logic games is trivial using Prolog or a SAT-solver, focus will initially be on the computer vision part,
recognizing a game and outputting a nicer representation of the game,
that a solver program can understand without dealing with image recognition.


# Progress

Grid detection works reliably across multiple angles for the "Light Up" game. Here is what the process looks like:
<img width="1199" alt="image" src="https://user-images.githubusercontent.com/4309591/27445374-cc6e9d72-5779-11e7-96b6-60a1ecc62c99.png">

From left to right:
* Original image
* Local-thresholding and Gaussian Blur
* Hough line detection
* Largest connected-component convex hull (& detection of warping points)
* Resulting warped image prepared for solving

Here is an example with other games:
<img width="1199" alt="image" src="https://user-images.githubusercontent.com/4309591/27445639-c093ca3a-577a-11e7-8a08-8e72057492d6.png">

It's a pretty robust approach, since it has detected 9 different games without even touching the parameters.

# TODO
- [x] Image capturer
- [ ] Implement number detection
- [ ] Design game representation
- [ ] Solver
- [ ] Solution - 3D printer representation
- [ ] Computer - 3D printer interface
