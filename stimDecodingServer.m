clearvars, close all, clc

%% MAIN SETTINGS

addpath(genpath('C:\Users\master\Documents\Python Scripts\stimDecoding'))

% EXPERIMENT SETTINGS
% -------------------------------------------------------------------------
settings.stimuli = {'cross', 'triangle', 'circle', 'square', 'h_letter',...
                    'v_letter', 'star', 't_letter', 's_letter', 'w_letter'};

settings.repetitions = 2;          %
settings.preStim = 1;               % in seconds
settings.durStim = 1;               % in seconds
settings.postStim = 5;              % in seconds

settings.exposureTime = 100;        % in milliseconds

% Folder where to save the result of the experiments
settings.savingFolder = 'F:\stimDecoding\test\';

% TCP/IP SETTINGS
% -------------------------------------------------------------------------
settings.tcp.address = '192.168.1.3';
settings.tcp.port = 40000;

% ADDITIONAL SETTINGS
% -------------------------------------------------------------------------
settings.framerate = 1/(settings.exposureTime/1000);
settings.nFrames = ceil((settings.preStim + settings.durStim + settings.postStim) * settings.framerate);

time = -settings.preStim:(settings.exposureTime/1000):(settings.postStim+settings.durStim) - (settings.exposureTime/1000);

%% Connect to the camera and initialize it
[vid, src] = loadCamera_PCOEdge(settings.repetitions * length(settings.stimuli),...
    settings.nFrames,...
    settings.exposureTime,...
    '04');

%% Setup TCP/IP connection with the psychopy instance on localhost

% Create a pseudorandom shuffled list of stimuli
stimList = pseudorandomSequence(settings.stimuli, settings.repetitions);

% Create a connection
tcp = connectTCP_server(settings.tcp.address, settings.tcp.port);

% Wait for connection from the paychopy client
fprintf('Waiting for connections...')
fopen(tcp);
fprintf('Connected!\n')

%% MAIN LOOP

h = src.H5HardwareROI_Height;
w = src.H2HardwareROI_Width;

for i = 1:length(settings.stimuli)
    rawData.(settings.stimuli{i}) = ...
        zeros(h/2, w/2, settings.nFrames, settings.repetitions,'uint16');
end

% Choose randomly 3 of the selected stimuli to plot the avg response
indexes = randperm(length(settings.stimuli),3);
selectedStims = settings.stimuli(indexes);

% Initialize the average images of the 3 selected stimuli and a matrix to
% contain the timelines of all the trials
sumImgs = zeros(h/2, w/2, 3, 'double');
avgImgs = zeros(h/2, w/2, 3, 'double');
timelines = zeros(settings.repetitions * length(settings.stimuli), settings.nFrames,'double');

% Create the output MATFILE
pth = settings.savingFolder;
fName = [pth filesep 'rec_' datestr(now, 'YYYYmmDD-hhMMss') '.mat'];
m = matfile(fName,'Writable',true);
m.settings = settings;
fprintf('Created the oputput matfile in:\n')
fprintf('\t%s\n', fName)

numPrestimFrames = round(settings.preStim*settings.framerate);
numStimFrames = round(settings.durStim*settings.framerate);

currentRepetition = 1;
start(vid)
for i = 1:length(stimList)    
    tic
    fprintf([repmat('-',1,40) '\n'])
    fprintf('Trial [%s] (%u/%u)...\n', stimList{i}, i, length(stimList))
    pause(0.1)
    
    % Send current trial to python that whil trigget the camera
    fwrite(tcp, stimList{i});
    fprintf('\tstimulus sent. Recording...\n')
        
    % Preprocess data, save it and display preview
    data = getdata(vid, settings.nFrames, 'native');
    fprintf('\tCaptured %u frames. [Elapsed Time: %.2f]\n', size(data,4), toc)
    
    % In the first iteration pops up the preview figure
    if i == 1
        prevHandles = createPreviewFigure([h, w], selectedStims, time);
    end
    
    % Downsample the images to half the resolution
    data = imresize(squeeze(data),0.5);
    fprintf('\tFrames resized. [Elapsed Time: %.2f]\n', toc)
    
    % Add the new Raw data to the struct
    rawData.(stimList{i})(:,:,:,currentRepetition) = data;
    
    
    % Update preview Image
    % ---------------------------------------------------------------------
    data = double(data);
    dFoF = dRoR(data,data(:,:,2:numPrestimFrames));
    
    % Update The sum Image
    lastImage = mean(dFoF(:,:,numPrestimFrames+1: numPrestimFrames+numStimFrames),3);
    [needToUpdate, idx] = ismember(stimList{i}, selectedStims);
    if needToUpdate
        sumImgs(:,:,idx) = sumImgs(:,:,idx) + lastImage;
        avgImgs(:,:,idx) = sumImgs(:,:,idx) / currentRepetition;
    end
    % Update the timelines matrix
    tl = timeline(dFoF);
    timelines(i,:) = tl;
    
    updatePreview(lastImage,avgImgs,timelines(1:i, :),time,prevHandles)      
    fprintf('\tEnd trial. [Elapsed Time: %.2f]\n',toc)
    
    % Updates the current repetition number when all the stimuli have ben
    % showed once
    if(mod(i,length(settings.stimuli))) == 0
        currentRepetition = currentRepetition + 1;
    end
end

fprintf([repmat('*',1,30), '\n'])
fprintf('Saving raw data...')
m.rawData = rawData;
fprintf('done.\n')
fprintf('END OF RECORDING.\n')
fprintf([repmat('*',1,30), '\n'])

fwrite(tcp, 'stop');
fclose(tcp);

%% cleanup

delete(vid);
fclose(tcp);
close all
clear all
clc







