import wavio
import numpy as np

# Import input signal
inFile = wavio.read('input.wav')
x = inFile.data         # Input signal
fs = inFile.rate        # Sample rate
sw = inFile.sampwidth   # Sample width
N = x.size              # Number of samples
# Initial parameters
D = int(0.003*fs)
F = 2/fs
a = 0.9
# Internal delay buffer for x[n]
w = [0]*(D + 1)
# Delay buffer index variable
q = 0
# Empty array for output
y = np.array([])
# Loop through input signal
for n in range(N):
    d = int(round((D/2)*(1 - np.cos(2*np.pi*F*n))))
    tap = q + d
    # Ensure tap is within range
    if tap < 0: 
        tap + tap + D
    elif tap > D:
        tap = tap - D
    y = np.append(y, x[n] + a*w[tap])
    w[q] = x[n]
    q -= 1
    # Ensure buffer index is within range
    if q < 0:
        q = q + D

# Normalize results
y = y/y.max()
m = max(y)      # Maximum value of y
for i in range(len(y)):
    y[i] = y[i]/m

# Output results
wavio.write('output.wav', y, fs, sampwidth = sw)
