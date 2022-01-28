function newSumImg = updatePreviewFigure(imHandle, data, newData, iterNumber)

newData = double(newData);
df = dRoR(newData, newData(:,:,1:10));

df = mean(df(:,:,16:35),3);
newSumImg = (data + df);
totalAverage = newSumImg / iterNumber;
totalAverage = imgaussfilt(totalAverage,2);
imHandle.CData = totalAverage;
caxis(imHandle.Parent, [min(totalAverage(:)),max(totalAverage(:))]); 


