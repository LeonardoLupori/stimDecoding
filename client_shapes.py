from psychopy import visual, monitors, parallel
from stimuli.shapesStimuli import Trial_flickeringShapes
import socket
from time import sleep

# ------------------------------------------------------------------------------
# -- PARAMETERS DEFINITIONS
# ------------------------------------------------------------------------------

# TRIGGER
# ---------------
triggerPin = 1

# STIMULI
# ---------------
shapesWidth = 40
shapesStroke = 5
chkbrdTempFreq = 4
chkbrdSpFreq = 0.08
chkbrdContrast = 0.6
prestimFrames = 30
stimFrames = 30
postStimFrames = 60

# MONITOR
# ---------------
distanceCm = 20
monitorWidthCm = 52
monitorResolution = [1920, 1080]

# TPC/IP Communication
# ---------------
TCP_ip = '192.168.1.2'      # IP address of the recording machine
TCP_port = 40000            # Port to use
TCP_buffSize = 4096

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Setup some monitor parameters
mon = monitors.Monitor('TestMonitor')
mon.setDistance(distanceCm)
mon.setWidth(monitorWidthCm)

# Setup the parallel port
pPort = parallel.ParallelPort(address = '0xD010')
pPort.setData(int("00000001",2))

# Create the main stimulation window
stimWin = visual.Window(
    size = monitorResolution,
    screen = 0,
    fullscr = True,
    units = 'deg',
    monitor = mon,
    allowStencil = True)

# Create the aperture object
mask = visual.Aperture(stimWin)

# Create the cross stimulus object
cross = Trial_flickeringShapes(
    stimWin,
    mask,
    pPort = pPort,
    triggerPin=triggerPin,
    shape='cross',
    width = shapesWidth,
    stroke = shapesStroke,
    chkbrdTempFreq = chkbrdTempFreq,
    chkbrdSpFreq = chkbrdSpFreq,
    chkbrdContrast = chkbrdContrast,
    prestimFrames = prestimFrames,
    stimFrames = stimFrames,
    postStimFrames = postStimFrames
    )
# Create the  circle stimulus object
circle = Trial_flickeringShapes(
    stimWin,
    mask,
    pPort = pPort,
    triggerPin=triggerPin,
    shape='circle',
    width = shapesWidth,
    stroke = shapesStroke,
    chkbrdTempFreq = chkbrdTempFreq,
    chkbrdSpFreq = chkbrdSpFreq,
    chkbrdContrast = chkbrdContrast,
    prestimFrames = prestimFrames,
    stimFrames = stimFrames,
    postStimFrames = postStimFrames
    )
# Create the  triangle stimulus object
triangle = Trial_flickeringShapes(
    stimWin,
    mask,
    pPort = pPort,
    triggerPin=triggerPin,
    shape='triangle',
    width = shapesWidth,
    stroke = shapesStroke,
    chkbrdTempFreq = chkbrdTempFreq,
    chkbrdSpFreq = chkbrdSpFreq,
    chkbrdContrast = chkbrdContrast,
    prestimFrames = prestimFrames,
    stimFrames = stimFrames,
    postStimFrames = postStimFrames
    )

# Create the  square stimulus object
square = Trial_flickeringShapes(
    stimWin,
    mask,
    pPort = pPort,
    triggerPin=triggerPin,
    shape='square',
    width = shapesWidth,
    stroke = shapesStroke,
    chkbrdTempFreq = chkbrdTempFreq,
    chkbrdSpFreq = chkbrdSpFreq,
    chkbrdContrast = chkbrdContrast,
    prestimFrames = prestimFrames,
    stimFrames = stimFrames,
    postStimFrames = postStimFrames
    )

# Create the  h_letter stimulus object
h_letter = Trial_flickeringShapes(
    stimWin,
    mask,
    pPort = pPort,
    triggerPin=triggerPin,
    shape='h_letter',
    width = shapesWidth,
    stroke = shapesStroke,
    chkbrdTempFreq = chkbrdTempFreq,
    chkbrdSpFreq = chkbrdSpFreq,
    chkbrdContrast = chkbrdContrast,
    prestimFrames = prestimFrames,
    stimFrames = stimFrames,
    postStimFrames = postStimFrames
    )

# Create the  v_letter stimulus object
v_letter = Trial_flickeringShapes(
    stimWin,
    mask,
    pPort = pPort,
    triggerPin=triggerPin,
    shape='v_letter',
    width = shapesWidth,
    stroke = shapesStroke,
    chkbrdTempFreq = chkbrdTempFreq,
    chkbrdSpFreq = chkbrdSpFreq,
    chkbrdContrast = chkbrdContrast,
    prestimFrames = prestimFrames,
    stimFrames = stimFrames,
    postStimFrames = postStimFrames
    )

# Create the  star stimulus object
star = Trial_flickeringShapes(
    stimWin,
    mask,
    pPort = pPort,
    triggerPin=triggerPin,
    shape='star',
    width = shapesWidth,
    stroke = shapesStroke,
    chkbrdTempFreq = chkbrdTempFreq,
    chkbrdSpFreq = chkbrdSpFreq,
    chkbrdContrast = chkbrdContrast,
    prestimFrames = prestimFrames,
    stimFrames = stimFrames,
    postStimFrames = postStimFrames
    )

# Create the  t_letter stimulus object
t_letter = Trial_flickeringShapes(
    stimWin,
    mask,
    pPort = pPort,
    triggerPin=triggerPin,
    shape='t_letter',
    width = shapesWidth,
    stroke = shapesStroke,
    chkbrdTempFreq = chkbrdTempFreq,
    chkbrdSpFreq = chkbrdSpFreq,
    chkbrdContrast = chkbrdContrast,
    prestimFrames = prestimFrames,
    stimFrames = stimFrames,
    postStimFrames = postStimFrames
    )

# Create the  s_letter stimulus object
s_letter = Trial_flickeringShapes(
    stimWin,
    mask,
    pPort = pPort,
    triggerPin=triggerPin,
    shape='s_letter',
    width = shapesWidth,
    stroke = shapesStroke,
    chkbrdTempFreq = chkbrdTempFreq,
    chkbrdSpFreq = chkbrdSpFreq,
    chkbrdContrast = chkbrdContrast,
    prestimFrames = prestimFrames,
    stimFrames = stimFrames,
    postStimFrames = postStimFrames
    )

# Create the  s_letter stimulus object
w_letter = Trial_flickeringShapes(
    stimWin,
    mask,
    pPort = pPort,
    triggerPin=triggerPin,
    shape='w_letter',
    width = shapesWidth,
    stroke = shapesStroke,
    chkbrdTempFreq = chkbrdTempFreq,
    chkbrdSpFreq = chkbrdSpFreq,
    chkbrdContrast = chkbrdContrast,
    prestimFrames = prestimFrames,
    stimFrames = stimFrames,
    postStimFrames = postStimFrames
    )

# Start TCP/IP communication with the server PC
tcpObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpObj.connect((TCP_ip, TCP_port))
tcpObj.settimeout(60)


# MAIN STIMULATION LOOP
# The code will sit waiting for incoming messages.
# When it recieves one it will parse it and start the appropriate trial
while True:
    msg = tcpObj.recv(TCP_buffSize)
    msg = msg.decode('utf8')
    print(f'TRIAL: {msg}')

    if msg == 'cross':
        cross.doTrial()
        print('End of Trial')
    elif msg == 'circle':
        circle.doTrial()
        print('End of Trial')
    elif msg == 'triangle':
        triangle.doTrial()
        print('End of Trial')
    elif msg == 'square':
        square.doTrial()
        print('End of Trial')
    elif msg == 'h_letter':
        h_letter.doTrial()
        print('End of Trial')
    elif msg == 'v_letter':
        v_letter.doTrial()
        print('End of Trial')
    elif msg == 'star':
        star.doTrial()
        print('End of Trial')
    elif msg == 't_letter':
        t_letter.doTrial()
        print('End of Trial')
    elif msg == 's_letter':
        s_letter.doTrial()
        print('End of Trial')
    elif msg == 'w_letter':
        w_letter.doTrial()
        print('End of Trial')
    elif msg == 'stop':
        break