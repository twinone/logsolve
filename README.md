# log-solve
Logic puzzle game solver using Python, Prolog, scikit-image, a camera and a 3D printer.

# Basic idea
The idea of this project is to take a picture of a game on a phone (like 
[Simon Tatham's Puzzles](https://play.google.com/store/apps/details?id=name.boyle.chris.sgtpuzzles&hl=en))
and solve it using a programming language (like [Prolog](http://www.swi-prolog.org/)).
Then use a capacitive pen attached to a 3D printer to solve the game on the phone.

We can distinguish three stages in the process:

## 1. Capture & convert the game to a numeric representation. (Capturer)
There are two ways to approach this:
* Capturing a screenshot and reading the SD card. This method reduces the problem-solving to puzzles that are predictable from the initial state.
* Using an external camera. This way we can take pictures or video while playing, and interact with the printer while it's solving. **We will be using this approach**.

## 2. Solve the game (Solver)
Theoretically this can be done using any language or algorithm, but it will probably be using Prolog and the clpfd library. Some games contributed by other developers are in other languages, but most of Simon Tatham's Puzzles are to be solved in Prolog.

## 3. Reproduce the solution on the phone (Executor)
Using a 3D printer we can simulate a finger that plays the game.



Obviously this is a very simple way of solving a game, and has some restrictions, discarding games that:
* Require very fast inputs
* Use more than a single finger or the accelerometer as inputs, etc.



# Design and implementation


For the first design only games that can be solved with a picture of the initial state will be considered.

Since solving logic games is trivial using Prolog or a SAT-solver, focus will initially be on the computer vision part,
recognizing a game and outputting a nicer representation of the game,
that a solver program can understand without dealing with image recognition.


# Requirements
* [skimage](http://scikit-image.org/docs/dev/install.html) `pip install scikit-image`



# How it works
Here are the steps that the programs do in order to solve a puzzle

## 1. Capture

Capturing the image and undistorting works reliably across multiple angles across multiple games. Here is what the process looks like with the **Loopy** game:
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


## 2. Grid size detection
We can accurately detect the size of the grid on an undistorted image:
<img width="1201" alt="grid" src="https://user-images.githubusercontent.com/4309591/27477018-2c1f16d4-580b-11e7-9f29-f9a4bd1d177c.png">
From left to right:
* Original undistorted image
* Local-thresholding
* Hough line detection
* Line clustering

The line clustering algorithm first selects horizontal and vertical lines, and groups them by distance. This way we'll have an accurate and redundant map of the grid. If we count the number of groups we get the size of the grid.

#### Testing
We test the undistorted images from the Capture process. Images are manually labeled as nameN-XxY.jpg where X and Y are the width and height in grid cells of the puzzle.

Automated testing of all images in the test folder produces the following result:

```
[PASS] test/fifteen0-4x4.jpg: 4x4
[PASS] test/galaxies0-7x7.jpg: 7x7
...
[PASS] test/unruly0-10x10.jpg: 10x10
[PASS] test/range0-6x9.jpg: 6x9
```

It's a very flexible approach, as there can be both NxM grids and the vertical size of a cell does not need to match the horizontal size.

## 3. Cell classification
In most games we want to be able to distinguish between dark and light cells. This is an easy problem with thresholding. Thresholding converts an image (grayscale) to a binary image (black and white only) pixel by pixel based on whether the pixel meets certain criteria, like being brighter than the mean, or being darker than the mean of the 20x20 pixels surrounding it. If we use all the pixels it's called **global thresholding**, and the same criteria is applied to all pixels. This is a fast approach. Using only the **neighborhood** of a pixel is called **local thresholding** and is a bit slower but can easily solves **shadow** problems. A quick comparison shows the problem with global thresholding.
<img width="895" alt="image" src="https://user-images.githubusercontent.com/4309591/27509816-42c7ede8-5905-11e7-8f06-c30e9ff08773.png">

Just being 'brighter' than the mean value is a little error prone, so we use an **offset** to make sure it's at least brighter by *offset*. Since the brightness of the pixels are between 0 and 1 in this example, an offset of 0.1 worked surprisingly well. We'll use **local thresholding** even though it's a bit slower, because with more aggressive shadows global thresholding could be a problem.

#### Ternary thresholding
Thresholding is nice, but it only classifies pixels in a binary way, a pixel is either in the resulting image or it is not, but in the game *Unruly* there are white, black and empty squares, and we want to detect all three.

The solution is fairly simple, we do **two separate binary thresholdings**, one for the white squares and one for the black squares:
<img width="849" alt="image" src="https://user-images.githubusercontent.com/4309591/27509855-1750c940-5906-11e7-9414-faf2053c157a.png">

The little errors are fine, we will be taking the average color of each cell after thresholding. Just in case it's probably a good idea to only use the center part of a cell for color detection, to avoid errors around the edges:
<img width="849" alt="image" src="https://user-images.githubusercontent.com/4309591/27510113-b5506886-590a-11e7-858e-0a374cd4e492.png">

With a slightly more complicated game, *Light Up*, we can use the same approach, without changing any code, and get the following result:
<img width="840" alt="image" src="https://user-images.githubusercontent.com/4309591/27510226-a645f21e-590c-11e7-9334-a36753395f16.png">

This way we only have to check for numbers on the black cells (and we need to know where they are anyway to solve the game).



## 4. Obtaining a solution

For the **Unruly** game, I've written a small Prolog script that calculates the solution given a problem. Given following problem:
```
10 10
-1 -1 -1 -1  0 -1 -1 -1  0 -1
-1 -1 -1 -1 -1  1 -1 -1 -1  1
-1  0 -1 -1 -1  1 -1 -1 -1 -1
-1 -1 -1 -1  0 -1 -1 -1  1 -1
-1  0 -1 -1 -1 -1 -1  0 -1  1
-1 -1  1 -1 -1 -1 -1 -1 -1  1
-1 -1 -1  0 -1 -1  1 -1  1 -1
-1 -1  0 -1 -1 -1  1 -1 -1 -1
-1 -1 -1 -1 -1 -1 -1 -1 -1  1
 1  0 -1 -1 -1 -1 -1  0 -1  1
```

It prints the following solution and steps:

```
$ ./solve < input.txt 

1 1 0 1 0 0 1 1 0 0 
0 1 0 0 1 1 0 0 1 1 
1 0 1 0 1 1 0 1 0 0 
1 1 0 1 0 0 1 0 1 0 
0 0 1 0 1 0 1 0 1 1 
0 0 1 1 0 1 0 1 0 1 
1 1 0 0 1 0 1 0 1 0 
0 1 0 1 1 0 1 1 0 0 
0 0 1 1 0 1 0 1 0 1 
1 0 1 0 0 1 0 0 1 1 

dclick 1 1
dclick 1 2
click 1 3
[...]
dclick 10 6
click 10 7
dclick 10 9

```

Now this only has to be sent over the network to the 3D printer. To do this we use [pyserial](https://github.com/pyserial/pyserial)

If you take a look at [core/comm](https://github.com/twinone/logsolve/blob/master/core/comm.py), there the minimum required commands to get this project to work, and a [gcode](https://en.wikipedia.org/wiki/G-code) interpreter.
(This will probably be a separate project in the future)

The 3D printer will execute the orders sent to it. You would expect a capacitive pen attached to the printer to do it job,
but it doesn't. [The reason](https://electronics.stackexchange.com/a/60424) is that capacitive pens actually use your body's capacitance, but they don't work if you don't hold them. This results in not working touches most of the time.

To overcome this, we use aluminum foil as capacitive tip instead of a dedicated pen. This allows us to connect the other
end to the phone's charger, and that way the tip is grounded with the phone and works reliably. See [HARDWARE.md](https://github.com/twinone/logsolve/blob/master/HARDWARE.md) for details.

Here is how the (very ugly but functional) prototype looks:

![img](https://user-images.githubusercontent.com/4309591/28494238-8d89affe-6f28-11e7-8018-b26bd3da6cd3.gif)



---


Currently I'm learning about **TensorFlow** and using the **MNIST dataset** seems like the perfect solution to detect numbers. We still need to be able to distinguish between cells with and without numbers, so maybe this part will take some time to be completed. Meanwhile simple games like **Unruly** can already be solved, so both TensorFlow and the solving will be implemented in parallel.



# TODO
- [x] Image capturer
- [x] Detect grid size
- [x] Cell classification and color detection
- [ ] Implement number detection (In progress)
- [x] Design game representation
- [x] Solver
- [x] Solution - 3D printer representation
- [x] Computer - 3D printer interface

