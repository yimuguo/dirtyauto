from __future__ import print_function
import visa
from i2c.aa_i2c import AAReadWrite
import time
import sys
import logging


sys.path.append('.')


class SweepTempVCO(object):
    def __init__(self):
        self.i2c_add = 0x68
        self.vdd = 5
        self.dut_i2c = AAReadWrite(0, self.i2c_add, True)
        self.power = visa.ResourceManager().open_resource('GPIB0::13::INSTR')
        self.fcounter = visa.ResourceManager().open_resource('GPIB0::3::INSTR')
        self.dut_i2c.length = 1
        self.power.write("APPL P6V,%d,0.3" % self.vdd)
        self.power.write("APPL P25V,3.3,0.2")
        self.chamber = visa.ResourceManager().open_resource('GPIB0::1::INSTR')

    def cal_vco(self, tempco=True):
        if tempco:
            self.dut_i2c.aa_write_i2c(40, [0])
            time.sleep(0.1)
        self.dut_i2c.aa_write_i2c(26, [0])
        time.sleep(0.05)
        self.dut_i2c.aa_write_i2c(26, [0x80])
        time.sleep(0.05)
        vco_band = list(self.dut_i2c.aa_read_i2c(47))
        time.sleep(0.05)
        return vco_band[0]

    def power_on(self, on=True):
        if on:
            self.power.write("OUTPUT:STATe ON;*OPC?")
            self.power.read()
            idd = self.power.query('MEASure:CURRent:DC? P6V')
            # time.sleep(0.01)
            return float(idd)
        else:
            self.power.write("OUTPUT:STATe OFF;*OPC?")
            self.power.read()

    def freq(self, channel=1):
        curr_freq = self.fcounter.query(':MEAS:FREQ? 100E+006,1, (@%d)' % channel)
        # time.sleep(0.05)
        return float(curr_freq)

    def set_temp(self, temp):
        self.chamber.write('TEMP, S' + str(temp))
        time.sleep(0.05)

    def read_temp(self):
        # self.chamber.write('TEMP?')
        # time.sleep(0.05)
        # read_val = self.chamber.read()
        # time.sleep(0.05)
        self.chamber.query("TEMP?")
        time.sleep(0.05)
        read_val = self.chamber.query("TEMP?")
        time.sleep(0.5)
        return float(read_val.split(',')[0])

    def close(self):
        self.dut_i2c.close()
        time.sleep(0.1)
        self.chamber.close()
        time.sleep(0.1)
        self.fcounter.close()
        time.sleep(0.1)
        self.power.close()
        time.sleep(0.1)


def main(start_temp, stop_temp, stepping, serial=0, tol_temp=0.2):
    ak692 = SweepTempVCO()
    logfile = open("log" + str(serial) + '_' + str(start_temp) + "_" + str(stop_temp) + ".txt", 'w+')
    time.sleep(0.1)
    ak692.power_on(False)
    # ak692.set_temp(start_temp)
    for temp in range(start_temp, stop_temp+stepping, stepping):
        curr_temp = ak692.read_temp()
        ak692.set_temp(temp)
        print("RAMP TEMP TO " + str(temp))
        while not((curr_temp < (temp + tol_temp)) and (curr_temp > (temp - tol_temp))):
            curr_temp = ak692.read_temp()
            print(".", end='')
            # print(curr_temp)
        if temp == start_temp:
            print("\nSOAK TIME 2MIN AT STARTING POINT...")
            time.sleep(120)
            idd = ak692.power_on()
            if idd < 0.1:
                raise EnvironmentError("IDD TOO SMALL PLEASE CHECK SETUP")
            time.sleep(0.05)
            band = list(ak692.dut_i2c.aa_read_i2c(47))[0]
            print("\nLOG: W/O TEMP CAL " + str(band))
            logfile.write("W/O TEMP CAL " + str(band) + '\n')
            cal_band = ak692.cal_vco()
            print("Calibrated with tempco: " + str(cal_band))
            ak692.cal_vco()
            time.sleep(0.05)
        frequency = ak692.freq()
        vco_band = list(ak692.dut_i2c.aa_read_i2c(47))[0]
        print('\nLOG: ' + str(temp) + '\t' + str(frequency) + '\t' + str(vco_band))
        logfile.write(str(temp) + '\t' + str(frequency) + '\t' + str(vco_band) + '\n')
        # if temp == start_temp:
        # ak692.set_temp(stop_temp)
    logfile.close()
    ak692.close()

if __name__ == '__main__':
    unitnum = sys.argv[1]
    print("STARTING TEMP.......... FROM 90C to -40C")
    main(90, -40, -10, unitnum)
    print("\nDone with first round, starting from -40C.....")
    time.sleep(30)
    main(-40, 90, 10, unitnum)
