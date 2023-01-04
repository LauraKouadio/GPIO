<!-- docs/_quickstart.md -->

# Quickstart

## Step 1: Downloads

- Download STM32Cube IDE.
- Download Visual Studio Code (or any other code editor).
- Clone the GPIO repository.


## Step 2: Run the scripts

- Connect the board to the PC and launch STM32CubeIDE.
- You can connect LEDs to the I/Os if you want to see the pin's mode and value changes.
- Build and run the project in STM32CubeIDE.

- Run the python script Seriallink with the following commmand:


```python
python .\Seriallink.py
```
- While the Seriallink python script is running, enter one of the following command:

To turn the pin "pinNumber" of port "portLetter" into output push pull mode:

```bash
io.portLetter.pinNumber.dir=out
```

To turn the pin "pinNumber" of port "portLetter" into input analog mode:
```bash
io.portLetter.pinNumber.dir=in
```

To set the value of the pin "pinNumber" of port "portLetter" to HIGH. Please note that the value of a pin can be set to "HIGH" ONLY if the pin is already in output push pull mode:
```bash
io.portLetter.pinNumber.val=on
```

To set the value of the pin "pinNumber" of port "portLetter" to LOW. Please note that the value of a pin can be set to LOW ONLY if the pin is already in output push pull mode:
```bash
io.portLetter.pinNumber.val=off
```

To set the value of the pin "pinNumber" of port "portLetter" to LOW. Please note that the value of a pin can be set to LOW ONLY if the pin is already in output push pull mode:
```bash
io.portLetter.pinNumber.val=off
```

To print the value of the pin "pinNumber" of port "portLetter": 
```bash
io.portLetter.pinNumber.val?
```