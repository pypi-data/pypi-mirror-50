import math
def sin(x, n):
    """Function to calculate the sum of sine series
    
    Args:
         x(degrees):angle of sine in degrees
         n(int):number upto which the series should expand to calculate sum
    
    Returns:
        value of the sum of sine series
    """    
    sine=0
    for i in range (n):
        sign=(-1)**i
        pi=22/7
        y=x*(pi/180)
        sine=sine+((y**(2.0*i+1))/math.factorial(2*i+1))*sign
    return sine
x = int(input("Enter the value of x in degrees:"))
n = int(input("Enter the number of terms:"))
#print(round(sin(x, n), 2))
s=round(sin(x, n), 2)
print (s)

#Unit tests to check soluion 
from tests import run_tests
run_tests(x, n, s)
    