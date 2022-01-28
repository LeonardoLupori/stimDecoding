function [vid, src] = loadCamera_PCOEdge(nTrigger,framesPerTrigger, expTime, binning)
% 
% [vid, src] = loadCamera_PCOEdge()
% [vid, src] = loadCamera_PCOEdge(nTrigger,framesPerTrigger, expTime, binning)
% 
% Function for initializing the PCO Edge 5.5 camera
% 
% INPUTS (all inputs are optional)
% nTrigger: Number of times the camera will be triggered (def: 1)
% framesPerTrigger: Number of frames the camera will acquire every trigger(def:20)
% expTime: Exposure time in ms (def:100)
% binning: Spatial binning ['01','02','04'] (def: 04')

arguments
    nTrigger (1,1) double {mustBePositive, mustBeInteger} = 1
    framesPerTrigger (1,1) double {mustBePositive, mustBeInteger} = 20
    expTime (1,1) {mustBeInRange(expTime,1,10000)} = 100
    binning (1,2) char {mustBeMember(binning,{'01','02','04'})} = '04'
end


% General settings for the PCO edge adaptor
% Tested in MATLAB 2020b
adaptor = 'pcocameraadaptor_r2020b';    % AdaptorName. See the folder camera_support for installing the adaptor
deviceID = 0;                           % In case there are multiple cameras
format = 'USB 3.0';                     % Acquisition format (1x1, 2x2,4x4 binning; various bit-depth)

% Load the camera
fprintf(['Loading up the camera: [' adaptor '] with format: [' format ']...'])
vid = videoinput(adaptor, deviceID , format);
src = getselectedsource(vid);

% Setup the Camera acquisition parameters
src.E1ExposureTime_unit = 'ms';
src.E2ExposureTime = expTime;

% Set thebinning property
src.B1BinningHorizontal = binning;
src.B2BinningVertical = binning;

% Number of frames to acquire
vid.FramesPerTrigger= framesPerTrigger;

% Number of times the camera will be triggered
vid.TriggerRepeat = nTrigger - 1;

% Settings for triggering the camera on the IO port 2 by using the
% "AcquireMode" "sequence_strigger".
% This allows to trigger series of frames and not each frame individually
% Resulting in faster acquisition
triggerconfig(vid, 'immediate');
src.AMAcquireMode = 'sequence_trigger';
src.AMImageNumber = framesPerTrigger;
src.IO_2SignalPolarity = 'low';

fprintf(' done\n')