# micropython on Raspberry Pi Pico
# asynchronous control of multiple PWM channels
# the program manages multiple processes
# the technique used is comparable to using millis() on an Arduino
from machine import Pin, PWM
from utime import sleep, ticks_us

# Modifiable PWM variables. 3 prepared here.
# Add as many as you like (16 max on raspberry pico)
numLeds = 3
ledPin = [15, 14, 13]
dutyDelay = [900, 1200, 500] # in microseconds. no effect under 500
minBright = 0
maxBright = 65500
rampStep = 100 # increase or decrease to change PWM ramp resolution (affects ramp speed)

# following variables not to be modified
led = []
ledDuty = [0] * numLeds
rampLedFlag = [True] * numLeds

# timing elements
currentTime = 0;
previousTime = [0] * numLeds

# Prepare led objects
for x in range(numLeds):
    led.append(PWM(Pin(ledPin[x])))
    led[x].freq(1000)

# loop forever
while True:
    for i in range(numLeds):
        currentTime = ticks_us()

        # reset previousTime variable if our timer returns to zero
        if currentTime < previousTime[0]:
            for x in range(numLeds):
                previousTime[x] = 0

        if (currentTime - previousTime[i]) >= dutyDelay[i]:
            previousTime[i] = currentTime

            if rampLedFlag[i] is True:
                ledDuty[i] += rampStep
                if ledDuty[i] is maxBright:
                    rampLedFlag[i] = False

            elif rampLedFlag[i] is False:
                ledDuty[i] -= rampStep
                if ledDuty[i] is minBright:
                    rampLedFlag[i] = True

            led[i].duty_u16(ledDuty[i])
