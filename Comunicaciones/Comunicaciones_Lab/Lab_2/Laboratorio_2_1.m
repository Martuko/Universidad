clc;
clear;
close all;

f0 = 1000;
alphas = [0, 0.25, 0.75, 1];
t = linspace(0, 5/f0, 1000);
f = linspace(-2*f0*2, 2*f0*2, 2000);


colors = ['r', 'g', 'b', 'm']; 


figure('Name','Todas las Respuestas en Frecuencia');
hold on;
for i = 1:length(alphas)
    alpha = alphas(i);
    fDelta = alpha * f0;
    B = f0 * (1 + alpha);
    f1 = f0 * (1 - alpha);

    He = zeros(size(f));
    for j = 1:length(f)
        fj = abs(f(j));
        if fj < f1
            He(j) = 1;
        elseif fj < B
            He(j) = 0.5 * (1 + cos(pi * (fj - f1) / (2*fDelta)));
        else
            He(j) = 0;
        end
    end

    plot(f, He, 'Color', colors(i), 'LineWidth', 1.5);
end
title('Respuesta en Frecuencia para distintos \alpha');
xlabel('Frecuencia [Hz]');
ylabel('Magnitud');
grid on;
ylim([0 1.2]);
legend('\alpha = 0', '\alpha = 0.25', '\alpha = 0.75', '\alpha = 1');
hold off;

% Crear figura para Respuesta al Impulso
figure('Name','Todas las Respuestas al Impulso');
hold on;
for i = 1:length(alphas)
    alpha = alphas(i);
    fDelta = alpha * f0;

    sinc_part = sinc(2*f0*t);
    cos_part = cos(2*pi*fDelta*t);
    denom_part = 1 - (4*fDelta*t).^2;
    denom_part(abs(denom_part) < 1e-6) = 1e-6;

    h_t = 2*f0 * sinc_part .* (cos_part ./ denom_part);

    plot(t, h_t, 'Color', colors(i), 'LineWidth', 1.5);
end
title('Respuesta al Impulso para distintos \alpha');
xlabel('Tiempo [s]');
ylabel('Amplitud');
grid on;
legend('\alpha = 0', '\alpha = 0.25', '\alpha = 0.75', '\alpha = 1');
hold off;

% Referencias:
% [1] https://es.mathworks.com/help/comm/ug/raised-cosine-filtering.html
% [2] https://en.wikipedia.org/wiki/Raised-cosine_filter
