clearvars, close all, clc

%% MAIN SETTINGS

% EXPERIMENT SETTINGS
% -------------------------------------------------------------------------
settings.stimuli = {'cross', 'triangle', 'circle', 'square', 'h_letter',...
                    'v_letter', 'star', 't_letter', 's_letter', 'w_letter'};
settings.repetitions = 10;
settings.preStim = 1;                           % in seconds
settings.durStim = 1;                           % in seconds
settings.postStim = 5;                            % in seconds

% Folder where to save the result of the experiments
settings.savingFolder = 'C:\Recordings\stimDecoding\gNex30\202220127\';

% TCP/IP SETTINGS
% -------------------------------------------------------------------------
settings.tcp.address = '192.168.1.3';
settings.tcp.port = 40000;

nFrames = 70;

%% Connect to the camera and initialize it
[vid, src] = loadCamera_PCOEdge();

%% Setup TCP/IP connection with the psychopy instance on localhost
stimList = pseudorandomSequence(settings.stimuli, settings.repetitions);

tcp = connectTCP_server(settings.tcp.address, settings.tcp.port);
fopen(tcp);

%% MAIN LOOP
h = src.H5HardwareROI_Height;
w = src.H2HardwareROI_Width;

sumImg_Triangle = zeros(h/2,w/2,'double');
sumImg_Circle = zeros(h/2,w/2,'double');
sumImg_Cross = zeros(h/2,w/2,'double');

pth = settings.savingFolder;
rawTriangle = zeros(h/2, w/2, nFrames, settings.repetitions,'uint16');
rawCircle = zeros(h/2, w/2, nFrames, settings.repetitions,'uint16');
rawCross = zeros(h/2, w/2, nFrames, settings.repetitions,'uint16');
rawSquare = zeros(h/2, w/2, nFrames, settings.repetitions,'uint16');
rawLetter_H = zeros(h/2, w/2, nFrames, settings.repetitions,'uint16');
rawLetter_V = zeros(h/2, w/2, nFrames, settings.repetitions,'uint16');
rawLetter_T = zeros(h/2, w/2, nFrames, settings.repetitions,'uint16');
rawLetter_S = zeros(h/2, w/2, nFrames, settings.repetitions,'uint16');
rawLetter_W = zeros(h/2, w/2, nFrames, settings.repetitions,'uint16');
rawStar = zeros(h/2, w/2, nFrames, settings.repetitions,'uint16');



m = matfile([pth filesep 'rec_' datestr(now, 'YYYYmmDD-hhMMss') '.mat'],...
    'Writable',true);
m.rawTriangle = rawTriangle;
m.rawCircle = rawCircle;
m.rawCross = rawCross;
m.rawSquare = rawSquare;
m.rawLetter_H = rawLetter_H;
m.rawLetter_V = rawLetter_V;
m.rawLetter_T = rawLetter_T;
m.rawLetter_S = rawLetter_S;
m.rawLetter_W = rawLetter_W;
m.rawStar = rawStar;

m.settings = settings;

clear rawTriangle rawCircle rawCross rawSquare rawLetter_H rawLetter_V rawLetter_T rawLetter_S rawLetter_W
crossN = 1;
triangleN = 1;
circleN = 1;
squareN = 1;
h_N = 1;
t_N = 1;
w_N = 1;
s_N = 1;
v_N = 1;
star_N = 1;



for i = 1:length(stimList)
    tic
    fprintf('Trial (%s) [%u/%u]...', stimList{i}, i, length(stimList))
    start(vid)
    fprintf('start, ')
    trigger(vid)
    fprintf('soft Trig, ')
    pause(0.25)
    % Send current trial to python that whil trigget the camera
    fwrite(tcp, stimList{i});
    % Wait for the acquisition to finish
    wait(vid)
    fprintf(' done [%.2f].\nProcessing...',toc)
    
    tic
    % Preprocess data, save it and display preview
    [data,time] = getdata(vid, nFrames);
    fprintf(' got data. [%.2f]', toc)
    tic
    if i == 1
        [f, im_T, im_C, im_X] = createPreviewFigure([h, w]);
    end
    
    data = imresize(squeeze(data),0.5);
    fprintf(' resized. ')
    switch stimList{i}
        case 'triangle'
            saveRawData(m, data, 'triangle', triangleN)
            sumImg_Triangle = updatePreviewFigure(im_T, sumImg_Triangle, data, triangleN);
            triangleN = triangleN + 1;
        case 'cross'
            saveRawData(m, data, 'cross', crossN)
            sumImg_Cross = updatePreviewFigure(im_X, sumImg_Cross, data, crossN);
            crossN = crossN + 1;
        case 'circle'
            saveRawData(m, data, 'circle', circleN)
            sumImg_Circle = updatePreviewFigure(im_C, sumImg_Circle, data, circleN);
            circleN = circleN + 1;
        case 'square'
            saveRawData(m, data, 'square', circleN)
            squareN = squareN + 1;
        case 'h_letter'
            saveRawData(m, data, 'h_letter', circleN)
            h_N = h_N + 1;
        case 'v_letter'
            saveRawData(m, data, 'v_letter', circleN)
            v_N = v_N + 1;
        case 'star'
            saveRawData(m, data, 'star', circleN)
            star_N = star_N + 1;
        case 't_letter'
            saveRawData(m, data, 't_letter', circleN)
            t_N = t_N + 1;
        case 's_letter'
            saveRawData(m, data, 's_letter', circleN)
            s_N = s_N + 1;
        case 'w_letter'
            saveRawData(m, data, 'w_letter', circleN)
            w_N = w_N + 1;
           
    end
    fprintf('End trial. [%.2f sec]\n',toc)
end
fprintf('END OF RECORDING.\n')
fwrite(tcp, 'stop');
fclose(tcp);

%% cleanup

delete(vid);
fclose(tcp);
close all
clear all
clc







