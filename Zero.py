#!/usr/bin/python3

# Zero Counter, for NES files
# Doug Fraker 2017

# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in the 
# Software without restriction, including without limitation the rights to use, copy, 
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the 
# following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF  
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import os



if len(sys.argv) < 2:
	print("usage: " + sys.argv[0] + " <path>")
	exit()
path = sys.argv[1]


# initialize some variables

bankSize = 8192 # default size
filesize = 0



# START OF PROGRAM

filename = os.path.basename(path)

try:
	fileIn = open(path, "rb") #read bytes
except:
	print("\nERROR: couldn't find file\n")
	raise
	
print (filename)
filesize = os.path.getsize(path)
print("filesize = ", filesize)
folder = os.path.dirname(path)
	
workArray = fileIn.read() #make a big int array 

testarray = bytearray(b'\x4e\x45\x53\x1a') # NES 1a



# validate header	

header = 16	
	
for i in range (0,4):
	if (workArray[i] != testarray[i]):
		header = 0

		
		
# bank sizes
		
b = 0
print("bank size = ?")

while (b == 0):
	b = input("1 = 8192, 2 = 16384, 4 = 32768:")
	if b == "1":
		bankSize = 8192
		Valid = 1
		break
	elif b == "2":
		bankSize = 16384
		Valid = 1
		break
	elif b == "4":
		bankSize = 32768
		Valid = 1
		break	
	else:
		b = 0		
		

	
if (filesize - header) < bankSize:
	print("  file size is smaller than bank size")
	bankSize = filesize - header
	print("  new bank size is "+str(bankSize))
	
if bankSize < 1:
	print("ERROR: something went wrong")
	exit()
	
number_banks = (filesize - header) / bankSize
number_banks = int(number_banks)
print("number_banks = "+str(number_banks))



# add up all the zeros in each bank

countZeros = 0
percent = 0
	
for i in range (1,number_banks+1):
	for j in range (0, bankSize):
		z = j + (bankSize * (i - 1)) + header
		if workArray[z] == 0:
			countZeros = countZeros + 1
		
	percent = 100 * countZeros / bankSize
	percent = round(percent, 2)
	print ("bank "+str(i)+" = "+str(percent)+"% empty. Or, "+str(countZeros)+" bytes of zero.")
	countZeros = 0
	percent = 0
	
	
# if file not exactly divisible by bankSize, because of a smaller bank at the end

if (number_banks * bankSize + header) < filesize:
	x = filesize - (number_banks * bankSize + header)
	y = filesize - x
	for i in range (y,filesize):
		if workArray[i] == 0:
			countZeros = countZeros + 1
	percent = 100 * countZeros / x
	percent = round(percent, 2)
	print ("smaller bank at end = "+str(percent)+"% empty. Or, "+str(countZeros)+" bytes of zero.")
		
	
fileIn.close	

