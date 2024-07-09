from music21 import converter, note
import serial
import time


# Load the .mxl file
score = converter.parse('Twinkle Twinkle Little Star.mxl')

string = ""

# Iterate through all the notes in the score
for element in score.recurse().notes:
    if isinstance(element, note.Note):
        string += f"3,{element.name.lower()},{round(element.quarterLength*1000)}\n"  
        # print(element.name)
        print(f'Note: {element.nameWithOctave}, Duration: {element.quarterLength}, Offset: {element.offset}')
    elif isinstance(element, note.Rest):
        print(f'Rest, Duration: {element.quarterLength}, Offset: {element.offset}')

# print(string)
string += "|"
print("Finished reading file")
print("Sending data to Arduino")

ser = serial.Serial('COM3', 9600)
time.sleep(1)
ser.write(string.encode())
time.sleep(1)
ser.close()
print("Finished sending data")

