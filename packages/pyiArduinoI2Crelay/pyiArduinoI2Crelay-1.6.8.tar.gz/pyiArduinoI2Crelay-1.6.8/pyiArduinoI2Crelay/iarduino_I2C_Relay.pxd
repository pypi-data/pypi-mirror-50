cdef extern from "iarduino_I2C_Relay.cpp":
    pass

cdef extern from "iarduino_I2C_Relay.h":
    cdef cppclass iarduino_I2C_Relay:
        iarduino_I2C_Relay() except +
        iarduino_I2C_Relay(unsigned char) except +
        bint begin()
        bint changeAddress(unsigned char)
        bint reset()
        unsigned char getAddress()
        unsigned char getVersion()
        unsigned char getModel()
        void digitalWrite(unsigned char, unsigned char)
        unsigned char digitalRead(unsigned char)
        void analogWrite(unsigned char, unsigned short)
        unsigned short analogRead(unsigned char)
        void analogAveraging(unsigned char)
        void freqPWM(unsigned short)
        void currentWrite(unsigned char, float)
        void currentWrite(unsigned char, float, unsigned char&)
        float currentRead(unsigned char)
        void setCurrentProtection(unsigned char, float, unsigned char)
        bint getCurrentProtection(unsigned char)
        void delCurrentProtection(unsigned char)
        void resCurrentProtection(unsigned char) 
        bint enableWDT(unsigned char)
        bint disableWDT()
        bint resetWDT()
        bint getStateWDT()
cdef extern from "iarduino_I2C_Relay_PI.h":
    cdef cppclass iarduino_I2C:
        void changeBus(unsigned char)
