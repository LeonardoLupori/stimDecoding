function [vid, src] = loadCamera_PCOEdge()

settings.camera.adaptor = 'pcocameraadaptor_r2020b';      % AdaptorName. See the folder camera_support for installing the adaptor
settings.camera.deviceID = 0;                      % In case there are multiple cameras
settings.camera.format = 'USB 3.0';                % Acquisition format (1x1, 2x2,4x4 binning; various bit-depth)

% Get the videoinput object
fprintf(['Loading up the camera: [' settings.camera.adaptor '] with format: [' settings.camera.format ']...'])

vid = videoinput(settings.camera.adaptor, settings.camera.deviceID , settings.camera.format);
src = getselectedsource(vid);

% Setup the Camera acquisition parameters
src.E1ExposureTime_unit = 'ms';
src.E2ExposureTime = 100;

src.B1BinningHorizontal = '04';
src.B2BinningVertical = '04';

src.AMAcquireMode = 'sequence_trigger';
src.AMImageNumber = 70;
vid.FramesPerTrigger= 70;
src.IO_2SignalPolarity = 'low';

triggerconfig(vid, 'manual');
fprintf(' done\n')