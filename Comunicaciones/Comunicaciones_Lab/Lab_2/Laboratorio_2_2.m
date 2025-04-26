clear all;
close all;
clc;

N_bits = 1e3;
Rb = 1e3;
Fs = 10*Rb;
Ts = 1/Rb;
samples_per_symbol = Fs/Rb;

alpha_values = [0 0.25 0.75 1];

bits = randi([0 1], 1, N_bits);
symbols = 2*bits - 1;
upsampled = upsample(symbols, samples_per_symbol);
t = (0:length(upsampled)-1)/Fs;
SNR = 25;

for i = 1:length(alpha_values)
    alpha = alpha_values(i);
    span = 10;
    rrc_filter = rcosdesign(alpha, span, samples_per_symbol, 'normal');
    tx_signal = conv(upsampled, rrc_filter, 'same');
    rx_signal = awgn(tx_signal, SNR, 'measured');
    figure;
    eyediagram(rx_signal, 2*samples_per_symbol);
    title(['Diagrama de Ojo - \alpha = ', num2str(alpha)]);
end

% Referencias:
% [1] https://la.mathworks.com/help/comm/ref/eyediagram.html
% [2] https://www.youtube.com/watch?v=KJRpLMWb-7I