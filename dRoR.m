function res = dRoR(avgMovie,avgBase)
% res = dRoR(avgData,avgBase)
% 
% dRoR calculates the delta R over R of a set of data, based on a baseline
% 
% INPUT
% avgMovie: A 3D matrix containing the data that you want to calculate the
%           dR on R on.
% avgBase: a 3D matrix containing the data that you want to use as a
%           baseline
%
% OUTPUT
% res: deltaR over R of the data contained in avgMovie.
%
% see also ios_preprocessing


baseline = mean(avgBase,3);

res = bsxfun(@rdivide,bsxfun(@minus,avgMovie,baseline),baseline);
end

 