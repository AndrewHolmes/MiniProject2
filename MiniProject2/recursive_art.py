""" TODO: Put your header comment here """

import random
import math
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    depth = random.randint(min_depth, max_depth) #Randomly chooses an integer in the range specified, including the two specified endpoints, and assigns it as the depth of the function
    f = [] #Creates an empty list on first run through and nested lists on subsequent recursive passes
    functs = ['prod', 'avg', 'cos_pi', 'sin_pi', 'square', 'natural_exponent'] #List of function names to choose from (functions are further defined in evaluate_random_function)
    variables = [['x'], ['y']] #List of variables to choose from; x represents the horizontal axis and y the vertical axis
    f.append(random.choice(functs)) #Randomly chooses one of the functions and adds it to f
    i = depth - 1 #Decrements the depth with each pass through the function
    if i <= 1: #When the depth is equal to 1, the function needs to call an x or a y variable that defines the function
        if f[0] == 'prod' or f[0] == 'avg': #Randomly choose between x and y twice because 'prod' and 'avg' take two inputs
            f.append(random.choice(variables))
            f.append(random.choice(variables))
        else:
            f.append(random.choice(variables)) #Randomly add x or y once if the function in use is not 'prod' or 'avg'
    else:
        if f[0] == 'prod' or f[0] == 'avg': #Calls on the function twice, decrementing min_depth and max_depth by 1, randomly choosing two new nested functions, as 'prod' and 'avg' both take two inputs
            f.append(build_random_function(min_depth-1, max_depth-1)) 
            f.append(build_random_function(min_depth-1, max_depth-1))
        else:
            f.append(build_random_function(min_depth-1, max_depth-1)) #Randomly nest another function if the previous function is not 'prod' or 'avg'
    return f #returns the full list of nested functions that will be evaulated in evaluate_random_function


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if f[0] == 'x': #Return the value of x when 'x' appears in f
        return x
    if f[0] == 'y': #Return the value of y when 'y' appears in f
        return y
    if f[0] == 'cos_pi': #Return the cos of pi times the next nested function 
        return math.cos(math.pi*evaluate_random_function(f[1],x,y))
    if f[0] == 'prod': #Return the product of the functions nested within 'prod'
        return evaluate_random_function(f[1],x,y) * evaluate_random_function(f[2],x,y)
    if f[0] == 'avg': #Return the average of the functions nested within 'avg'
        return (evaluate_random_function(f[1],x,y) + evaluate_random_function(f[2],x,y))/2.0
    if f[0] == 'sin_pi': #Return the sin of pi times the next nested function 
        return math.sin(math.pi*evaluate_random_function(f[1],x,y))
    if f[0] == 'square': #Return the nested function to the power of 2
        return evaluate_random_function(f[1],x,y)**2
    if f[0] == 'natural_exponent': #Return the result of exponentiating e to the power of the nested function
        return math.exp(evaluate_random_function(f[1],x,y))


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    value = float(val) #Converts the value from type int to float
    input_interval = input_interval_end - input_interval_start #Calculates the range of the initial interval
    output_interval = output_interval_end - output_interval_start #Calculates the range of the output interval
    if val >= input_interval_start and val <= input_interval_end: #val must fall within the input interval in order for the code to execute
        output_val = (((value - input_interval_start) * output_interval) / input_interval) + output_interval_start + 0.0 #Converts the value from the input interval to the output interval
    else:
        return 0
    return float(output_val)


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


#def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    #im = Image.new("RGB", (x_size, y_size))
    #pixels = im.load()
    # for i in range(x_size):
    #     for j in range(y_size):
    #         x = remap_interval(i, 0, x_size, -1, 1)
    #         y = remap_interval(j, 0, y_size, -1, 1)
    #         pixels[i, j] = (random.randint(0, 255),  # Red channel
    #                         random.randint(0, 255),  # Green channel
    #                         random.randint(0, 255))  # Blue channel

    # im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9) #Builds a random function that dictates RED values in the image
    green_function = build_random_function(7, 9) #Builds a random function that dictates GREEN values in the image
    blue_function = build_random_function(7, 9) #Builds a random function that dictates BLUE values in the image

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
