import ctypes
import os
import mmap 
import time
class Filephysics(ctypes.Structure):
    _fields_ = [
        ("packetId" ,ctypes.c_int),
        ("gas" , ctypes.c_float),
        ("brake" , ctypes.c_float),
         ("fuel" , ctypes.c_float) , 
         ("gear" , ctypes.c_int) , 
         ("rpms" , ctypes.c_int) , 
         ("steerAngle" , ctypes.c_float) , 
         ("speedKmh" , ctypes.c_float)

    ]


data = mmap.mmap(-1 , 32 , r"Local\acpmf_physics")

PreviousPacketId = -1
while True:
    FilephysicsData = Filephysics.from_buffer_copy(data[0:32])
    if(PreviousPacketId != FilephysicsData.packetId ):
        print(FilephysicsData.speedKmh , FilephysicsData.gear , FilephysicsData.rpms , FilephysicsData.packetId)
        PreviousPacketId = FilephysicsData.packetId
    time.sleep(1/60)

