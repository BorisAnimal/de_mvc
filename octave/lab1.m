close all; clear all; clc; # To close 'widgets', delete variables and clean CLI
# graphics_toolkit('gnuplot') # For a better plotting

function ydot = f(y,x) 
  a = 7;
  b = 1;
  c = 98;
  ydot = -y + a*x^2 + b*x + c;
endfunction

function y = euler(y0, x) 
  y = [y0];
  step = x(2) - x(1);
  for i = 2:length(x)
    yi = y(i-1) + step * f(y(i-1), x(i-1));
    y = [y, yi];
  endfor
endfunction


function y = runge_kutt(y0,x)
  y = [y0];
  step = x(2) - x(1);
  for i = 2:length(x)
    k1 = f(y(i - 1), x(i - 1));
    k2 = f(y(i - 1) + step * k1 / 2, x(i - 1) + step / 2);
    k3 = f(y(i - 1) + step * k2 / 2, x(i - 1) + step / 2);
    k4 = f(y(i - 1) + step * k3, x(i - 1) + step);
    yi = y(i - 1) + step / 6 * (k1 + 2 * k2 + 2 * k3 + k4);
    y = [y, yi];  
  endfor
endfunction

function y = exact(y0, x)
  y = [y0];
  for i = 2:length(x)
    tmp = 7*x(i)**2 -13*x(i) + 111 - 110 * e()**(-x(i));
    y = [y, tmp];
  endfor
endfunction

function err = mean_error(y1, y2)
  s = 0;
  for i = 1:length(y1)
    s += abs(y1(i) - y2(i));
  endfor
  err = s / length(y1);
endfunction

function err = abs_error(y1, y2)
  err = [abs(y1(1) - y2(1))];
  for i = 2: length(y1)
    err = [err, abs(y1(i) - y2(i))];
  endfor
endfunction

function err = max_error(y1, y2)
  err = abs(y1(1) - y2(1));
  for i = 2:length(y1)
    tmp = abs(y1(i) - y2(i));
    if tmp > err
      err = tmp;
    endif
  endfor
endfunction

x0 = 0;
xn = 4;
steps = 100;

y0 = 1;

x = linspace(x0,xn, steps);
y = lsode("f", y0, x);
y_rk = runge_kutt(y0, x);
y_eu = euler(y0, x);
y_ex = exact(y0, x);
figure(1);
hold on;

# Plotting the results:
plot(x, y   , '-g;lsode solution;', 'linewidth', 2);
plot(x, y_rk, '-.r;Runge-Kutt method;', 'linewidth', 2);
plot(x, y_ex, '*o;Exact solution;', 'linewidth', 2);
plot(x, y_eu, '--b;Euler method;', 'linewidth', 2);
xlabel ("x");
ylabel ("y");
title ("Hello, Octave");

figure(2);
hold on;

# plot error distribution 
plot(x, abs_error(y, y_ex),  '-g;Abs error for Euler;', 'linewidth', 2);
title ("error of Euler method");

errors = [];
# Dependency of steps and max error
for i = 10:100
  x = linspace(x0,xn, i);
  y = exact(y0,x);
  y_eu = euler(y0,x);
  errors = [errors, max_error(y,y_eu)];
endfor

figure(3);
hold on;

plot(linspace(10,100,91),errors,'-g;max error;', 'linewidth', 2);
title ("Dependency of steps and max error");