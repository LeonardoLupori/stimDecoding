function t = timeline(movie)
% t = timeline(movie)
% Movie: 3D matrix where the tird dimension represents frames


reshaped = reshape(movie, [], size(movie,3));
t = mean(reshaped, 1);