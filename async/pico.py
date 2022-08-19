from machine import SPI, Pin, freq
from vs1053 import *
import uasyncio as asyncio

xcs = Pin(14, Pin.OUT, value=1)  # Labelled CS on PCB, xcs on chip datasheet
reset = Pin(15, Pin.OUT, value=1)  # Active low hardware reset
xdcs = Pin(2, Pin.OUT, value=1)  # Data chip select xdcs in datasheet
dreq = Pin(3, Pin.IN)  # Active high data request
sdcs = Pin(5, Pin.OUT, value=1)  # SD card CS
spi = SPI(0, sck=Pin(6), mosi=Pin(7), miso=Pin(4))
player = VS1053(spi, reset, dreq, xdcs, xcs, sdcs, '/fc')

async def heartbeat():
    led = Pin(25, Pin.OUT)
    while(True):
        led(not(led()))
        await asyncio.sleep_ms(500)

async def main_01():  # Test cancellation
    player.volume(-10, -10)  # -10dB (0dB is loudest)
    locn = '/fc/192kbps/'
    asyncio.create_task(heartbeat())
    with open(locn + '01.mp3', 'rb') as f:
        task = asyncio.create_task(player.play(f))
        await asyncio.sleep(10)
        print('Cancelling playback')
        await player.cancel()
        print('Cancelled')
    with open(locn + '02.mp3', 'rb') as f:
        await player.play(f)
    print('All done.')

async def main():
    player.volume(-10, -10)  # -10dB (0dB is loudest)
    locn = '/fc/192kbps/'
    asyncio.create_task(heartbeat())
    with open(locn + '01.mp3', 'rb') as f:
        await player.play(f)
    # player.mode_set(SM_EARSPEAKER_LO | SM_EARSPEAKER_HI)  # You decide.
    # player.response(bass_freq=150, bass_amp=15)  # This is extreme.
    with open(locn + '02.mp3', 'rb') as f:
        await player.play(f)
    with open(locn + '03.mp3', 'rb') as f:
        await player.play(f)
    print('All done.')

asyncio.run(main())
