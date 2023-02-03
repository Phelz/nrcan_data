from dataclasses import dataclass

@dataclass
class Riometer:

    name : str
    tag : str
    lon: float
    lat: float
    status: str


# TODO: Will define frequeny range (and other things) based on the type
@dataclass
class HyperSpectralRiometer(Riometer):
    riometer_type: str = "HSR" 
    

@dataclass
class IrisRiometer(Riometer):
    riometer_type: str = "Widebeam" # Could be IRIS-Widebeam/ beam
    
@dataclass
class LaJollaRiometer(Riometer):
    riometer_type: str = "La Jolla"

