import sys
import math

def calculateL(color):
    processedColor = []
    for channel in color:
        channel = channel / 255.0
        if channel <= 0.03928:
            channel = channel/12.92
        else:
            channel = math.pow(((channel+0.055)/1.055), 2.4)
        processedColor.append(channel)
    return 0.2126 * processedColor[0] + 0.7152 * processedColor[1] + 0.0722 * processedColor[2]

def calculateContrast(color_1, color_2):
    L1 = calculateL(color_1)
    L2 = calculateL(color_2)
    if L1 > L2:
        return (L1 + 0.05) / (L2 + 0.05)
    else:
        return (L2 + 0.05) / (L1 + 0.05)

print calculateContrast([0, 0, 0], [255, 255, 255])
print calculateContrast([0, 0, 0], [0, 0, 0])
print calculateContrast([0, 0, 255], [255, 255, 255])
print calculateContrast([58, 103, 167], [255, 255, 255])
print calculateContrast([141, 40, 112], [255, 0, 0])
print calculateContrast([141, 40, 112], [172, 80, 204])

# Large Text,  Level AA,  Contrast should > 3
# Large Text,  Level AAA, Contrast should > 4.5
# Normal Text, Level AA,  Contrast should > 4.5
# Normal Text, Level AAA, Contrast should > 7

# Validate with https://webaim.org/resources/contrastchecker/