# SCRIPTING ASSIGNMENT

Write a Python script for a ‘fill’ functionality.

# 1. Input sample
Script reads ascii files like below: 

10 14 <br />
0 0 0 0 0 0 0 0 0 0 0 0 0 0 <br />
0 0 0 0 0 0 0 0 1 1 1 1 0 0 <br />
0 0 0 0 0 0 1 1 1 0 1 1 1 0 <br />
0 0 0 0 0 1 1 1 0 0 1 1 1 0 <br />
0 0 0 0 1 1 1 0 0 1 1 1 0 0 <br />
0 0 0 1 1 0 0 0 0 1 1 0 0 0 <br />
0 0 1 1 1 0 0 0 1 1 0 0 0 0 <br />
0 0 1 1 0 1 0 0 0 1 1 1 1 0 <br />
0 0 0 1 1 1 1 1 1 1 1 1 0 0 <br />
0 0 0 0 0 1 1 0 0 0 0 0 0 0 <br />

# 2. Output sample
Script outputs a filled version of the image data:

10 14 <br />
0 0 0 0 0 0 0 0 0 0 0 0 0 0 <br />
0 0 0 0 0 0 0 0 1 1 1 1 0 0 <br />
0 0 0 0 0 0 1 1 1 1 1 1 1 0 <br />
0 0 0 0 0 1 1 1 1 1 1 1 1 0 <br />
0 0 0 0 1 1 1 1 1 1 1 1 0 0 <br />
0 0 0 1 1 1 1 1 1 1 1 0 0 0 <br />
0 0 1 1 1 1 1 1 1 1 0 0 0 0 <br />
0 0 1 1 1 1 1 1 1 1 1 1 1 0 <br />
0 0 0 1 1 1 1 1 1 1 1 1 0 0 <br />
0 0 0 0 0 1 1 0 0 0 0 0 0 0 <br />
16

Where the last number is the amount of positions filled in.

# RESULTS
# 1. Original input:
![img.png](results/results_1_1.png)

![img.png](results/results_1_2.png)

# 2. Modified input 1:
![img.png](results/results_2_1.png)

![img.png](results/results_2_2.png)

# 3. Modified input 2:
![img.png](results/results_3_1.png)

![img.png](results/results_3_2.png)