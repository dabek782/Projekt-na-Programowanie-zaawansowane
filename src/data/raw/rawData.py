import ctypes
import mmap
import time
from pathlib import Path
import numpy as np
import pandas as pd


class File_physics(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ("packetId", ctypes.c_int),
        ("gas", ctypes.c_float),
        ("brake", ctypes.c_float),
        ("fuel", ctypes.c_float),
        ("gear", ctypes.c_int),
        ("rpms", ctypes.c_int),
        ("steerAngle", ctypes.c_float),
        ("speedKmh", ctypes.c_float),
        ("velocity", ctypes.c_float * 3),
        ("accG", ctypes.c_float * 3),
        ("wheelSlip", ctypes.c_float * 4),
        ("wheelLoad", ctypes.c_float * 4),
        ("wheelsPressure", ctypes.c_float * 4),
        ("wheelAngularSpeed", ctypes.c_float * 4),
        ("tyreWear", ctypes.c_float * 4),
        ("tyreDirtyLevel", ctypes.c_float * 4),
        ("tyreCoreTemperature", ctypes.c_float * 4),
        ("camberRAD", ctypes.c_float * 4),
        ("suspensionTravel", ctypes.c_float * 4),
        ("drs", ctypes.c_float),
        ("tc", ctypes.c_float),
        ("heading", ctypes.c_float),
        ("pitch", ctypes.c_float),
        ("roll", ctypes.c_float),
        ("cgHeight", ctypes.c_float),
        ("carDamage", ctypes.c_float * 5),
        ("numberOfTyresOut", ctypes.c_int),
        ("pitLimiterOn", ctypes.c_int),
        ("abs", ctypes.c_float),
    ]


class File_graphics(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ("packetId", ctypes.c_int),
        ("status", ctypes.c_int),
        ("session", ctypes.c_int),
        ("currentTime", ctypes.c_wchar * 15),
        ("lastTime", ctypes.c_wchar * 15),
        ("bestTime", ctypes.c_wchar * 15),
        ("split", ctypes.c_wchar * 15),
        ("completedLaps", ctypes.c_int),
        ("position", ctypes.c_int),
        ("iCurrentTime", ctypes.c_int),
        ("iLastTime", ctypes.c_int),
        ("iBestTime", ctypes.c_int),
        ("sessionTimeLeft", ctypes.c_float),
        ("distanceTraveled", ctypes.c_float),
        ("isInPit", ctypes.c_int),
        ("currentSectorIndex", ctypes.c_int),
        ("lastSectorTime", ctypes.c_int),
        ("numberOfLaps", ctypes.c_int),
        ("tyreCompound", ctypes.c_wchar * 33),
        ("replayTimeMultiplier", ctypes.c_float),
        ("normalizedCarPosition", ctypes.c_float),
        ("carCoordinates", ctypes.c_float * 3),
    ]


data_physics = mmap.mmap(-1, ctypes.sizeof(File_physics), r"Local\acpmf_physics")
data_graphics = mmap.mmap(-1, ctypes.sizeof(File_graphics), r"Local\acpmf_graphics")
PreviousPacketId = -1
track_data = []
completedLaps = 0
file_name = f"data_telemetry_{int(time.time())}.parquet"
try:
    print("Getting data")
    while True:

        FilephysicsData = File_physics.from_buffer_copy(data_physics)
        file_graphics_data = File_graphics.from_buffer_copy(data_graphics)
        if PreviousPacketId != FilephysicsData.packetId:
            if(file_graphics_data.status == 2 and file_graphics_data.isInPit == 0):
                track_data.append([FilephysicsData.packetId,FilephysicsData.gas , FilephysicsData.brake , FilephysicsData.steerAngle , FilephysicsData.speedKmh , FilephysicsData.gear , FilephysicsData.rpms , FilephysicsData.accG[0] , FilephysicsData.accG[1] , FilephysicsData.accG[2] , FilephysicsData.numberOfTyresOut , file_graphics_data.normalizedCarPosition ,  file_graphics_data.completedLaps ,  file_graphics_data.iCurrentTime ,  file_graphics_data.iLastTime ,  file_graphics_data.iBestTime ,  file_graphics_data.status ,  file_graphics_data.isInPit , file_graphics_data.carCoordinates[0] , file_graphics_data.carCoordinates[1] , file_graphics_data.carCoordinates[2]    ])
                PreviousPacketId = FilephysicsData.packetId
        time.sleep(1 / 60)
        if completedLaps != file_graphics_data.completedLaps:
            completedLaps = file_graphics_data.completedLaps
            folder = Path(__file__).parent
            df = pd.DataFrame(track_data , columns=["packetId" , "gas" , "brake" , "steerAngle" , "speedKmh" , "gear" , "rpms" , "accG_x" , "accG_y" , "accG_z" , "numberOfTyresOut" ,"normalizedCarPosition" , "completedLaps" , "iCurrentTime" , "iLastTime" , "iBestTime" , "status" , "isInPit" , "carCoordinates_x" , "carCoordinates_y", "carCoordinates_z" ])
            print(f"Zapisano{len(df)} wierszy")
            df.to_parquet(folder / file_name , index=False)
            print(f"zapisano okrążenie + completedLaps")

except KeyboardInterrupt:

        folder = Path(__file__).parent
        df = pd.DataFrame(track_data , columns=["packetId" , "gas" , "brake" , "steerAngle" , "speedKmh" , "gear" , "rpms" , "accG_x" , "accG_y" , "accG_z" , "numberOfTyresOut" ,"normalizedCarPosition" , "completedLaps" , "iCurrentTime" , "iLastTime" , "iBestTime" , "status" , "isInPit" , "carCoordinates_x" , "carCoordinates_y", "carCoordinates_z" ])
        print(f"Zapisano{len(df)} wierszy")
        df.to_parquet(folder / file_name , index=False)

