# TODO document how sensor groups work

def _signed_word_from_bytes(value,ofs):
        value = (value[ofs]<<8) | value[ofs+1]
        if value>32767:
            value = value - 65536
        return value
    
def _unsigned_word_from_bytes(value,ofs):
        value = (value[ofs]<<8) | value[ofs+1]        
        return value
    
class BumpsAndWheelDrops:    
    ID = 7
    SIZE = 1    
    def __init__(self):
        self.bump_right = None # bumper pushed in on right side
        self.bump_left  = None # bumper pushed in on left side
        self.drop_right = None # right wheel dropped
        self.drop_left  = None # left wheel dropped
    
    def decode(self,packet,ofs):
        # print(packet)
        self.bump_right = ((packet[ofs]&1)>0)        
        self.bump_left  = ((packet[ofs]&2)>0) 
        self.drop_right = ((packet[ofs]&4)>0) 
        self.drop_left  = ((packet[ofs]&8)>0)         
            
    def __repr__(self):
        return ('BumpsAndDrops bump_left:'+str(self.bump_left)+' bump_right:'+str(self.bump_right)+
                ' drop_left:'+str(self.drop_left)+' drop_right:'+str(self.drop_right))
        
class Wall:
    ID = 8
    SIZE = 1
    def __init__(self):
        self.is_wall = None # right side of bumper
    def decode(self,packet,ofs):
        self.is_wall = (packet[ofs]>0)
    def __repr__(self):
        return ('Wall is_wall:'+str(self.is_wall))
        
class CliffLeft:
    ID = 9
    SIZE = 1
    
    def __init__(self):
        self.is_cliff = None # TODO where?
        
    def decode(self,packet,ofs):
        #print(packet)
        self.is_cliff = (packet[ofs]>0)
    
    def __repr__(self):
        return ('CliffLeft is_cliff:'+str(self.is_cliff))
    
class CliffFrontLeft:
    ID = 10
    SIZE = 1
    
    def __init__(self):
        self.is_cliff = None # TODO where?
        
    def decode(self,packet,ofs):
        #print(packet)
        self.is_cliff = (packet[ofs]>0)
    
    def __repr__(self):
        return ('CliffFrontLeft is_cliff:'+str(self.is_cliff))
    
class CliffFrontRight:
    ID = 11
    SIZE = 1
    
    def __init__(self):
        self.is_cliff = None # TODO where?
        
    def decode(self,packet,ofs):
        #print(packet)
        self.is_cliff = (packet[ofs]>0)
    
    def __repr__(self):
        return ('CliffFrontRight is_cliff:'+str(self.is_cliff))
    
class CliffRight:
    ID = 12
    SIZE = 1
    
    def __init__(self):
        self.is_cliff = None # TODO where?
        
    def decode(self,packet,ofs):
        #print(packet)
        self.is_cliff = (packet[ofs]>0)
    
    def __repr__(self):
        return ('CliffRight is_cliff:'+str(self.is_cliff))

class VirtualWall:
    ID = 13
    SIZE = 1   
    def __init__(self):
        self.is_vwall = None
    def decode(self,packet,ofs):
        self.is_vwall = (packet[ofs]>0)
    def __repr__(self):
        return ('VirtualWall is_vwall:'+str(self.is_vwall))

class WheelOvercurrents:
    ID = 14
    SIZE = 1
    def __init__(self):
        self.is_left_wheel = None
        self.is_right_wheel = None
        self.is_main_brush = None        
        self.is_side_brush = None  
    def decode(self,packet,ofs):
        self.is_left_wheel =  ((packet[ofs]&16)>0)  
        self.is_right_wheel = ((packet[ofs]&8)>0) 
        self.is_main_brush =  ((packet[ofs]&4)>0) 
        self.is_side_brush =  ((packet[ofs]&1)>0)   
    def __repr__(self):
        return ('WheelOvercurrents is_left_wheel:'+str(self.is_left_wheel)+" is_right_wheel:"+str(self.is_right_wheel)+
                ' is_main_brush:'+str(self.is_main_brush)+' is_side_brush:'+str(self.is_side_brush))
    
class DirtDetect:
    ID = 15
    SIZE = 1
    def __init__(self):
        self.dirt = None
    def decode(self,packet,ofs):
        self.dirt = packet[ofs]
    def __repr__(self):
        return 'DirtDetect dirt:'+str(self.dirt)
    
class InfraredCharacterOmni:
    ID = 17
    SIZE = 1
    def __init__(self):
        self.character = None
    def decode(self,packet,ofs):
        self.character = packet[ofs]
    def __repr__(self):
        return 'InfraredCharacterOmni character:'+str(self.character)
    
class Buttons:
    ID = 18
    SIZE = 1    
    
    def __init__(self):
        self.is_clock    = None
        self.is_schedule = None
        self.is_day      = None
        self.is_hour     = None
        self.is_minute   = None
        self.is_dock     = None
        self.is_spot     = None
        self.is_clean    = None
        
    def decode(self,packet,ofs):
        #print(packet)
        self.is_clock    = ((packet[ofs]&128)>0)
        self.is_schedule = ((packet[ofs]&64)>0)
        self.is_day      = ((packet[ofs]&32)>0)
        self.is_hour     = ((packet[ofs]&16)>0)
        self.is_minute   = ((packet[ofs]&8)>0)
        self.is_dock     = ((packet[ofs]&4)>0)
        self.is_spot     = ((packet[ofs]&2)>0)
        self.is_clean    = ((packet[ofs]&1)>0)
    
    def __repr__(self):
        return ('Buttons is_clock:'+str(self.is_clock)+' is_schedule:'+str(self.is_schedule)+' is_day:'+str(self.is_day)+
                ' is_hour:'+str(self.is_hour)+' is_minute:'+str(self.is_minute)+' is_dock:'+str(self.is_dock)+
                ' is_spot:'+str(self.is_spot)+' is_clean:'+str(self.is_clean))

class Distance:
    ID = 19
    SIZE = 2
    
    def __init__(self):
        self.since_last_mm = None
        
    def decode(self,packet,ofs):
        self.since_last_mm = _signed_word_from_bytes(packet,ofs)
        
    def __repr__(self):
        return 'Distance since_last_mm:'+str(self.since_last_mm)

class Angle:
    ID = 20
    SIZE = 2
    
    def __init__(self):
        self.since_last_deg = None
        
    def decode(self,packet,ofs):
        self.since_last_deg = _signed_word_from_bytes(packet,ofs)
        
    def __repr__(self):
        return 'Angle since_last_deg:'+str(self.since_last_deg)
    
class ChargingState:
    ID = 21
    SIZE = 1
    
    def __init__(self):
        self.state = None
        
    def decode(self,packet,ofs):
        if packet[ofs]==0:
            self.state = (0,'Not charging')
        elif packet[ofs]==1:
            self.state = (1,'Reconditioning Charging')
        elif packet[ofs]==2:
            self.state = (2,'Full Charging')
        elif packet[ofs]==3:
            self.state = (3,'Trickle Charging')
        elif packet[ofs]==4:
            self.state = (4,'Waiting')
        elif packet[ofs]==5:
            self.state = (5,'Charging Fault Condition')
        else:
            self.state = (packet[ofs],'UNKNOWN VALUE')
            
    def __repr__(self):
        return 'ChargingState state:'+str(self.state)
    
class BatteryVoltage:
    ID = 22
    SIZE = 2
    
    def __init__(self):
        self.voltage = None
        
    def decode(self,packet,ofs):
        self.voltage = _unsigned_word_from_bytes(packet,ofs)/1000.0
        
    def __repr__(self):
        return 'BatteryVoltage voltage:'+str(self.voltage)
    
class BatteryCurrent:
    ID = 23
    SIZE = 2
    
    def __init__(self):
        self.current = None
        
    def decode(self,packet,ofs):
        self.current = _signed_word_from_bytes(packet,ofs)/1000.0
        
    def __repr__(self):
        return 'BatteryCurrent current:'+str(self.current)
    
class BatteryTemperature:
    ID = 24
    SIZE = 1
    
    def __init__(self):
        self.temperature_c = None
        
    def decode(self,packet,ofs):
        self.temperature_c = packet[ofs]
        if(self.temperature_c>127):
            self.temperature_c = self.temperature_c - 256
        
    def __repr__(self):
        return 'BatteryTemperature temperature_c:'+str(self.temperature_c)
    
class BatteryCharge:
    ID = 25
    SIZE = 2
    
    def __init__(self):
        self.charge_mah = None
        
    def decode(self,packet,ofs):
        self.charge_mah = _unsigned_word_from_bytes(packet,ofs)
        
    def __repr__(self):
        return 'BatteryCharge charge_mah:'+str(self.charge_mah)

class BatteryCapacity:
    ID = 26
    SIZE = 2
    
    def __init__(self):
        self.capacity_mah = None
        
    def decode(self,packet,ofs):
        self.capacity_mah = _unsigned_word_from_bytes(packet,ofs)
        
    def __repr__(self):
        return 'BatteryCapacity capacity_mah:'+str(self.capacity_mah)    
    
class WallSignal:
    ID = 27
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'WallSignal signal:'+str(self.signal)

class CliffLeftSignal:
    ID = 28
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'WallSignal signal:'+str(self.signal)
    
class CliffFrontLeftSignal:
    ID = 29
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'CliffFrontLeftSignal signal:'+str(self.signal)
    
class CliffFrontRightSignal:
    ID = 30
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'CliffFrontRightSignal signal:'+str(self.signal)
    
class CliffRightSignal:
    ID = 31
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'CliffRightSignal signal:'+str(self.signal)
    
class ChargingSourcesAvailable:
    ID = 34
    SIZE = 1
    def __init__(self):
        self.is_home_base = None
        self.is_internal_charger = None
    def decode(self,packet,ofs):
        self.is_home_base = ((packet[ofs]&2)>0)
        self.is_internal_charger = ((packet[ofs]&1)>0)
    def __repr__(self):
        return ('ChargingSourcesAvailable is_home_base:'+str(self.is_home_base)+
                ' is_internal_charger:'+str(self.is_internal_charger))
    
class OIMode:
    ID = 35
    SIZE = 1
    def __init__(self):
        self.mode = None
    def decode(self,packet,ofs):
        if packet[ofs]==0:
            self.mode = (0,'Off')
        elif packet[ofs]==1:
            self.mode = (1,'Passive')
        elif packet[ofs]==2:
            self.mode = (2,'Safe')
        elif packet[ofs]==3:
            self.mode = (3,'Full')        
    def __repr__(self):
        return 'OIMode mode:'+str(self.mode)

class SongNumber:
    ID = 36
    SIZE = 1
    def __init__(self):
        self.song = None
    def decode(self,packet,ofs):
        self.song = packet[ofs]
    def __repr__(self):
        return 'SongNumber song:'+str(self.song)
        
class SongPlaying:
    ID = 37
    SIZE = 1
    def __init__(self):
        self.is_playing = None
    def decode(self,packet,ofs):
        self.is_playing = (packet[ofs]==1)
    def __repr__(self):
        return 'SongPlaying is_playing:'+str(self.is_playing)
    
class NumberStreamPackets:
    ID = 38
    SIZE = 1
    def __init__(self):
        self.num_packets = None
    def decode(self,packet,ofs):
        self.num_packets = packet[ofs]
    def __repr__(self):
        return 'NumberStreamPackets num_packets:'+str(self.num_packets)
    
class RequestedVelocity:
    ID = 39
    SIZE = 2
    def __init__(self):
        self.requested_velocity = None
    def decode(self,packet,ofs):
        self.requested_velocity = _signed_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'RequestedVelocity requested_velocity:'+str(self.requested_velocity)

class RequestedRadius:
    ID = 40
    SIZE = 2
    def __init__(self):
        self.requested_radius = None
    def decode(self,packet,ofs):
        self.requested_radius = _signed_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'RequestedRadius requested_radius:'+str(self.requested_radius)

class RequestedRightVelocity:
    ID = 41
    SIZE = 2
    def __init__(self):
        self.requested_right_velocity = None
    def decode(self,packet,ofs):
        self.requested_right_velocity = _signed_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'RequestedRightVelocity requested_right_velocity:'+str(self.requested_right_velocity)
    
class RequestedLeftVelocity:
    ID = 42
    SIZE = 2
    def __init__(self):
        self.requested_left_velocity = None
    def decode(self,packet,ofs):
        self.requested_left_velocity = _signed_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'RequestedLeftVelocity requested_left_velocity:'+str(self.requested_left_velocity)
    
class LeftEncoderCounts:
    ID = 43
    SIZE = 2
    def __init__(self):
        self.count = None
    def decode(self,packet,ofs):
        self.count = _signed_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'LeftEncoderCounts count:'+str(self.count)
    
class RightEncoderCounts:
    ID = 44
    SIZE = 2
    def __init__(self):
        self.count = None
    def decode(self,packet,ofs):
        self.count = _signed_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'RightEncoderCounts count:'+str(self.count)
    
class LightBumper:
    ID = 45
    SIZE = 1
    def __init__(self):
        self.is_right = None
        self.is_front_right = None
        self.is_center_right = None
        self.is_center_left = None
        self.is_front_left = None
        self.is_left = None
    def decode(self,packet,ofs):
        self.is_right        = ((packet[ofs]&32)>0)
        self.is_front_right  = ((packet[ofs]&16)>0)
        self.is_center_right = ((packet[ofs]&8)>0)
        self.is_center_left  = ((packet[ofs]&4)>0)
        self.is_front_left   = ((packet[ofs]&2)>0)
        self.is_left         = ((packet[ofs]&1)>0)
    def __repr__(self):
        return ('LightBumper is_right:'+str(self.is_right)+' is_front_right:'+str(self.is_front_right)+
                ' is_center_right:'+str(self.is_center_right)+' is_center_left:'+str(self.is_center_left)+
                ' is_front_left:'+str(self.is_front_left)+' is_left:'+str(self.is_left) )
    
class LightBumpLeftSignal:
    ID = 46
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'LightBumpLeftSignal signal:'+str(self.signal)
    
class LightBumpFrontLeftSignal:
    ID = 47
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'LightBumpFrontLeftSignal signal:'+str(self.signal)
    
class LightBumpCenterLeftSignal:
    ID = 48
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'LightBumpCenterLeftSignal signal:'+str(self.signal)
    
class LightBumpCenterRightSignal:
    ID = 49
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'LightBumpCenterRightSignal signal:'+str(self.signal)
    
class LightBumpFrontRightSignal:
    ID = 50
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'LightBumpFrontRightSignal signal:'+str(self.signal)
    
class LightBumpRightSignal:
    ID = 51
    SIZE = 2
    def __init__(self):
        self.signal = None
    def decode(self,packet,ofs):
        self.signal = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'LightBumpRightSignal signal:'+str(self.signal)
    
class InfraredCharacterLeft:
    ID = 52
    SIZE = 1
    def __init__(self):
        self.character = None
    def decode(self,packet,ofs):
        self.character = packet[ofs]
    def __repr__(self):
        return 'InfraredCharacterLeft character:'+str(self.character)

class InfraredCharacterRight:
    ID = 53
    SIZE = 1
    def __init__(self):
        self.character = None
    def decode(self,packet,ofs):
        self.character = packet[ofs]
    def __repr__(self):
        return 'InfraredCharacterRight character:'+str(self.character)
    
class LeftMotorCurrent:
    ID = 54
    SIZE = 2
    def __init__(self):
        self.current_ma = None
    def decode(self,packet,ofs):
        self.current_ma = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'LeftMotorCurrent current_ma:'+str(self.current_ma)
    
class RightMotorCurrent:
    ID = 55
    SIZE = 2
    def __init__(self):
        self.current_ma = None
    def decode(self,packet,ofs):
        self.current_ma = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'RightMotorCurrent current_ma:'+str(self.current_ma)
    
class MainBrushMotorCurrent:
    ID = 56
    SIZE = 2
    def __init__(self):
        self.current_ma = None
    def decode(self,packet,ofs):
        self.current_ma = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'MainBrushMotorCurrent current_ma:'+str(self.current_ma)
    
class SideBrushMotorCurrent:
    ID = 57
    SIZE = 2
    def __init__(self):
        self.current_ma = None
    def decode(self,packet,ofs):
        self.current_ma = _unsigned_word_from_bytes(packet,ofs)
    def __repr__(self):
        return 'SideBrushMotorCurrent current_ma:'+str(self.current_ma)
    
class Stasis:
    ID = 58
    SIZE = 1
    def __init__(self):
        self.is_disabled = None
        self.is_toggling = None
    def decode(self,packet,ofs):
        self.is_disabled   = ((packet[ofs]&2)>0)
        self.is_toggling   = ((packet[ofs]&1)>0)
    def __repr__(self):
        return 'Stasis is_disabled:'+str(self.is_disabled)+' is_toggling:'+str(self.is_toggling)
