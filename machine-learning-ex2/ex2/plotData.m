function plotData(X, y)
%PLOTDATA Plots the data points X and y into a new figure 
%   PLOTDATA(x,y) plots the data points with + for the positive examples
%   and o for the negative examples. X is assumed to be a Mx2 matrix.

% Create New Figure
figure; hold on;

% ====================== YOUR CODE HERE ======================
% Instructions: Plot the positive and negative examples on a
%               2D plot, using the option 'k+' for the positive
%               examples and 'ko' for the negative examples.
%
t = find(y==1);
f = find(y==0);
plot(X(t, 1), X(t, 2), 'k+', "markersize", 6, "LineWidth", 2);
plot(X(f, 1), X(f, 2), 'ko', "MarkerFaceColor", 'y', "markersize", 6);
% =========================================================================



hold off;

end
