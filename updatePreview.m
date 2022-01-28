function updatePreview(lastImage,avgImages,timelines,time,prevHandles)

avgImages = imgaussfilt(avgImages,2);
lastImage = imgaussfilt(lastImage,2);

prevHandles.img_1.CData = avgImages(:,:,1);
limits = [min(avgImages(:,:,1),[],'all'), max(avgImages(:,:,1),[],'all')];
caxis(prevHandles.img_1.Parent, limits);

prevHandles.img_2.CData = avgImages(:,:,2);
limits = [min(avgImages(:,:,2),[],'all'), max(avgImages(:,:,2),[],'all')];
caxis(prevHandles.img_2.Parent, limits);

prevHandles.img_3.CData = avgImages(:,:,3);
limits = [min(avgImages(:,:,3),[],'all'), max(avgImages(:,:,3),[],'all')];
caxis(prevHandles.img_3.Parent, limits);

prevHandles.img_last.CData = lastImage;
limits = [min(lastImage,[],'all'), max(lastImage,[],'all')];
caxis(prevHandles.img_last.Parent, limits);

plot(prevHandles.tl_ax, time, timelines,'Color',[1 .8 .8])
hold on
plot(prevHandles.tl_ax, time, mean(timelines),'Color',[.8,0,0], 'LineWidth', 2)
plot(prevHandles.tl_ax, time, timelines(end,:),'Color', [0 0 .8], 'LineWidth', 2)
xline(0,'color', 'k')
yline(0,'color', 'k')
hold off
