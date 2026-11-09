#%%
import pyvisa





class CrowScope:

    def __init__(self, address):

        self.rm = pyvisa.ResourceManager()
        self.address = address
        self.handshake() 
        identity = self.query("*IDN?")

        print("Connected to")
        print(identity)

    def __enter__(self):
        return self 

    def __exit__(self, exc_type, exc_val, exc_tb):
        return 

    def handshake(self):
        self.client = self.rm.open_resource(self.address)
        return self.client 

    def query(self, command):
        answer = self.client.query(command)

        return answer[:-1]


    #### in seconds
    def get_xscaling(self):
        command = "HORizontal:SCAle?"
        answer = self.query(command)

        return float(answer)

    # def set_xscaling(self, scaling_mv):

    #     command = "
    #     answer = self.query(command)
    #     return answer 


if __name__ == "__main__":
    with CrowScope("USB0::0x0699::0x0374::C011064::INSTR") as cs:
        import code; code.interact(local=locals())


#%%