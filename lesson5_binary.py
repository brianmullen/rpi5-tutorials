from gpiozero import LED
from time import sleep

bit1 = LED("BOARD37")
bit2 = LED("BOARD35")
bit4 = LED("BOARD33")
bit8 = LED("BOARD31")
bit16 = LED("BOARD29")

try:
    for i in range(0, 32, 1):
        isBit1 = bool(i & 0b00001)
        isBit2 = bool(i & 0b00010)
        isBit4 = bool(i & 0b00100)
        isBit8 = bool(i & 0b01000)
        isBit16 = bool(i & 0b10000)

        if isBit1:
            bit1.on()
        else:
            bit1.off()

        if isBit2:
            bit2.on()
        else:
            bit2.off()

        if isBit4:
            bit4.on()
        else:
            bit4.off()

        if isBit8:
            bit8.on()
        else:
            bit8.off()

        if isBit16:
            bit16.on()
        else:
            bit16.off()
        
        sleep(1)
except KeyboardInterrupt:
    print(' Interrupted')

bit1.close()
bit2.close()
bit4.close()
bit8.close()
bit16.close()
