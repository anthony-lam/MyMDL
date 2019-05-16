import mdl
from display import *
from matrix import *
from draw import *
import math

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print ("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    # print symbols
    for command in commands:
        if command["op"] == "push":
            stack.append([x[:] for x in stack[-1]])
        if command["op"] == "pop":
            stack.pop()
        if command["op"] == "move":
            args = command["args"]
            tmp = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        if command["op"] == "rotate":
            args = command["args"]
            theta = args[1] * (math.pi/180)
            if args[0] == 'x':
                tmp = make_rotX(theta)
            elif args[0] == 'y':
                tmp = make_rotY(theta)
            else:
                tmp = make_rotZ(theta)
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
            tmp = []
        if command["op"] == "scale":
            args = command["args"]
            tmp = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        if command["op"] == "box":
            args = command["args"]
            add_box(tmp,
                    args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            if (command['constants']):
                reflect = command['constants']
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []
        if command["op"] == "sphere":
            args = command["args"]
            add_sphere(tmp,
                       args[0], args[1], args[2], args[3], step_3d)
            matrix_mult( stack[-1], tmp )
            if (command['constants']):
                reflect = command['constants']
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []
        if command["op"] == "torus":
            args = command["args"]
            add_torus(tmp,
                      args[0], args[1], args[2], args[3], args[4], step_3d)
            matrix_mult( stack[-1], tmp )
            if (command['constants']):
                reflect = command['constants']
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []
        if command["op"] == "line":
            args = command["args"]
            add_edge(tmp,
                     args[0], args[1], args[2], args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []
        if command["op"] == "save":
            args = command["args"]
            save_extension(screen, args[0])
            screen = new_screen()
            zbuffer = new_zbuffer()
        if command["op"] == "display":
            display(screen)
