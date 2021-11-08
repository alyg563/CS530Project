# CS 530- Fall Detection Program
# Authors:
# Shane Tasker, Alyssa Garcia, Sawyer Thompson, Alexander Ray


# Code Source: https://www.waveshare.com/wiki/Sense_HAT_(B)#Raspberry_Pi_examples

# !/usr/bin/python
# -*- coding:utf-8 -*-
# Import Statements
import smbus
import math
import time

Accel = [0, 0, 0]
pu8data = [0, 0, 0, 0, 0, 0, 0, 0]
U8tempX = [0, 0, 0, 0, 0, 0, 0, 0, 0]
U8tempY = [0, 0, 0, 0, 0, 0, 0, 0, 0]
U8tempZ = [0, 0, 0, 0, 0, 0, 0, 0, 0]
Ki = 1.0
Kp = 4.50
q0 = 1.0
q1 = q2 = q3 = 0.0
true = 0x01
false = 0x00
# define ICM-20948 Device I2C address
I2C_ADD_ICM20948 = 0x68
I2C_ADD_ICM20948_AK09916 = 0x0C
I2C_ADD_ICM20948_AK09916_READ = 0x80
I2C_ADD_ICM20948_AK09916_WRITE = 0x00
# define ICM-20948 Register
# user bank 0 register
REG_ADD_WIA = 0x00
REG_VAL_WIA = 0xEA
REG_ADD_USER_CTRL = 0x03
REG_VAL_BIT_I2C_MST_EN = 0x20
REG_ADD_PWR_MIGMT_1 = 0x06
REG_VAL_ALL_RGE_RESET = 0x80
REG_VAL_RUN_MODE = 0x01  # Non low-power mode
REG_ADD_ACCEL_XOUT_H = 0x2D
REG_ADD_EXT_SENS_DATA_00 = 0x3B
REG_ADD_REG_BANK_SEL = 0x7F
REG_VAL_REG_BANK_0 = 0x00
REG_VAL_REG_BANK_2 = 0x20
REG_VAL_REG_BANK_3 = 0x30

# user bank 1 register
# user bank 2 register
REG_ADD_ACCEL_SMPLRT_DIV_2 = 0x11
REG_ADD_ACCEL_CONFIG = 0x14
REG_VAL_BIT_ACCEL_DLPCFG_6 = 0x30  # bit[5:3]
REG_VAL_BIT_ACCEL_FS_2g = 0x00  # bit[2:1]
REG_VAL_BIT_ACCEL_DLPF = 0x01  # bit[0]

# user bank 3 register
REG_ADD_I2C_SLV0_ADDR = 0x03
REG_ADD_I2C_SLV0_REG = 0x04
REG_ADD_I2C_SLV0_CTRL = 0x05
REG_VAL_BIT_SLV0_EN = 0x80
REG_VAL_BIT_MASK_LEN = 0x07
REG_ADD_I2C_SLV1_ADDR = 0x07
REG_ADD_I2C_SLV1_REG = 0x08
REG_ADD_I2C_SLV1_CTRL = 0x09
REG_ADD_I2C_SLV1_DO = 0x0A

# define ICM-20948 Register  end

# define ICM-20948 MAG Register

REG_ADD_MAG_CNTL2 = 0x31
REG_VAL_MAG_MODE_20HZ = 0x04
# define ICM-20948 MAG Register  end

class ICM20948(object):
    def __init__(self, address=I2C_ADD_ICM20948):
        self._address = address
        self._bus = smbus.SMBus(1)
        bRet = self.icm20948Check()  # Initialization of the device multiple times after power on will result in a return error
        time.sleep(0.5)  # We can skip this detection by delaying it by 500 milliseconds
        # user bank 0 register
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)
        self._write_byte(REG_ADD_PWR_MIGMT_1, REG_VAL_ALL_RGE_RESET)
        time.sleep(0.1)
        self._write_byte(REG_ADD_PWR_MIGMT_1, REG_VAL_RUN_MODE)
        # user bank 2 register
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_2)
        self._write_byte(REG_ADD_ACCEL_SMPLRT_DIV_2, 0x07)
        self._write_byte(REG_ADD_ACCEL_CONFIG,
                         REG_VAL_BIT_ACCEL_DLPCFG_6 | REG_VAL_BIT_ACCEL_FS_2g | REG_VAL_BIT_ACCEL_DLPF)
        # user bank 0 register
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)
        time.sleep(0.1)
        self.icm20948WriteSecondary(I2C_ADD_ICM20948_AK09916 | I2C_ADD_ICM20948_AK09916_WRITE, REG_ADD_MAG_CNTL2,
                                    REG_VAL_MAG_MODE_20HZ)

    def icm20948_Accel_Read(self):
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)
        data = self._read_block(REG_ADD_ACCEL_XOUT_H, 12)
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_2)
        Accel[0] = (data[0] << 8) | data[1]
        Accel[1] = (data[2] << 8) | data[3]
        Accel[2] = (data[4] << 8) | data[5]
        if Accel[0] >= 32767:  # Solve the problem that Python shift will not overflow
            Accel[0] = Accel[0] - 65535
        elif Accel[0] <= -32767:
            Accel[0] = Accel[0] + 65535
        if Accel[1] >= 32767:
            Accel[1] = Accel[1] - 65535
        elif Accel[1] <= -32767:
            Accel[1] = Accel[1] + 65535
        if Accel[2] >= 32767:
            Accel[2] = Accel[2] - 65535
        elif Accel[2] <= -32767:
            Accel[2] = Accel[2] + 65535

    def icm20948ReadSecondary(self, u8I2CAddr, u8RegAddr, u8Len):
        u8Temp = 0
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # swtich bank3
        self._write_byte(REG_ADD_I2C_SLV0_ADDR, u8I2CAddr)
        self._write_byte(REG_ADD_I2C_SLV0_REG, u8RegAddr)
        self._write_byte(REG_ADD_I2C_SLV0_CTRL, REG_VAL_BIT_SLV0_EN | u8Len)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # swtich bank0

        u8Temp = self._read_byte(REG_ADD_USER_CTRL)
        u8Temp |= REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)
        time.sleep(0.01)
        u8Temp &= ~REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)

        for i in range(0, u8Len):
            pu8data[i] = self._read_byte(REG_ADD_EXT_SENS_DATA_00 + i)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # swtich bank3

        u8Temp = self._read_byte(REG_ADD_I2C_SLV0_CTRL)
        u8Temp &= ~((REG_VAL_BIT_I2C_MST_EN) & (REG_VAL_BIT_MASK_LEN))
        self._write_byte(REG_ADD_I2C_SLV0_CTRL, u8Temp)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # swtich bank0

    def icm20948WriteSecondary(self, u8I2CAddr, u8RegAddr, u8data):
        u8Temp = 0
        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # swtich bank3
        self._write_byte(REG_ADD_I2C_SLV1_ADDR, u8I2CAddr)
        self._write_byte(REG_ADD_I2C_SLV1_REG, u8RegAddr)
        self._write_byte(REG_ADD_I2C_SLV1_DO, u8data)
        self._write_byte(REG_ADD_I2C_SLV1_CTRL, REG_VAL_BIT_SLV0_EN | 1)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # swtich bank0

        u8Temp = self._read_byte(REG_ADD_USER_CTRL)
        u8Temp |= REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)
        time.sleep(0.01)
        u8Temp &= ~REG_VAL_BIT_I2C_MST_EN
        self._write_byte(REG_ADD_USER_CTRL, u8Temp)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_3)  # swtich bank3

        u8Temp = self._read_byte(REG_ADD_I2C_SLV0_CTRL)
        u8Temp &= ~((REG_VAL_BIT_I2C_MST_EN) & (REG_VAL_BIT_MASK_LEN))
        self._write_byte(REG_ADD_I2C_SLV0_CTRL, u8Temp)

        self._write_byte(REG_ADD_REG_BANK_SEL, REG_VAL_REG_BANK_0)  # swtich bank0


    def _read_byte(self, cmd):
        return self._bus.read_byte_data(self._address, cmd)

    def _read_block(self, reg, length=1):
        return self._bus.read_i2c_block_data(self._address, reg, length)

    def _read_u16(self, cmd):
        LSB = self._bus.read_byte_data(self._address, cmd)
        MSB = self._bus.read_byte_data(self._address, cmd + 1)
        return (MSB << 8) + LSB

    def _write_byte(self, cmd, val):
        self._bus.write_byte_data(self._address, cmd, val)
        time.sleep(0.0001)

    def imuAHRSupdate(self, ax, ay, az):
        norm = 0.0
        vx = vy = vz = 0.0
        exInt = eyInt = ezInt = 0.0
        ex = ey = ez = 0.0
        halfT = 0.024
        global q0
        global q1
        global q2
        global q3
        q0q0 = q0 * q0
        q0q1 = q0 * q1
        q0q2 = q0 * q2
        q0q3 = q0 * q3
        q1q1 = q1 * q1
        q1q2 = q1 * q2
        q1q3 = q1 * q3
        q2q2 = q2 * q2
        q2q3 = q2 * q3
        q3q3 = q3 * q3

        norm = float(1 / math.sqrt(ax * ax + ay * ay + az * az))
        ax = ax * norm
        ay = ay * norm
        az = az * norm

        # estimated direction of gravity(v)
        vx = 2 * (q1q3 - q0q2)
        vy = 2 * (q0q1 + q2q3)
        vz = q0q0 - q1q1 - q2q2 + q3q3

        # error is sum of cross product between reference direction of fields and direction measured by sensors
        ex = (ay * vz - az * vy)
        ey = (az * vx - ax * vz)
        ez = (ax * vy - ay * vx)

        if (ex != 0.0 and ey != 0.0 and ez != 0.0):
            exInt = exInt + ex * Ki * halfT
            eyInt = eyInt + ey * Ki * halfT
            ezInt = ezInt + ez * Ki * halfT

        norm = float(1 / math.sqrt(q0 * q0 + q1 * q1 + q2 * q2 + q3 * q3))
        q0 = q0 * norm
        q1 = q1 * norm
        q2 = q2 * norm
        q3 = q3 * norm

    def icm20948Check(self):
        bRet = false
        if REG_VAL_WIA == self._read_byte(REG_ADD_WIA):
            bRet = true
        return bRet

    def icm20948CalAvgValue(self):
        MotionVal[0] = Accel[0]
        MotionVal[1] = Accel[1]
        MotionVal[2] = Accel[2]

    # Detect and return current acceleration
    def detectFall(self):
        detector.icm20948_Accel_Read()
        detector.icm20948CalAvgValue()
        time.sleep(0.1)
        detector.imuAHRSupdate(MotionVal[0], MotionVal[1], MotionVal[2])
        #Converts from LSB units to G's
        Accel[0] /= 16384.0
        Accel[1] /= 16384.0
        Accel[2] /= 16384.0

        print("\r\n /-------------------------------------------------------------/ \r\n")
        print('\r\nAcceleration:  X = %f , Y = %f , Z = %f\r\n' % (Accel[0], Accel[1], Accel[2]))
        return Accel[2]

# Make emergency call based on inputted contact info
def call(contactInfo):
    #make call to contactInfo number or send email to contactInfo email
    print("Called!")
    return

fallen = false
contactInfo = "" #Store user inputted contact info
MotionVal = [0.0, 0.0, 0.0]
detector = ICM20948()
FallThreshold = -1.5 # A fall is considered 1.5 Gs in the negative Z direction

#Main while loop that constantly queries the accelerometer for current velocity,
# and makes a call if it is determined that a person is falling
while not fallen:
    if detector.detectFall() <= FallThreshold: 
        print("Fallen!")
        call(contactInfo) # Make emergency call
        fallen = true # exit loop
        
