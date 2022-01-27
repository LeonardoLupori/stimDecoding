from psychopy import core, visual
import numpy as np
import math
from time import sleep

"""
Trial_flickeringShapes CLASS

This class can be used to generate complex visual stimuli in which a geometric 
shape, containing a phase-reversing checkerboard pattern, is presented.

It works by generating stimuli inside a psychopy window object that has to be
provided in the stimWin argument. All the shapes require the use of a psychopy
aperture object that also has to be provided as the aperture argument.

Optionally, the class can also send a trigger through a parallel port at the beginning of 
each trial to trigger recording equipment. To do this, you have to provide a
psychopy parallelPort object as the optional pPort object. Also you have to specify 
which of the 8 pins of the LPT port you want to use as a trigger with the triggerPin 
argument (default:1).

Parameters of the visual stimulation can be fine tuned by changing the various
arguments at the moment of object instantiation.

Run a trial for a Trial_flickeringShapes object with the method doTrial()

For an example use case of how to use the class see the section under
if __name__ == "__main__"
"""


class Trial_flickeringShapes:
    def __init__(self,
                stimWin,                    # Psychopy window object
                aperture,                   # Psychopy aperture object
                pPort = 0,                  # Psychopy parallel port object (for triggering)
                triggerPin = 1,             # If the parallel port is available, which pin to use
                shape = 'cross',            # Stimulus shape. can be 'cross','triangle', or 'circle'
                width = 20,                 # Width (in degrees) of the shape
                stroke = 2,                 # Thickness of the shape
                chkbrdTempFreq = 5,         # Temporal freq of the flickering checkerboard
                chkbrdSpFreq = 0.08,        # Spatial frequency of the checkerboard
                chkbrdContrast = 0.8,       # Contrast of the checkerboard
                prestimFrames = 60,         # Number of 'gray' frames before the stimulus onset
                                            # This is in the context of the stimulation monitor refresh rate
                                            # so 60 frames in a 60Hz monitor will be 1 second
                stimFrames = 60,            # Number of frames the stimulus is visible
                postStimFrames = 180,       # Number of post-stimulation 'gray' frames
                ):

        self.stimWindow = stimWin
        self.aperture = aperture
        self.pPort = pPort 
        self.triggerPin = triggerPin
        self.shape = shape
        self.width = width
        self.stroke = stroke
        self.chkbrdTempFreq = chkbrdTempFreq
        self.chkbrdSpFreq = chkbrdSpFreq
        self.chkbrdContrast = chkbrdContrast
        self.prestimFrames = prestimFrames
        self.stimFrames = stimFrames
        self.postStimFrames = postStimFrames

        # Check that a supported shape is requested
        msg = "Shape must be one of 'cross','triangle', or 'circle'"
        assert shape in ['cross', 'triangle', 'circle', 'square', 'h_letter',
                         'v_letter', 'star', 't_letter', 's_letter', 'w_letter', msg]
        
        # Check that the pin for the trigger is an int between 1 and 8
        msg = "triggerPin must be an integer between 1 and 8."
        if not isinstance(self.triggerPin, int):
            raise NameError(msg)
        if self.triggerPin>8 or self.triggerPin<1:
            raise NameError(msg)
        # Calculate the value to send to the parallel port to switch up only the
        # desired pin
        self.trigValue = 2**(self.triggerPin-1)

        # Calculate the proper shape coordinates
        # coord is a (M by 2 by 2) np array.
        # coord[:,:,0] are the [x,y] coordinates of the outer edges of the shape;
        # coord[:,:,1] are the [x,y] coordinates of the inner edges in case the 
        # shape has a hole (like circle and triangle), otherwise it is empty.
        if shape == 'cross':
            coord = self._crossCoordinates(width=width, stroke=stroke)
        elif shape == 'triangle':
            coord = self._triangleCoordinates(width=width, stroke=stroke)
        elif shape == 'circle':
            coord = self._circleCoordinates(width=width, stroke=stroke)
        elif shape == 'square':
            coord = self._squareCoordinates(width=width, stroke=stroke)
        elif shape == 'h_letter':
            coord = self._h_letterCoordinates(width=width, stroke=stroke)
        elif shape == 'v_letter':
            coord = self._v_letterCoordinates(width=width, stroke=stroke)
        elif shape == 'star':
            coord = self._starCoordinates(width=width, stroke=stroke)
        elif shape == 't_letter':
            coord = self._t_letterCoordinates(width=width, stroke=stroke)
        elif shape == 's_letter':
            coord = self._s_letterCoordinates(width=width, stroke=stroke)
        elif shape == 'w_letter':
            coord = self._w_letterCoordinates(width=width, stroke=stroke)

        # Generate the coordinates for restricting the stimulus visibility by
        # using both aperture and an optional shapeStim for shapes with holes
        if coord.ndim > 2:          # For shapes with a hole
            self.outerEdges = coord[:,:,0]
            self.innerEdges = coord[:,:,1]
        else:                       # For shapes without a hole
            self.outerEdges = coord
            self.innerEdges = [[0,0]]   # Dummy value

        # Generate the Background Checkerboard
        chkb_texture = np.array([[-1,1],[1,-1]])
        self.checkerboard = visual.GratingStim(
            self.stimWindow,
            size = [180,180],           # 180 degrees to get full field coverage
            sf = self.chkbrdSpFreq,
            contrast = self.chkbrdContrast,
            ori = 0,
            tex = chkb_texture,
            autoDraw = False
        )

        # Shape object for filling central holes in stimuli shapes like circle 
        # or triangle with a gray patch
        self.outBckg = visual.ShapeStim(
            self.stimWindow,
            vertices = self.innerEdges, 
            fillColor = [0,0,0],            # gray
            lineWidth=0
            )

        # Generate a clock for flickering the background checkerboard
        self.revClock = core.Clock()
        self.revClock.reset()

    def doTrial(self):
        # Change the aperture to only render the central part of the stimulus
        # This uses internal functions of the psychopy aperture class since by default
        # they don't allow updating vertices of an already created aperture.
        self.aperture._shape.vertices = self.outerEdges
        self.aperture._needVertexUpdate = True
        self.aperture._reset()

        # Send a Trigger for the start of the trial in case the user specified 
        # a parallel port object
        if self.pPort != 0:
            self.pPort.setData(int("00000000",2))   # Force all the pins LOW
            sleep(.001)                             # 1ms trigger length
            self.pPort.setData(int("00010001",2))
            # self.pPort.setData(self.trigValue)      # Pull back HIGH the desired pin 

        # STIMULATION LOOP
        # -----------------------------    

        # PRESTIM
        for _ in range(self.prestimFrames):
            self.stimWindow.flip()
        # STIMULUS
        for _ in range(self.stimFrames):
            if self.revClock.getTime() >= 1/self.chkbrdTempFreq:
                self.checkerboard.phase += (0.5, 0)
                self.revClock.reset()

            self.checkerboard.draw()
            self.outBckg.draw()
            self.stimWindow.flip()
        # POSTSTIM
        for _ in range(self.postStimFrames):
            self.stimWindow.flip()

        sleep(0.1)
        if self.pPort != 0:
            self.pPort.setData(int("00000001",2))   # Force all the pins LOW
        
    #---------------------------------------------------------------------------
    #--- INTERNAL FUNCTIONS
    #---------------------------------------------------------------------------

    def _crossCoordinates(self, width=10, stroke=2):
        # Calculates the coordinates of the 12 vertices of a cross (square form 
        # factor since witdh = height) given its width and the desired thickness
        height = width
        coord = np.zeros([12,2])
        coord[0,:] = np.array([-(width/2) - stroke, height/2])
        coord[1,:] = np.array([-(width/2) + stroke, height/2])
        coord[2,:] = np.array([0, (height/2)*stroke/(width/2)])
        coord[3,:] = np.array([-coord[1,0], height/2])
        coord[4,:] = np.array([-coord[0,0], height/2])
        coord[5,:] = np.array([stroke,0])
        coord[6,:] = np.array([coord[4,0], -height/2])
        coord[7,:] = np.array([coord[3,0], -height/2])
        coord[8,:] = np.array([0, -coord[2,1]])
        coord[9,:] = np.array([coord[1,0], -height/2])
        coord[10,:] = np.array([coord[0,0], -height/2])
        coord[11,:] = np.array([-stroke,0])

        coord[[0,1,3,4],1] += stroke
        coord[[6,7,9,10],1] -= stroke
        return coord

    def _triangleCoordinates(self, width=10, stroke=2):
        # Calulates the coordinates of the 6 vertices of an equilateral triangle. 

        aboveZero = (width/2) / math.cos(math.radians(30))

        coordInt = np.zeros([3,2])
        coordExt = np.zeros([3,2])
        coordExt[0,:] = np.array([0, aboveZero+stroke])
        coordExt[1,:] = np.array([(aboveZero+stroke)* math.cos(math.radians(30)), 
            -(aboveZero+stroke)* math.sin(math.radians(30))])
        coordExt[2,:] = np.array([-coordExt[1,0], coordExt[1,1]])
        coordInt[0,:] = np.array([0, aboveZero-stroke])
        coordInt[1,:] = np.array([(aboveZero-stroke)* math.cos(math.radians(30)),
            -(aboveZero-stroke)* math.sin(math.radians(30))])
        coordInt[2,:] = np.array([-coordInt[1,0], coordInt[1,1]])

        # Center the triangle vertically
        offsetUp = aboveZero - (width/2)
        coordExt[:,1] = coordExt[:,1] - offsetUp
        coordInt[:,1] = coordInt[:,1] - offsetUp

        coord = np.dstack((coordExt, coordInt))
        return coord

    def _circleCoordinates(self, width=10, stroke=2):
        # Calulates the coordinates of 2 circles. 100 [x,y] coordinates are calculated
        # which are usually fine for a relatively smooth circle  
        coordExt = self._calcEquilateralVertices(100, radius = width/2 + stroke)
        coordInt = self._calcEquilateralVertices(100, radius = width/2 - stroke)

        coord = np.dstack((coordExt, coordInt))
        return coord

    def _calcEquilateralVertices(self, edges, radius=5):
        # Get vertices for an equilateral shape with a given number of sides
        d = np.pi * 2 / edges
        vertices = np.asarray(
            [np.asarray((np.sin(e * d), np.cos(e * d))) * radius
             for e in range(int(round(edges)))])
        return vertices

    def _squareCoordinates(self, width=10, stroke=2):
        # calculates the 8 coordinates of external and internal square
        coordExt = np.zeros([4,2])
        coordInt = np.zeros([4,2])

        coordExt[0,:] = [-width/2 - stroke, -width/2 - stroke]
        coordExt[1,:] = [width/2 + stroke, -width/2 - stroke]
        coordExt[2,:] = [width/2 + stroke, width/2 + stroke]
        coordExt[3,:] = [-width/2 - stroke, width/2 + stroke]

        coordInt[0, :] = [-width/2 + stroke, -width/2 + stroke]
        coordInt[1, :] = [width/2 - stroke, -width/2 + stroke]
        coordInt[2, :] = [width/2 - stroke, width/2 - stroke]
        coordInt[3, :] = [-width/2 + stroke, width/2 - stroke]

        coord = np.dstack((coordExt, coordInt))
        return coord

    def _h_letterCoordinates(self, width=10, stroke=2):
        # calculates the 12 coordinates of letter H
        coord = np.zeros([12,2])
        coord[0,:] = [-width/2 - stroke, -width/2- stroke]
        coord[1,:] = [-width/2 + stroke, -width/2- stroke]
        coord[2,:] = [-width/2 + stroke, - stroke]
        coord[3,:] = [width/2 - stroke, -stroke]
        coord[4,:] = [width/2 - stroke, -width/2- stroke]
        coord[5,:] = [width/2 + stroke, -width/2- stroke]
        coord[6,:] = [width/2 + stroke, width/2+ stroke]
        coord[7,:] = [width/2 - stroke, width/2+ stroke]
        coord[8,:] = [width/2 - stroke, stroke]
        coord[9,:] = [-width/2 + stroke, stroke]
        coord[10,:] = [-width/2 + stroke, width/2+ stroke]
        coord[11,:] = [-width/2 - stroke, width/2+ stroke]
        return coord

    def _v_letterCoordinates(self, width=10, stroke=2):
        # calculates the 12 coordinates of letter V
        k = stroke/(2*math.sqrt(2))
        coord = np.zeros([6,2])
        coord[0,:] = [0, -width/2 - stroke-k]
        coord[1,:] = [width/2 + stroke/2, width/2-stroke/2]
        coord[2,:] = [width/2 - stroke/2, width/2 + stroke/2]
        coord[3,:] = [0, -width/2 + stroke+k]
        coord[4,:] = [-width/2 + stroke/2, width/2 + stroke/2]
        coord[5,:] = [-width/2 - stroke/2, width/2 - stroke/2]
        return coord

    def _starCoordinates(self, width=10, stroke=2):
        # calculates the 12 coordinates of letter V
        k = (width/2 + stroke ) * 1.2
        coord = np.zeros([10,2])
        coord[0,:] = [-0.6*k, -0.9*k]
        coord[1,:] = [0, -0.4*k]
        coord[2,:] = [0.6*k, -0.9*k]
        coord[3,:] = [0.35*k, -0.15*k]
        coord[4,:] = [0.9*k, 0.25*k]
        coord[5,:] = [0.2*k, 0.25*k]
        coord[6,:] = [0, k]
        coord[7,:] = [-0.2*k, 0.25*k]
        coord[8,:] = [-0.9*k, 0.25*k]
        coord[9,:] = [-0.35*k, -0.15*k]
        return coord

    def _t_letterCoordinates(self, width=10, stroke=2):
        coord = np.zeros([8,2])
        coord[0, :] = [-stroke, -width/2 - stroke]
        coord[1, :] = [stroke, -width/2 - stroke]
        coord[2, :] = [stroke, width/2 - stroke]
        coord[3, :] = [width/2 + stroke, width/2 - stroke]
        coord[4, :] = [width/2 + stroke,width/2 + stroke]
        coord[5, :] = [-width/2 - stroke, width/2 + stroke]
        coord[6, :] = [-width/2 - stroke, width/2 - stroke]
        coord[7, :] = [-stroke, width/2 - stroke]
        return coord

    def _s_letterCoordinates(self, width=10, stroke=2):
        coord = np.zeros([12, 2])
        coord[0,:] = [-width/2 - stroke, -width/2 - stroke]
        coord[1,:] = [width/2 + stroke, -width/2-stroke]
        coord[2,:] = [width/2 + stroke, stroke]
        coord[3,:] = [-width/2 + stroke, stroke]
        coord[4,:] = [-width/2 + stroke, width/2 - stroke]
        coord[5,:] = [width/2 + stroke, width/2 - stroke]
        coord[6,:] = [width/2 + stroke, width/2 + stroke]
        coord[7,:] = [-width/2 - stroke, width/2 + stroke]
        coord[8,:] = [-width/2 - stroke, -stroke]
        coord[9,:] = [width/2 - stroke, -stroke]
        coord[10, :] = [width/2 - stroke, -width/2 + stroke]
        coord[11, :] = [- width/2 - stroke, -width/2 + stroke]
        return coord

    def _w_letterCoordinates(self, width=10, stroke=2):
        coord = np.zeros([12, 2])
        coord[0, :] = [-width/4 - stroke, -width/2 - stroke]
        coord[1, :] = [-width/4 + stroke/2, -width/2 - stroke]
        coord[2, :] = [0, -stroke]
        coord[3, :] = [width/4 - stroke/2, -width/2 - stroke]
        coord[4, :] = [width/4 + stroke, -width/2 - stroke]
        coord[5, :] = [width/2 + stroke, width/2 + stroke]
        coord[6, :] = [width/2 - stroke, width/2 + stroke]
        coord[7, :] = [width/4 - stroke/4, -stroke]
        coord[8, :] = [0, (3/2)*stroke]
        coord[9, :] = [-width/4 + stroke/4, -stroke]
        coord[10, :] = [-width/2 + stroke, width/2 + stroke]
        coord[11, :] = [-width/2 - stroke, width/2 + stroke]
        return coord

# Example implementation of the three stimuli
if __name__ == '__main__':
    """ 
    The monitor setup is only useful to get an approximately reproducible 
    output in many different screens. Feel free to use your own psychopy monitor 
    calibration object in your own experiment.
    """
    from psychopy import monitors
    mon = monitors.Monitor('TestMonitor')
    mon.setDistance(20)
    mon.setWidth(50)


    # Experiment by changing these parameters
    # --------------------------------------------------------------------------
    width = 40          # width in degrees of the shapes
    stroke = 5          # thickness in degrees of the shapes

    chkbrdTempFreq = 4         # Temporal freq of the flickering checkerboard
    chkbrdSpFreq = 0.08        # Spatial frequency of the checkerboard
    chkbrdContrast = 0.6       # Contrast of the checkerboard
    
    prestimFrames = 30         # Number of 'gray' frames before the stimulus onset
    stimFrames = 30           # Number of frames the stimulus is visible
    postStimFrames = 60        # Number of post-stimulation 'gray' frames
    # --------------------------------------------------------------------------

    # Create a Psychopy window object
    stimWin = visual.Window(
        size = (1200,800),
        screen = 0,
        fullscr = True,
        units = 'deg',
        monitor = mon,
        allowStencil = True
    )

    # Create a Psychopy aperture object
    mask = visual.Aperture(stimWin)

    # Create an object for the cross
    cross = Trial_flickeringShapes(
        stimWin,
        mask,
        shape='cross',
        width = width,
        stroke = stroke,
        chkbrdSpFreq=chkbrdSpFreq,
        chkbrdTempFreq=chkbrdTempFreq,
        chkbrdContrast=chkbrdContrast,
        prestimFrames=prestimFrames,
        stimFrames=stimFrames,
        postStimFrames=postStimFrames)

    # Create an object for the circle
    circle = Trial_flickeringShapes(
        stimWin,
        mask,
        shape='circle',
        width = width,
        stroke = stroke,
        chkbrdSpFreq=chkbrdSpFreq,
        chkbrdTempFreq=chkbrdTempFreq,
        chkbrdContrast=chkbrdContrast,
        prestimFrames=prestimFrames,
        stimFrames=stimFrames,
        postStimFrames=postStimFrames)
    
    # Create an object for the triangle
    triangle = Trial_flickeringShapes(
        stimWin,
        mask,
        shape='triangle',
        width = width,
        stroke = stroke,
        chkbrdSpFreq=chkbrdSpFreq,
        chkbrdTempFreq=chkbrdTempFreq,
        chkbrdContrast=chkbrdContrast,
        prestimFrames=prestimFrames,
        stimFrames=stimFrames,
        postStimFrames=postStimFrames)

    # Create an object for the square
    square = Trial_flickeringShapes(
        stimWin,
        mask,
        shape='square',
        width=width,
        stroke=stroke,
        chkbrdSpFreq=chkbrdSpFreq,
        chkbrdTempFreq=chkbrdTempFreq,
        chkbrdContrast=chkbrdContrast,
        prestimFrames=prestimFrames,
        stimFrames=stimFrames,
        postStimFrames=postStimFrames)

    # Create an object for the h_letter
    h_letter = Trial_flickeringShapes(
        stimWin,
        mask,
        shape='h_letter',
        width=width,
        stroke=stroke,
        chkbrdSpFreq=chkbrdSpFreq,
        chkbrdTempFreq=chkbrdTempFreq,
        chkbrdContrast=chkbrdContrast,
        prestimFrames=prestimFrames,
        stimFrames=stimFrames,
        postStimFrames=postStimFrames)

    # Create an object for the v_letter
    v_letter = Trial_flickeringShapes(
        stimWin,
        mask,
        shape='v_letter',
        width=width,
        stroke=stroke,
        chkbrdSpFreq=chkbrdSpFreq,
        chkbrdTempFreq=chkbrdTempFreq,
        chkbrdContrast=chkbrdContrast,
        prestimFrames=prestimFrames,
        stimFrames=stimFrames,
        postStimFrames=postStimFrames)

    # Create an object for the star
    star = Trial_flickeringShapes(
        stimWin,
        mask,
        shape='star',
        width=width,
        stroke=stroke,
        chkbrdSpFreq=chkbrdSpFreq,
        chkbrdTempFreq=chkbrdTempFreq,
        chkbrdContrast=chkbrdContrast,
        prestimFrames=prestimFrames,
        stimFrames=stimFrames,
        postStimFrames=postStimFrames)

    # Create an object for the t_letter
    t_letter = Trial_flickeringShapes(
        stimWin,
        mask,
        shape='t_letter',
        width=width,
        stroke=stroke,
        chkbrdSpFreq=chkbrdSpFreq,
        chkbrdTempFreq=chkbrdTempFreq,
        chkbrdContrast=chkbrdContrast,
        prestimFrames=prestimFrames,
        stimFrames=stimFrames,
        postStimFrames=postStimFrames)

    # Create an object for the s_letter
    s_letter = Trial_flickeringShapes(
        stimWin,
        mask,
        shape='s_letter',
        width=width,
        stroke=stroke,
        chkbrdSpFreq=chkbrdSpFreq,
        chkbrdTempFreq=chkbrdTempFreq,
        chkbrdContrast=chkbrdContrast,
        prestimFrames=prestimFrames,
        stimFrames=stimFrames,
        postStimFrames=postStimFrames)

    # Create an object for the w_letter
    w_letter = Trial_flickeringShapes(
        stimWin,
        mask,
        shape='w_letter',
        width=width,
        stroke=stroke,
        chkbrdSpFreq=chkbrdSpFreq,
        chkbrdTempFreq=chkbrdTempFreq,
        chkbrdContrast=chkbrdContrast,
        prestimFrames=prestimFrames,
        stimFrames=stimFrames,
        postStimFrames=postStimFrames)

    # Show trials for each shape
    for _ in range(1):
        #cross.doTrial()
        #triangle.doTrial()
        #circle.doTrial()
        square.doTrial()
        h_letter.doTrial()
        v_letter.doTrial()
        star.doTrial()
        t_letter.doTrial()
        s_letter.doTrial()
        w_letter.doTrial()

