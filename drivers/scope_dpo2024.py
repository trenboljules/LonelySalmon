#%%
import pyvisa
import matplotlib.pyplot as plt
import numpy as np

class CrowScope:

    def __init__(self, address):

        self.rm = pyvisa.ResourceManager()
        self.address = address
        self.handshake() 
        self.identity = self.query("*IDN?")

        print("Connected to")
        print(self.identity)

    def __enter__(self):
        return self 

    def __exit__(self, exc_type, exc_val, exc_tb):
        return 

    def handshake(self):
        self.client = self.rm.open_resource(self.address)
        self.client.timeout = 10000
        return self.client 

    def query(self, command):
        answer = self.client.query(command)
        return answer[:-1]

    def write(self, command):
        self.client.write(command)
        return self


#Y SCALING
##CH<x>:SCAle?
    #### in volts
    def get_yscaling(self, channel):

        command =f"CH{channel}:SCAle?"
        answer = self.query(command)
        return float(answer)

##CH<x>:SCAle <NR3>

    def set_yscaling(self, channel, scaling_volt):

        command = f"CH{channel}:SCAle {scaling_volt}"
        self.write(command)
        return self

#X SCALING
  #### in S
    def get_xscaling(self):
        command =f"HORizontal:SCAle?"
        answer = self.query(command)
        return float(answer)

#HORizontal:SCAle <NR3>
#1 2 4 
#cs.set_xscaling(2e-3) 

    def set_xscaling(self, scaling_time):
        number = [1e-3, 2e-3, 4e-3]
        if scaling_time in number: 
            command = f"HORizontal:SCAle {scaling_time}"
            self.write(command)
            return self
        else : 
             return print(f"Scaling_time must have the  value of {number}")


##Trigger 
#TRIGger:A:LEVel?
#In V
    def get_trigger_level(self):
        command =f"TRIGger:A:LEVel?"
        answer = self.query(command)    
        return float(answer)


#TRIGger:A:LEVel {ECL|TTL|<NR3>}   
#cs.set_trigger(5)

    def set_trigger_level(self, level):
        command = f"TRIGger:A:LEVel {level}"
        self.write(command)
        return self

#TRIGger:A:EDGE:SOUrce {{CH1}}

    def set_trigger_source(self, channel: int): 
        command = f"TRIGger:A:EDGE:SOUrce CH{channel}"
        self.write(command)
        return self

#TRIGger:A:EDGE:SOUrce?

    def get_trigger_source(self):
        command = f"TRIGger:A:EDGE:SOUrce?"
        answer = self.query(command)
        return str(answer)

#Slope edge 
#TRIGger:A:EDGE:SLOpe?


    def get_trigger_slope(self):
        command = "TRIGger:A:EDGE:SLOpe?"
        answer = self.query(command)
        if answer == "FALL":
            return False
        else: 
            return True

#TRIGger:A:EDGE:SLOpe {RISe|FALL}

    def set_trigger_slope(self, slope_bool):

        if slope_bool == True:
            slope = "RISE"
        elif slope_bool == False: 
            slope = "FALL"

        command = f"TRIGger:A:EDGE:SLOpe {slope}"
        self.write(command)
        return self




    def set_data_source(self, channel):
        command = f"DATa:SOUrce CH{channel}"
        answer = self.write(command)
        return self 
    
    def set_data_format(self, data_format):


        if data_format in ["ascii", "ASCII", "ASCii", "default", "DEFAULT", "Default", ]:
            format = "ascii"
        elif data_format in ["Binary", "BINARY", "binary", "Bi"]:
            format = "binary"
        
        command = f"DATa:ENCdg {format}"
        self.write(command)
        return self 

    def set_bytes_per_data(self, number_of_bytes: int):

        nbr  = [1, 2]
        if number_of_bytes in nbr: 
            input_num = number_of_bytes
        else : 
            return print("You'r number of byte per data must be 1 or 2")
        
        command = f"WFMOutpre:BIT_Nr {input_num}"
        answer = self.write(command)
        return self 


    def set_record_length(self, length: int): 
        command = f"WFMOutpre:RECOrdlength {length}"
        answer = self.write(command)
        return self

    def get_record_length(self): 
        command = "HORizontal:RECOrdlength?"
        answer = self.query(command)
        return int(answer)


    def set_data_start(self, data_start: int):
        command = f"DATa:STARt {data_start}"
        answer = self.write(command)
        return self

    def set_data_stop(self, data_stop: int):
        command = f"DATa:STOP {data_stop}"
        answer = self.write(command)
        return self

    def get_data_start(self):
        command = "DATa:STARt?"
        answer = self.query(command)
        return int(answer)

    def get_data_stop(self): 
        command = "DATa:STOP?"
        answer = self.query(command)
        return int(answer)


    def set_wave_form(self, format = "ASCII"):
        command = f"CURVE {format}"
        answer = self.write(command)
        return 

    def get_wave_form(self):
        command = "CURVe?"
        answer = self.query(command)
        return answer 

    def get_opc(self):
        command = "*OPC?"
        answer = self.query(command)
        return int(answer) 

    def set_data_resolution(self, full_res: bool):

        if not isinstance(full_res, bool):
            print("Invalid input for data res")
            return self 

        if full_res:
            command = "DATA:RESOLUTION FULL"
        else:
            command = "DATA:RESOLUTION REDUCED"
        self.write(command)
        return self

    def convert_adc2volts(self, raw_adc):
        ymult = float(self.query("WFMOutpre:YMUlt?"))
        yoff = float(self.query("WFMOutpre:YOFf?"))
        yzero = float(self.query("WFMOutpre:YZEro?"))

        voltage = (raw_adc - yoff) * ymult + yzero

        return voltage


    def get_channel_data(self, channel, data_format, number_of_bytes: int):

        self.set_wave_form("ASCII")
        self.set_data_resolution(True)

        self.set_data_source(channel)  
        self.set_data_format(data_format)
        self.set_bytes_per_data(number_of_bytes)
        record_length = self.get_record_length()

        self.set_data_start(1)
        self.set_data_stop(record_length)

        while self.get_opc() != 1:
            print("Waiting for scope...")

        wave_form = self.get_wave_form()

        adc_data = np.fromstring(wave_form, dtype=int, sep=',')
        voltage = self.convert_adc2volts(adc_data)

        print("Actual received points:", len(voltage))

        plt.plot(voltage)
        plt.show()

        return voltage
      


if __name__ == "__main__":
    with CrowScope("USB0::0x0699::0x0374::C011064::INSTR") as cs:
        import code; code.interact(local=locals())







#%%

