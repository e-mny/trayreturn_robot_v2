import time

if ((mcp.read_adc(4) != 0) and (mcp.read_adc(5) != 0) and (mcp.read_adc(6) != 0) and (mcp.read_adc(7) != 0)):
	turnpattern(status)

def timer():
	time.sleep(timethreshold)
	return True

def status:
	if (weight.sensor > weightthreshold) or (timer()):
		
