# distutils: language = c++
# cython: language_level = 3
#encoding = utf-8
DEF_CHIP_ID =   0x3C
DEF_MODEL_2RM = 0x0A
DEF_MODEL_4RT = 0x0B
DEF_MODEL_4NC = 0x0C
DEF_MODEL_4PC = 0x0D
DEF_MODEL_4NP = 0x0E
DEF_MODEL_4PP = 0x0F
#   Адреса регистров модулей
REG_FLAGS_0 =0x00
REG_BITS_0 = 0x01
REG_FLAGS_1 = 0x02
REG_BITS_1 = 0x03
REG_MODEL = 0x04
REG_VERSION = 0x05
REG_ADDRESS = 0x06
REG_CHIP_ID = 0x07
REG_FREQUENCY_L = 0x08
REG_FREQUENCY_H = 0x09
REG_AVERAGING   = 0x0A
REG_SHUNT = 0x0B
REG_FLG = 0x10
REG_BIT = 0x11
REG_DIGITAL_ALL = 0x12
REG_DIGITAL_ONE = 0x13
REG_PWM = 0x14
REG_ADC = 0x1C
REG_CURRENT = 0x24
REG_LIMIT = 0x2C
FLG_A_OFF = 0
FLG_A_MAX = 4
BIT_A_OFF = 0
BIT_A_MAX = 4
BIT_WRITE_L = 0
BIT_WRITE_H = 4
ALL_CHANNEL = 0xFF
CURRENT_LIMIT = 0xFF
CURRENT_DISABLE = 0x00
HIGH = 0x01
LOW = 0x00

from iarduino_I2C_Relay cimport iarduino_I2C_Relay
from iarduino_I2C_Relay cimport iarduino_I2C

cdef class pyiArduinoI2Crelay:
    cdef iarduino_I2C_Relay c_relay
    cdef iarduino_I2C b_relay

    def __cinit__(self, address=None):
        if address is not None:
            self.c_relay = iarduino_I2C_Relay(address)
            self.c_relay.begin()
        else:
            self.c_relay = iarduino_I2C_Relay()
            self.c_relay.begin()

    def begin(self):
        return self.c_relay.begin()

    def changeAddress(self, unsigned char newAddr):
        return self.c_relay.changeAddress(newAddr)

    def reset(self):
        return self.c_relay.reset()

    def getAddress(self):
        return self.c_relay.getAddress()

    def getVersion(self):
        return self.c_relay.getVersion()

    def getModel(self):
        return self.c_relay.getModel()

    def digitalWrite(self, unsigned char channel, unsigned char level):
        self.c_relay.digitalWrite(channel, level)

    def digitalRead(self, unsigned char channel):
        return self.c_relay.digitalRead(channel)
    
    def analogWrite(self, unsigned char channel, unsigned short level):
        self.c_relay.analogWrite(channel, level)

    def analogRead(self, unsigned char channel):
        return self.c_relay.analogRead(channel)

    def analogAveraging(self, unsigned char coefficient):
        self.c_relay.analogAveraging(coefficient)

    def freqPWM(self, unsigned short frequency):
        self.c_relay.freqPWM(frequency)

#   def currentWrite(self, unsigned char channel, float current):
#       self.c_relay.currentWrite(channel, current)

    def currentWrite(self, unsigned char channel, float current, Rsh=None):
        if Rsh is not None:
            self.c_relay.currentWrite(channel, current, Rsh)
        else:
            self.c_relay.currentWrite(channel, current)

    def currentRead(self,unsigned char channel):
        return self.c_relay.currentRead(channel)

    def setCurrentProtection(self, unsigned char channel, float current, unsigned char rtype):
        self.c_relay.setCurrentProtection(channel, current, rtype)

    def getCurrentProtection(self, unsigned char channel):
        return self.c_relay.getCurrentProtection(channel)

    def delCurrentProtection(self, unsigned char channel):
        self.c_relay.delCurrentProtection(channel)

    def resCurrentProtection(self, unsigned char channel):
        self.c_relay.resCurrentProtection(channel)

    def enableWDT(self, unsigned char time):
        return self.c_relay.enableWDT(time)

    def disableWDT(self):
        return self.c_relay.disableWDT()

    def resetWDT(self):
        return self.c_relay.resetWDT()

    def getStateWDT(self):
        return self.c_relay.getStateWDT()

    def changeBus(self, unsigned char bus):
        self.b_relay.changeBus(bus)
