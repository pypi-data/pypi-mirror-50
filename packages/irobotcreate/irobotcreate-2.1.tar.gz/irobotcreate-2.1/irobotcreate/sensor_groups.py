from sensor_packets import *

class Group_0:
    ID = 0
    SIZE = 26 # 7-26
    def __init__(self):  
        self.bumpsAndWheelDrops         = BumpsAndWheelDrops()         #  7 1
        self.wall                       = Wall()                       #  8 1
        self.cliffLeft                  = CliffLeft()                  #  9 1
        self.cliffFrontLeft             = CliffFrontLeft()             # 10 1
        self.cliffFrontRight            = CliffFrontRight()            # 11 1
        self.cliffRight                 = CliffRight()                 # 12 1
        self.virtualWall                = VirtualWall()                # 13 1
        self.wheelOvercurrents          = WheelOvercurrents()          # 14 1
        self.dirtDetect                 = DirtDetect()                 # 15 1            
        #                                                              # 16 1 UNUSED
        self.infraredCharacterOmni      = InfraredCharacterOmni()      # 17 1
        self.buttons                    = Buttons()                    # 18 1
        self.distance                   = Distance()                   # 19 2
        self.angle                      = Angle()                      # 20 2
        self.chargingState              = ChargingState()              # 21 1
        self.batteryVoltage             = BatteryVoltage()             # 22 2
        self.batteryCurrent             = BatteryCurrent()             # 23 2
        self.batteryTemperature         = BatteryTemperature()         # 24 1
        self.batteryCharge              = BatteryCharge()              # 25 2
        self.batteryCapacity            = BatteryCapacity()            # 26 2        
    def decode(self,packet,ofs):
        self.bumpsAndWheelDrops.decode(packet,ofs);         ofs+=1
        self.wall.decode(packet,ofs);                       ofs+=1
        self.cliffLeft.decode(packet,ofs);                  ofs+=1
        self.cliffFrontLeft.decode(packet,ofs);             ofs+=1
        self.cliffFrontRight.decode(packet,ofs);            ofs+=1
        self.cliffRight.decode(packet,ofs);                 ofs+=1
        self.virtualWall.decode(packet,ofs);                ofs+=1
        self.wheelOvercurrents.decode(packet,ofs);          ofs+=1
        self.dirtDetect.decode(packet,ofs);                 ofs+=1           
        ofs+=1
        self.infraredCharacterOmni.decode(packet,ofs);      ofs+=1
        self.buttons.decode(packet,ofs);                    ofs+=1
        self.distance.decode(packet,ofs);                   ofs+=2
        self.angle.decode(packet,ofs);                      ofs+=2
        self.chargingState.decode(packet,ofs);              ofs+=1
        self.batteryVoltage.decode(packet,ofs);             ofs+=2
        self.batteryCurrent.decode(packet,ofs);             ofs+=2
        self.batteryTemperature.decode(packet,ofs);         ofs+=1
        self.batteryCharge.decode(packet,ofs);              ofs+=2
        self.batteryCapacity.decode(packet,ofs);            ofs+=2        
    def __repr__(self):
        return(
            self.bumpsAndWheelDrops.__repr__()         +'\n'+
            self.wall.__repr__()                       +'\n'+
            self.cliffLeft.__repr__()                  +'\n'+
            self.cliffFrontLeft.__repr__()             +'\n'+
            self.cliffFrontRight.__repr__()            +'\n'+
            self.cliffRight.__repr__()                 +'\n'+
            self.virtualWall.__repr__()                +'\n'+
            self.wheelOvercurrents.__repr__()          +'\n'+
            self.dirtDetect.__repr__()                 +'\n'+
            self.infraredCharacterOmni.__repr__()      +'\n'+
            self.buttons.__repr__()                    +'\n'+
            self.distance.__repr__()                   +'\n'+
            self.angle.__repr__()                      +'\n'+
            self.chargingState.__repr__()              +'\n'+
            self.batteryVoltage.__repr__()             +'\n'+
            self.batteryCurrent.__repr__()             +'\n'+
            self.batteryTemperature.__repr__()         +'\n'+
            self.batteryCharge.__repr__()              +'\n'+
            self.batteryCapacity.__repr__()            
            )   
        
class Group_1:
    ID = 1
    SIZE = 10 # 7-16
    def __init__(self):  
        self.bumpsAndWheelDrops         = BumpsAndWheelDrops()         #  7 1
        self.wall                       = Wall()                       #  8 1
        self.cliffLeft                  = CliffLeft()                  #  9 1
        self.cliffFrontLeft             = CliffFrontLeft()             # 10 1
        self.cliffFrontRight            = CliffFrontRight()            # 11 1
        self.cliffRight                 = CliffRight()                 # 12 1
        self.virtualWall                = VirtualWall()                # 13 1
        self.wheelOvercurrents          = WheelOvercurrents()          # 14 1
        self.dirtDetect                 = DirtDetect()                 # 15 1            
        #                                                              # 16 1 UNUSED        
    def decode(self,packet,ofs):
        self.bumpsAndWheelDrops.decode(packet,ofs);         ofs+=1
        self.wall.decode(packet,ofs);                       ofs+=1
        self.cliffLeft.decode(packet,ofs);                  ofs+=1
        self.cliffFrontLeft.decode(packet,ofs);             ofs+=1
        self.cliffFrontRight.decode(packet,ofs);            ofs+=1
        self.cliffRight.decode(packet,ofs);                 ofs+=1
        self.virtualWall.decode(packet,ofs);                ofs+=1
        self.wheelOvercurrents.decode(packet,ofs);          ofs+=1
        self.dirtDetect.decode(packet,ofs);                 ofs+=1           
        ofs+=1            
    def __repr__(self):
        return(
            self.bumpsAndWheelDrops.__repr__()         +'\n'+
            self.wall.__repr__()                       +'\n'+
            self.cliffLeft.__repr__()                  +'\n'+
            self.cliffFrontLeft.__repr__()             +'\n'+
            self.cliffFrontRight.__repr__()            +'\n'+
            self.cliffRight.__repr__()                 +'\n'+
            self.virtualWall.__repr__()                +'\n'+
            self.wheelOvercurrents.__repr__()          +'\n'+
            self.dirtDetect.__repr__()            
            )   
        
class Group_2:
    ID = 2
    SIZE = 6 # 17-20
    def __init__(self):
        self.infraredCharacterOmni      = InfraredCharacterOmni()      # 17 1
        self.buttons                    = Buttons()                    # 18 1
        self.distance                   = Distance()                   # 19 2
        self.angle                      = Angle()                      # 20 2        
    def decode(self,packet,ofs):
        self.infraredCharacterOmni.decode(packet,ofs);      ofs+=1
        self.buttons.decode(packet,ofs);                    ofs+=1
        self.distance.decode(packet,ofs);                   ofs+=2
        self.angle.decode(packet,ofs);                      ofs+=2        
    def __repr__(self):
        return(            
            self.infraredCharacterOmni.__repr__()      +'\n'+
            self.buttons.__repr__()                    +'\n'+
            self.distance.__repr__()                   +'\n'+
            self.angle.__repr__()            
            )   

class Group_3:
    ID = 3
    SIZE = 10    
    def __init__(self):        
        self.chargingState      = ChargingState()      # 21 1
        self.batteryVoltage     = BatteryVoltage()     # 22 2
        self.batteryCurrent     = BatteryCurrent()     # 23 2
        self.batteryTemperature = BatteryTemperature() # 24 1
        self.batteryCharge      = BatteryCharge()      # 25 2
        self.batteryCapacity    = BatteryCapacity()    # 26 2
    def decode(self,packet,ofs):
        self.chargingState.decode(packet,ofs);      ofs+=1
        self.batteryVoltage.decode(packet,ofs);     ofs+=2
        self.batteryCurrent.decode(packet,ofs);     ofs+=2
        self.batteryTemperature.decode(packet,ofs); ofs+=1
        self.batteryCharge.decode(packet,ofs);      ofs+=2
        self.batteryCapacity.decode(packet,ofs)
    def __repr__(self):
        return (self.chargingState.__repr__()      +'\n'+
                self.batteryVoltage.__repr__()     +'\n'+
                self.batteryCurrent.__repr__()     +'\n'+
                self.batteryTemperature.__repr__() +'\n'+
                self.batteryCharge.__repr__()      +'\n'+
                self.batteryCapacity.__repr__())        
        
class Group_4:
    ID = 4
    SIZE = 14 # 27-34
    def __init__(self):         
        self.wallSignal                 = WallSignal()                 # 27 2
        self.cliffLeftSignal            = CliffLeftSignal()            # 28 2
        self.cliffFrontLeftSignal       = CliffFrontLeftSignal()       # 29 2
        self.cliffFrontRightSignal      = CliffFrontRightSignal()      # 30 2
        self.cliffRightSignal           = CliffRightSignal()           # 31 2
        #                                                              # 32 2 UNUSED
        #                                                              # 33 1 UNUSED
        self.chargingSourcesAvailable   = ChargingSourcesAvailable()   # 34 1        
    def decode(self,packet,ofs):        
        self.wallSignal.decode(packet,ofs);                 ofs+=2
        self.cliffLeftSignal.decode(packet,ofs);            ofs+=2
        self.cliffFrontLeftSignal.decode(packet,ofs);       ofs+=2
        self.cliffFrontRightSignal.decode(packet,ofs);      ofs+=2
        self.cliffRightSignal.decode(packet,ofs);           ofs+=2
        ofs+=2
        ofs+=1        
    def __repr__(self):
        return(            
            self.wallSignal.__repr__()                 +'\n'+
            self.cliffLeftSignal.__repr__()            +'\n'+
            self.cliffFrontLeftSignal.__repr__()       +'\n'+
            self.cliffFrontRightSignal.__repr__()      +'\n'+
            self.cliffRightSignal.__repr__()            
            )   
        
class Group_5:
    ID = 5
    SIZE = 12 # 35-42
    def __init__(self):
        self.oIMode                     = OIMode()                     # 35 1
        self.songNumber                 = SongNumber()                 # 36 1
        self.songPlaying                = SongPlaying()                # 37 1
        self.numberStreamPackets        = NumberStreamPackets()        # 38 1
        self.requestedVelocity          = RequestedVelocity()          # 39 2
        self.requestedRadius            = RequestedRadius()            # 40 2
        self.requestedRightVelocity     = RequestedRightVelocity()     # 41 2
        self.requestedLeftVelocity      = RequestedLeftVelocity()      # 42 2
    def decode(self,packet,ofs):        
        self.oIMode.decode(packet,ofs);                     ofs+=1
        self.songNumber.decode(packet,ofs);                 ofs+=1
        self.songPlaying .decode(packet,ofs);               ofs+=1
        self.numberStreamPackets.decode(packet,ofs);        ofs+=1
        self.requestedVelocity.decode(packet,ofs);          ofs+=2
        self.requestedRadius.decode(packet,ofs);            ofs+=2
        self.requestedRightVelocity.decode(packet,ofs);     ofs+=2
        self.requestedLeftVelocity.decode(packet,ofs);      ofs+=2
    def __repr__(self):
        return(            
            self.oIMode.__repr__()                     +'\n'+
            self.songNumber.__repr__()                 +'\n'+
            self.songPlaying.__repr__()                +'\n'+
            self.numberStreamPackets.__repr__()        +'\n'+
            self.requestedVelocity.__repr__()          +'\n'+
            self.requestedRadius.__repr__()            +'\n'+
            self.requestedRightVelocity.__repr__()     +'\n'+
            self.requestedLeftVelocity.__repr__()
            )   
        
class Group_6:
    ID = 6
    SIZE = 52 # 7-42
    def __init__(self):  
        self.bumpsAndWheelDrops         = BumpsAndWheelDrops()         #  7 1
        self.wall                       = Wall()                       #  8 1
        self.cliffLeft                  = CliffLeft()                  #  9 1
        self.cliffFrontLeft             = CliffFrontLeft()             # 10 1
        self.cliffFrontRight            = CliffFrontRight()            # 11 1
        self.cliffRight                 = CliffRight()                 # 12 1
        self.virtualWall                = VirtualWall()                # 13 1
        self.wheelOvercurrents          = WheelOvercurrents()          # 14 1
        self.dirtDetect                 = DirtDetect()                 # 15 1            
        #                                                              # 16 1 UNUSED
        self.infraredCharacterOmni      = InfraredCharacterOmni()      # 17 1
        self.buttons                    = Buttons()                    # 18 1
        self.distance                   = Distance()                   # 19 2
        self.angle                      = Angle()                      # 20 2
        self.chargingState              = ChargingState()              # 21 1
        self.batteryVoltage             = BatteryVoltage()             # 22 2
        self.batteryCurrent             = BatteryCurrent()             # 23 2
        self.batteryTemperature         = BatteryTemperature()         # 24 1
        self.batteryCharge              = BatteryCharge()              # 25 2
        self.batteryCapacity            = BatteryCapacity()            # 26 2
        self.wallSignal                 = WallSignal()                 # 27 2
        self.cliffLeftSignal            = CliffLeftSignal()            # 28 2
        self.cliffFrontLeftSignal       = CliffFrontLeftSignal()       # 29 2
        self.cliffFrontRightSignal      = CliffFrontRightSignal()      # 30 2
        self.cliffRightSignal           = CliffRightSignal()           # 31 2
        #                                                              # 32 2 UNUSED
        #                                                              # 33 1 UNUSED
        self.chargingSourcesAvailable   = ChargingSourcesAvailable()   # 34 1
        self.oIMode                     = OIMode()                     # 35 1
        self.songNumber                 = SongNumber()                 # 36 1
        self.songPlaying                = SongPlaying()                # 37 1
        self.numberStreamPackets        = NumberStreamPackets()        # 38 1
        self.requestedVelocity          = RequestedVelocity()          # 39 2
        self.requestedRadius            = RequestedRadius()            # 40 2
        self.requestedRightVelocity     = RequestedRightVelocity()     # 41 2
        self.requestedLeftVelocity      = RequestedLeftVelocity()      # 42 2
    def decode(self,packet,ofs):
        self.bumpsAndWheelDrops.decode(packet,ofs);         ofs+=1
        self.wall.decode(packet,ofs);                       ofs+=1
        self.cliffLeft.decode(packet,ofs);                  ofs+=1
        self.cliffFrontLeft.decode(packet,ofs);             ofs+=1
        self.cliffFrontRight.decode(packet,ofs);            ofs+=1
        self.cliffRight.decode(packet,ofs);                 ofs+=1
        self.virtualWall.decode(packet,ofs);                ofs+=1
        self.wheelOvercurrents.decode(packet,ofs);          ofs+=1
        self.dirtDetect.decode(packet,ofs);                 ofs+=1           
        ofs+=1
        self.infraredCharacterOmni.decode(packet,ofs);      ofs+=1
        self.buttons.decode(packet,ofs);                    ofs+=1
        self.distance.decode(packet,ofs);                   ofs+=2
        self.angle.decode(packet,ofs);                      ofs+=2
        self.chargingState.decode(packet,ofs);              ofs+=1
        self.batteryVoltage.decode(packet,ofs);             ofs+=2
        self.batteryCurrent.decode(packet,ofs);             ofs+=2
        self.batteryTemperature.decode(packet,ofs);         ofs+=1
        self.batteryCharge.decode(packet,ofs);              ofs+=2
        self.batteryCapacity.decode(packet,ofs);            ofs+=2
        self.wallSignal.decode(packet,ofs);                 ofs+=2
        self.cliffLeftSignal.decode(packet,ofs);            ofs+=2
        self.cliffFrontLeftSignal.decode(packet,ofs);       ofs+=2
        self.cliffFrontRightSignal.decode(packet,ofs);      ofs+=2
        self.cliffRightSignal.decode(packet,ofs);           ofs+=2
        ofs+=2
        ofs+=1
        self.chargingSourcesAvailable.decode(packet,ofs);   ofs+=1
        self.oIMode.decode(packet,ofs);                     ofs+=1
        self.songNumber.decode(packet,ofs);                 ofs+=1
        self.songPlaying .decode(packet,ofs);               ofs+=1
        self.numberStreamPackets.decode(packet,ofs);        ofs+=1
        self.requestedVelocity.decode(packet,ofs);          ofs+=2
        self.requestedRadius.decode(packet,ofs);            ofs+=2
        self.requestedRightVelocity.decode(packet,ofs);     ofs+=2
        self.requestedLeftVelocity.decode(packet,ofs);      ofs+=2
    def __repr__(self):
        return(
            self.bumpsAndWheelDrops.__repr__()         +'\n'+
            self.wall.__repr__()                       +'\n'+
            self.cliffLeft.__repr__()                  +'\n'+
            self.cliffFrontLeft.__repr__()             +'\n'+
            self.cliffFrontRight.__repr__()            +'\n'+
            self.cliffRight.__repr__()                 +'\n'+
            self.virtualWall.__repr__()                +'\n'+
            self.wheelOvercurrents.__repr__()          +'\n'+
            self.dirtDetect.__repr__()                 +'\n'+
            self.infraredCharacterOmni.__repr__()      +'\n'+
            self.buttons.__repr__()                    +'\n'+
            self.distance.__repr__()                   +'\n'+
            self.angle.__repr__()                      +'\n'+
            self.chargingState.__repr__()              +'\n'+
            self.batteryVoltage.__repr__()             +'\n'+
            self.batteryCurrent.__repr__()             +'\n'+
            self.batteryTemperature.__repr__()         +'\n'+
            self.batteryCharge.__repr__()              +'\n'+
            self.batteryCapacity.__repr__()            +'\n'+
            self.wallSignal.__repr__()                 +'\n'+
            self.cliffLeftSignal.__repr__()            +'\n'+
            self.cliffFrontLeftSignal.__repr__()       +'\n'+
            self.cliffFrontRightSignal.__repr__()      +'\n'+
            self.cliffRightSignal.__repr__()           +'\n'+
            self.chargingSourcesAvailable.__repr__()   +'\n'+
            self.oIMode.__repr__()                     +'\n'+
            self.songNumber.__repr__()                 +'\n'+
            self.songPlaying.__repr__()                +'\n'+
            self.numberStreamPackets.__repr__()        +'\n'+
            self.requestedVelocity.__repr__()          +'\n'+
            self.requestedRadius.__repr__()            +'\n'+
            self.requestedRightVelocity.__repr__()     +'\n'+
            self.requestedLeftVelocity.__repr__()
            )   

class Group_100:
    ID = 100
    SIZE = 80           
    def __init__(self):  
        self.bumpsAndWheelDrops         = BumpsAndWheelDrops()         #  7 1
        self.wall                       = Wall()                       #  8 1
        self.cliffLeft                  = CliffLeft()                  #  9 1
        self.cliffFrontLeft             = CliffFrontLeft()             # 10 1
        self.cliffFrontRight            = CliffFrontRight()            # 11 1
        self.cliffRight                 = CliffRight()                 # 12 1
        self.virtualWall                = VirtualWall()                # 13 1
        self.wheelOvercurrents          = WheelOvercurrents()          # 14 1
        self.dirtDetect                 = DirtDetect()                 # 15 1            
        #                                                              # 16 1 UNUSED
        self.infraredCharacterOmni      = InfraredCharacterOmni()      # 17 1
        self.buttons                    = Buttons()                    # 18 1
        self.distance                   = Distance()                   # 19 2
        self.angle                      = Angle()                      # 20 2
        self.chargingState              = ChargingState()              # 21 1
        self.batteryVoltage             = BatteryVoltage()             # 22 2
        self.batteryCurrent             = BatteryCurrent()             # 23 2
        self.batteryTemperature         = BatteryTemperature()         # 24 1
        self.batteryCharge              = BatteryCharge()              # 25 2
        self.batteryCapacity            = BatteryCapacity()            # 26 2
        self.wallSignal                 = WallSignal()                 # 27 2
        self.cliffLeftSignal            = CliffLeftSignal()            # 28 2
        self.cliffFrontLeftSignal       = CliffFrontLeftSignal()       # 29 2
        self.cliffFrontRightSignal      = CliffFrontRightSignal()      # 30 2
        self.cliffRightSignal           = CliffRightSignal()           # 31 2
        #                                                              # 32 2 UNUSED
        #                                                              # 33 1 UNUSED
        self.chargingSourcesAvailable   = ChargingSourcesAvailable()   # 34 1
        self.oIMode                     = OIMode()                     # 35 1
        self.songNumber                 = SongNumber()                 # 36 1
        self.songPlaying                = SongPlaying()                # 37 1
        self.numberStreamPackets        = NumberStreamPackets()        # 38 1
        self.requestedVelocity          = RequestedVelocity()          # 39 2
        self.requestedRadius            = RequestedRadius()            # 40 2
        self.requestedRightVelocity     = RequestedRightVelocity()     # 41 2
        self.requestedLeftVelocity      = RequestedLeftVelocity()      # 42 2            
        self.leftEncoderCounts          = LeftEncoderCounts()          # 43 2
        self.rightEncoderCounts         = RightEncoderCounts()         # 44 2
        self.lightBumper                = LightBumper()                # 45 1
        self.lightBumpLeftSignal        = LightBumpLeftSignal()        # 46 2
        self.lightBumpFrontLeftSignal   = LightBumpFrontLeftSignal()   # 47 2
        self.lightBumpCenterLeftSignal  = LightBumpCenterLeftSignal()  # 48 2
        self.lightBumpCenterRightSignal = LightBumpCenterRightSignal() # 49 2
        self.lightBumpFrontRightSignal  = LightBumpFrontRightSignal()  # 50 2
        self.lightBumpRightSignal       = LightBumpRightSignal()       # 51 2
        self.infraredCharacterLeft      = InfraredCharacterLeft()      # 52 1
        self.infraredCharacterRight     = InfraredCharacterRight()     # 53 1
        self.leftMotorCurrent           = LeftMotorCurrent()           # 54 2
        self.rightMotorCurrent          = RightMotorCurrent()          # 55 2
        self.mainBrushMotorCurrent      = MainBrushMotorCurrent()      # 56 2
        self.sideBrushMotorCurrent      = SideBrushMotorCurrent()      # 57 2
        self.stasis                     = Stasis()                     # 58 1 
    def decode(self,packet,ofs):
        self.bumpsAndWheelDrops.decode(packet,ofs);         ofs+=1
        self.wall.decode(packet,ofs);                       ofs+=1
        self.cliffLeft.decode(packet,ofs);                  ofs+=1
        self.cliffFrontLeft.decode(packet,ofs);             ofs+=1
        self.cliffFrontRight.decode(packet,ofs);            ofs+=1
        self.cliffRight.decode(packet,ofs);                 ofs+=1
        self.virtualWall.decode(packet,ofs);                ofs+=1
        self.wheelOvercurrents.decode(packet,ofs);          ofs+=1
        self.dirtDetect.decode(packet,ofs);                 ofs+=1           
        ofs+=1
        self.infraredCharacterOmni.decode(packet,ofs);      ofs+=1
        self.buttons.decode(packet,ofs);                    ofs+=1
        self.distance.decode(packet,ofs);                   ofs+=2
        self.angle.decode(packet,ofs);                      ofs+=2
        self.chargingState.decode(packet,ofs);              ofs+=1
        self.batteryVoltage.decode(packet,ofs);             ofs+=2
        self.batteryCurrent.decode(packet,ofs);             ofs+=2
        self.batteryTemperature.decode(packet,ofs);         ofs+=1
        self.batteryCharge.decode(packet,ofs);              ofs+=2
        self.batteryCapacity.decode(packet,ofs);            ofs+=2
        self.wallSignal.decode(packet,ofs);                 ofs+=2
        self.cliffLeftSignal.decode(packet,ofs);            ofs+=2
        self.cliffFrontLeftSignal.decode(packet,ofs);       ofs+=2
        self.cliffFrontRightSignal.decode(packet,ofs);      ofs+=2
        self.cliffRightSignal.decode(packet,ofs);           ofs+=2
        ofs+=2
        ofs+=1
        self.chargingSourcesAvailable.decode(packet,ofs);   ofs+=1
        self.oIMode.decode(packet,ofs);                     ofs+=1
        self.songNumber.decode(packet,ofs);                 ofs+=1
        self.songPlaying .decode(packet,ofs);               ofs+=1
        self.numberStreamPackets.decode(packet,ofs);        ofs+=1
        self.requestedVelocity.decode(packet,ofs);          ofs+=2
        self.requestedRadius.decode(packet,ofs);            ofs+=2
        self.requestedRightVelocity.decode(packet,ofs);     ofs+=2
        self.requestedLeftVelocity.decode(packet,ofs);      ofs+=2            
        self.leftEncoderCounts.decode(packet,ofs);          ofs+=2
        self.rightEncoderCounts.decode(packet,ofs);         ofs+=2
        self.lightBumper.decode(packet,ofs);                ofs+=1
        self.lightBumpLeftSignal.decode(packet,ofs);        ofs+=2
        self.lightBumpFrontLeftSignal.decode(packet,ofs);   ofs+=2
        self.lightBumpCenterLeftSignal.decode(packet,ofs);  ofs+=2
        self.lightBumpCenterRightSignal.decode(packet,ofs); ofs+=2
        self.lightBumpFrontRightSignal.decode(packet,ofs);  ofs+=2
        self.lightBumpRightSignal.decode(packet,ofs);       ofs+=2
        self.infraredCharacterLeft.decode(packet,ofs);      ofs+=1
        self.infraredCharacterRight.decode(packet,ofs);     ofs+=1
        self.leftMotorCurrent.decode(packet,ofs);           ofs+=2
        self.rightMotorCurrent.decode(packet,ofs);          ofs+=2
        self.mainBrushMotorCurrent.decode(packet,ofs);      ofs+=2
        self.sideBrushMotorCurrent.decode(packet,ofs);      ofs+=2
        self.stasis.decode(packet,ofs);                     ofs+=1    
    def __repr__(self):
        return(
            self.bumpsAndWheelDrops.__repr__()         +'\n'+
            self.wall.__repr__()                       +'\n'+
            self.cliffLeft.__repr__()                  +'\n'+
            self.cliffFrontLeft.__repr__()             +'\n'+
            self.cliffFrontRight.__repr__()            +'\n'+
            self.cliffRight.__repr__()                 +'\n'+
            self.virtualWall.__repr__()                +'\n'+
            self.wheelOvercurrents.__repr__()          +'\n'+
            self.dirtDetect.__repr__()                 +'\n'+
            self.infraredCharacterOmni.__repr__()      +'\n'+
            self.buttons.__repr__()                    +'\n'+
            self.distance.__repr__()                   +'\n'+
            self.angle.__repr__()                      +'\n'+
            self.chargingState.__repr__()              +'\n'+
            self.batteryVoltage.__repr__()             +'\n'+
            self.batteryCurrent.__repr__()             +'\n'+
            self.batteryTemperature.__repr__()         +'\n'+
            self.batteryCharge.__repr__()              +'\n'+
            self.batteryCapacity.__repr__()            +'\n'+
            self.wallSignal.__repr__()                 +'\n'+
            self.cliffLeftSignal.__repr__()            +'\n'+
            self.cliffFrontLeftSignal.__repr__()       +'\n'+
            self.cliffFrontRightSignal.__repr__()      +'\n'+
            self.cliffRightSignal.__repr__()           +'\n'+
            self.chargingSourcesAvailable.__repr__()   +'\n'+
            self.oIMode.__repr__()                     +'\n'+
            self.songNumber.__repr__()                 +'\n'+
            self.songPlaying.__repr__()                +'\n'+
            self.numberStreamPackets.__repr__()        +'\n'+
            self.requestedVelocity.__repr__()          +'\n'+
            self.requestedRadius.__repr__()            +'\n'+
            self.requestedRightVelocity.__repr__()     +'\n'+
            self.requestedLeftVelocity.__repr__()      +'\n'+           
            self.leftEncoderCounts.__repr__()          +'\n'+
            self.rightEncoderCounts.__repr__()         +'\n'+
            self.lightBumper.__repr__()                +'\n'+
            self.lightBumpLeftSignal.__repr__()        +'\n'+
            self.lightBumpFrontLeftSignal.__repr__()   +'\n'+
            self.lightBumpCenterLeftSignal.__repr__()  +'\n'+
            self.lightBumpCenterRightSignal.__repr__() +'\n'+
            self.lightBumpFrontRightSignal.__repr__()  +'\n'+
            self.lightBumpRightSignal.__repr__()       +'\n'+
            self.infraredCharacterLeft.__repr__()      +'\n'+
            self.infraredCharacterRight.__repr__()     +'\n'+
            self.leftMotorCurrent.__repr__()           +'\n'+
            self.rightMotorCurrent.__repr__()          +'\n'+
            self.mainBrushMotorCurrent.__repr__()      +'\n'+
            self.sideBrushMotorCurrent.__repr__()      +'\n'+
            self.stasis.__repr__()
            )                   
 
class Group_101:
    ID = 101
    SIZE = 28 # 43-58
    def __init__(self): 
        self.leftEncoderCounts          = LeftEncoderCounts()          # 43 2
        self.rightEncoderCounts         = RightEncoderCounts()         # 44 2
        self.lightBumper                = LightBumper()                # 45 1
        self.lightBumpLeftSignal        = LightBumpLeftSignal()        # 46 2
        self.lightBumpFrontLeftSignal   = LightBumpFrontLeftSignal()   # 47 2
        self.lightBumpCenterLeftSignal  = LightBumpCenterLeftSignal()  # 48 2
        self.lightBumpCenterRightSignal = LightBumpCenterRightSignal() # 49 2
        self.lightBumpFrontRightSignal  = LightBumpFrontRightSignal()  # 50 2
        self.lightBumpRightSignal       = LightBumpRightSignal()       # 51 2
        self.infraredCharacterLeft      = InfraredCharacterLeft()      # 52 1
        self.infraredCharacterRight     = InfraredCharacterRight()     # 53 1
        self.leftMotorCurrent           = LeftMotorCurrent()           # 54 2
        self.rightMotorCurrent          = RightMotorCurrent()          # 55 2
        self.mainBrushMotorCurrent      = MainBrushMotorCurrent()      # 56 2
        self.sideBrushMotorCurrent      = SideBrushMotorCurrent()      # 57 2
        self.stasis                     = Stasis()                     # 58 1 
    def decode(self,packet,ofs):
        self.leftEncoderCounts.decode(packet,ofs);          ofs+=2
        self.rightEncoderCounts.decode(packet,ofs);         ofs+=2
        self.lightBumper.decode(packet,ofs);                ofs+=1
        self.lightBumpLeftSignal.decode(packet,ofs);        ofs+=2
        self.lightBumpFrontLeftSignal.decode(packet,ofs);   ofs+=2
        self.lightBumpCenterLeftSignal.decode(packet,ofs);  ofs+=2
        self.lightBumpCenterRightSignal.decode(packet,ofs); ofs+=2
        self.lightBumpFrontRightSignal.decode(packet,ofs);  ofs+=2
        self.lightBumpRightSignal.decode(packet,ofs);       ofs+=2
        self.infraredCharacterLeft.decode(packet,ofs);      ofs+=1
        self.infraredCharacterRight.decode(packet,ofs);     ofs+=1
        self.leftMotorCurrent.decode(packet,ofs);           ofs+=2
        self.rightMotorCurrent.decode(packet,ofs);          ofs+=2
        self.mainBrushMotorCurrent.decode(packet,ofs);      ofs+=2
        self.sideBrushMotorCurrent.decode(packet,ofs);      ofs+=2
        self.stasis.decode(packet,ofs);                     ofs+=1    
    def __repr__(self):
        return(            
            self.leftEncoderCounts.__repr__()          +'\n'+
            self.rightEncoderCounts.__repr__()         +'\n'+
            self.lightBumper.__repr__()                +'\n'+
            self.lightBumpLeftSignal.__repr__()        +'\n'+
            self.lightBumpFrontLeftSignal.__repr__()   +'\n'+
            self.lightBumpCenterLeftSignal.__repr__()  +'\n'+
            self.lightBumpCenterRightSignal.__repr__() +'\n'+
            self.lightBumpFrontRightSignal.__repr__()  +'\n'+
            self.lightBumpRightSignal.__repr__()       +'\n'+
            self.infraredCharacterLeft.__repr__()      +'\n'+
            self.infraredCharacterRight.__repr__()     +'\n'+
            self.leftMotorCurrent.__repr__()           +'\n'+
            self.rightMotorCurrent.__repr__()          +'\n'+
            self.mainBrushMotorCurrent.__repr__()      +'\n'+
            self.sideBrushMotorCurrent.__repr__()      +'\n'+
            self.stasis.__repr__()
            )   
    
class Group_106:
    ID = 106
    SIZE = 12 # 46-51
    def __init__(self):  
        self.lightBumpLeftSignal        = LightBumpLeftSignal()        # 46 2
        self.lightBumpFrontLeftSignal   = LightBumpFrontLeftSignal()   # 47 2
        self.lightBumpCenterLeftSignal  = LightBumpCenterLeftSignal()  # 48 2
        self.lightBumpCenterRightSignal = LightBumpCenterRightSignal() # 49 2
        self.lightBumpFrontRightSignal  = LightBumpFrontRightSignal()  # 50 2
        self.lightBumpRightSignal       = LightBumpRightSignal()       # 51 2        
    def decode(self,packet,ofs):        
        self.lightBumpLeftSignal.decode(packet,ofs);        ofs+=2
        self.lightBumpFrontLeftSignal.decode(packet,ofs);   ofs+=2
        self.lightBumpCenterLeftSignal.decode(packet,ofs);  ofs+=2
        self.lightBumpCenterRightSignal.decode(packet,ofs); ofs+=2
        self.lightBumpFrontRightSignal.decode(packet,ofs);  ofs+=2
        self.lightBumpRightSignal.decode(packet,ofs);       ofs+=2        
    def __repr__(self):
        return(            
            self.lightBumpLeftSignal.__repr__()        +'\n'+
            self.lightBumpFrontLeftSignal.__repr__()   +'\n'+
            self.lightBumpCenterLeftSignal.__repr__()  +'\n'+
            self.lightBumpCenterRightSignal.__repr__() +'\n'+
            self.lightBumpFrontRightSignal.__repr__()  +'\n'+
            self.lightBumpRightSignal.__repr__()            
            )   
    
class Group_107:
    ID = 107
    SIZE = 9 # 54-58
    def __init__(self):
        self.leftMotorCurrent           = LeftMotorCurrent()           # 54 2
        self.rightMotorCurrent          = RightMotorCurrent()          # 55 2
        self.mainBrushMotorCurrent      = MainBrushMotorCurrent()      # 56 2
        self.sideBrushMotorCurrent      = SideBrushMotorCurrent()      # 57 2
        self.stasis                     = Stasis()                     # 58 1 
    def decode(self,packet,ofs):
        self.leftMotorCurrent.decode(packet,ofs);           ofs+=2
        self.rightMotorCurrent.decode(packet,ofs);          ofs+=2
        self.mainBrushMotorCurrent.decode(packet,ofs);      ofs+=2
        self.sideBrushMotorCurrent.decode(packet,ofs);      ofs+=2
        self.stasis.decode(packet,ofs);                     ofs+=1    
    def __repr__(self):
        return(            
            self.leftMotorCurrent.__repr__()           +'\n'+
            self.rightMotorCurrent.__repr__()          +'\n'+
            self.mainBrushMotorCurrent.__repr__()      +'\n'+
            self.sideBrushMotorCurrent.__repr__()      +'\n'+
            self.stasis.__repr__()
            )   