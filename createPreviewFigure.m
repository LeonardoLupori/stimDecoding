function [handleList] = createPreviewFigure(imSize,selectedStimuli,time)
% [handleList] = createPreviewFigure(imSize)

f = figure('Position', [170,180,930,480],'MenuBar','none',...
    'Name','Preview', 'NumberTitle', 'off');

% Create a temporary blank image
dummyImg = zeros(imSize(1),imSize(2),'uint8');

% Settings for the subtightplot function
gap = [0.05 0.01];
h_margin = [.03 .04];
w_margin = [.01 .01];

% First Image
subtightplot(2,3,1,gap,h_margin,w_margin);
im_1 = imagesc(dummyImg);
axis off
axis image
title(['Avg ' selectedStimuli{1}], 'Interpreter', 'none')
colorbar

% Second Image
subtightplot(2,3,2,gap,h_margin,w_margin);
im_2 = imagesc(dummyImg);
axis off
axis image
title(['Avg ' selectedStimuli{2}], 'Interpreter', 'none')
colorbar

% Third Image
subtightplot(2,3,3,gap,h_margin,w_margin);
im_3 = imagesc(dummyImg);
axis off
axis image
colorbar
title(['Avg ' selectedStimuli{3}], 'Interpreter', 'none')

% Last Image
subtightplot(2,3,4,gap,h_margin,w_margin);
im_last = imagesc(dummyImg);
axis off
axis image
colorbar
title('Last Trial')

% Axes for the timelines
tl_ax = subtightplot(2,3,[5,6],[0.1, 0.12],[.1, .1],w_margin);
tl_ax.XLim = [time(1), time(end)];
tl_ax.XLabel.String = 'Time (s)';
tl_ax.YLabel.String = '\DeltaF/F';

title('Timelines')

handleList.figure = f;
handleList.img_1 = im_1;
handleList.img_2 = im_2;
handleList.img_3 = im_3;
handleList.img_last = im_last;
handleList.tl_ax = tl_ax;




