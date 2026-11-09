#%%
import pyvisa 

rm = pyvisa.ResourceManager()

rm.list_resources()
#%%

scope = rm.open_resource("USB0::0x0699::0x0374::C011064::INSTR")


#%%

answer = scope.query("*IDN?")

print(answer)
#%%