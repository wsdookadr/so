So the main loop will position your cuboids rotated around the origin
at an angle which is a multiple of 45 degrees.  Inside the loop, you
now want to draw the cuboids, and right after that, relative to the
position of each cuboid, you make a few more transformations (a rotation
and translation) to get the cylinders to pass through the centers of the
cuboids (It also helps if the height of the cylinder is bigger than the
side of the cuboid so you can actually see it passing through):






