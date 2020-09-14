import wavio
import numpy as np

# Import input signal
inFile = wavio.read('input.wav')
x = inFile.data         # Input signal
fs = inFile.rate        # Sample rate
sw = inFile.sampwidth   # Sample width
N = x.size              # Number of samples

# Compressor Design
Aa = 0.8661     # lambda_a
Ar = 0.9717     # lambda_r
p = 1/3         # rho
c0 = 1          # threshold
L = int(np.ceil((1 + Aa)/(1 - Aa))) # Length of FIR gain-smoothing filter
g = [0]*L       # Internal buffer for FIR gain-smoothing filter
q = 0           # Internal buffer index
c = 0           # Control signal
G = 0            #Smoothed gain
N = len(x)   # For limit on n

# Create empty list for output
y = np.array([])
for n in range(N):
    if abs(x[n]) >= c:
        c = Aa*c + (1 - Aa)*abs(x[n])
    else:
        c = Ar*c + (1 - Ar)*abs(x[n])

    if c == 0:
        g[q] = 1
    elif c >= c0:
        g[q] = (c/c0)**(p-1)
    else:
        g[q] = 1
    
    q = q + 1
    if q >= L:
        q = 1
    
    G = (1/L)*sum(g)                # FIR averaging filter
    y = np.append(y, G*x[n])        # Output

# Normalize results
y = y/y.max()
m = max(y)      # Maximum value of y
for i in range(len(y)):
    y[i] = y[i]/m

# Output results
wavio.write('output.wav', y, fs, sampwidth = sw)    