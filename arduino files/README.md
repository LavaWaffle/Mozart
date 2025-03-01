# Arduino files

This folder contains the Arduino sketch files for the project.

## Libraries

- LiquidCrystal.h
- VarSpeedServo.h

## Usage

1. Upload **mozart.ino** to the main Arduino board (the one with two servos and a LCD)
2. Upload **octave_controller.ino** to the secondary Arduino board (the one with a single servo)

## Circuit Diagram

![Circuit Diagram](https://github.com/LavaWaffle/Mozart/blob/main/arduino%20files/Circuit.png?raw=true)

- Note: Makeshift potentiometer is made via 10k resistor from 5v to a column, and a 1k resistor from the column to ground. That column is connected to the contrast pin of the LCD.

# Fun Fact

There is no need for two Arduino boards (pwm pin 6 is unused on the main board). However, the secondary Arduino board was good practice for uart communication.
