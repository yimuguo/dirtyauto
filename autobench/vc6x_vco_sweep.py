from __future__ import print_function
from sweep_temp_vco import SweepTempVCO
import time
import sys

sys.path.append('.')


def main(start_temp, stop_temp, stepping, serial=0, tol_temp=0.2):
    vc6x = SweepTempVCO()
    vc6x.i2c_add = 0x6a
    vc6x.vdd = 3.3
    logfile = open("log" + str(serial) + '_' + str(start_temp) + "_" + str(stop_temp) + ".txt", 'w+')
    time.sleep(0.1)
    vc6x.power_on(False)
    for temp in range(start_temp, stop_temp+stepping, stepping):
        curr_temp = vc6x.read_temp()
        vc6x.set_temp(temp)
        print("RAMP TEMP TO " + str(temp))
        while not((curr_temp < (temp + tol_temp)) and (curr_temp > (temp - tol_temp))):
            curr_temp = vc6x.read_temp()
            print(".", end='')
            # print(curr_temp)
        if temp == start_temp:
            print("\nSOAK TIME 2MIN AT STARTING POINT...")
            time.sleep(120)
            idd = vc6x.power_on()
            if idd < 0.1:
                raise EnvironmentError("IDD TOO SMALL PLEASE CHECK SETUP")
        frequency1 = (vc6x.freq(1))
        frequency2 = (vc6x.freq(2))
        vco_band = list(vc6x.dut_i2c.aa_read_i2c(0x99))[0]
        print('\nLOG: ' + str(temp) + '\t' + str(frequency1) + '\t' + str(frequency2) + '\t' + str(vco_band))
        logfile.write(str(temp) + '\t' + str(frequency1) + '\t' + str(frequency2) + '\t' + str(vco_band) + '\n')
        # if temp == start_temp:
        # ak692.set_temp(stop_temp)
    logfile.close()
    vc6x.close()

if __name__ == '__main__':
    unitnum = sys.argv[1]
    print("STARTING TEMP.......... FROM 90C to -40C")
    main(90, -40, -10, unitnum)
    print("\nDone with first round, starting from -40C.....")
    time.sleep(30)
    main(-40, 90, 10, unitnum)
