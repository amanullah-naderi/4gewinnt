##import RPi.GPIO as GPIO
from time import sleep, strftime
from datetime import datetime

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
import json
from gpiozero import Button
import requests
from time import sleep

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, width=32, height=8, block_orientation=-90)
device.contrast(2)
virtual = viewport(device, width=32, height=8)

diffi = 4

readyButton = Button(14)
difficultyButton = Button(18)

dict = {
  4: 'Leicht',
  5: 'Mittel',
  6: 'Schwer'
}

while True:
  try:
    if readyButton.is_pressed:
      difficulty = '{"difficulty": ' + dict.get(diffi) + '}'
      difficulty = json.loads(difficulty)
      result = requests.post(f"http://localhost:8090/ready", json=difficulty)
      print("JSON SEND")
      sleep(1)
    if difficultyButton.is_pressed:
      diffi += 1
      if diffi > 6:
        diffi = 4
      sleep(0.5)
    with canvas(virtual) as draw:
      text(draw, (0, 1), dict.get(diffi), fill="white", font=proportional(LCD_FONT))

  except KeyboardInterrupt:
    GPIO.cleanup()
