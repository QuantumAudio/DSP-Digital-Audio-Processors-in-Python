import wavio
import numpy as np

# Import input signal
inFile = wavio.read('original.wav')
s = inFile.data         # Input signal
fs = inFile.rate        # Sample rate
sw = inFile.sampwidth   # Sample width
N = s.size              # Number of samples
# Initial parameters
D1, D2 = int(0.25*fs), int(0.125*fs)
b0 = b1 = b2 = 1
a1, a2 = 0.2, 0.4
# Internal delay buffer 1 for s(n)
w = [0]*(D1 + D2 + 1)
# Delay buffer index variable
q = 0
# Delay buffer taps
tap1 = D1
tap2 = D1 + D2
# Empty list for output
y = np.array([])
# Loop through input signal
for n in range(N):
    s1 = w[tap1]
    s2 = w[tap2]
    y = np.append(y, b0*s[n] + b1*s1 + b2*s2)
    w[q] = s[n] + a1*s1 + a2*s2
    q -= 1              # Backshift index
    if q < 0:           # Circulate index
        q = D1 + D2
    tap1 -= 1           # Backshift tap1
    if tap1 < 0:        # Circulate tap1
        tap1 = D1 +D2
    tap2 -= 1
    if tap2 < 0:        # Backshift tap2
        tap2 = D1 + D2  # Circulate tap2

# Normalize results
y = y/y.max()
m = max(y)      # Maximum value of y
for i in range(len(y)):
    y[i] = y[i]/m

# Output results
wavio.write('output.wav', y, fs, sampwidth = sw)