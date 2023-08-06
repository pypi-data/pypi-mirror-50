from enum import Enum

"""
    Определяет максимальные размеры строковых типов
"""
class MaxLen:
    IdToken = 20
    SerialNumberString = 25


class ChargePointErrorCode(Enum):
    ConnectorLockFailure = 'ConnectorLockFailure'
    GroundFailure = 'GroundFailure'
    HighTemperature = 'HighTemperature'
    Mode3Error = 'Mode3Error'
    NoError = 'NoError'
    OtherError = 'OtherError'
    OverCurrentFailure = 'OverCurrentFailure'
    PowerMeterFailure = 'PowerMeterFailure'
    PowerSwitchFailure = 'PowerSwitchFailure'
    ReaderFailure = 'ReaderFailure'
    ResetFailure = 'ResetFailure'
    UnderVoltage = 'UnderVoltage'
    WeakSignal = 'WeakSignal'


class RemoteStartStopStatus(Enum):
    Accepted = 'Accepted'
    Rejected = 'Rejected'


class AvailabilityType(Enum):
    Inoperative = 'Inoperative' # Charge point is not available for charging.
    Operative = 'Operative'     # Charge point is available for charging.


class AvailabilityStatus(Enum):
    Accepted = 'Accepted'       # Request has been accepted and will be executed.
    Rejected = 'Rejected'       # Request has not been accepted and will not be executed.
    Scheduled = 'Scheduled'     # Request has been accepted and will be executed when transaction(s) in progress have finished.


class RegistrationStatus(Enum):
    Accepted = 'Accepted'   # Charge point is accepted by Central System.
    Rejected = 'Rejected'   # Charge point is not accepted by Central System. This happens when the charge point id is not known by Central System.


class ReservationStatus(Enum):
    Accepted = 'Accepted'   #Reservation has been made.
    Faulted = 'Faulted'     #Reservation has not been made, because connectors or specified connector are in a faulted state.
    Occupied = 'Occupied'   #Reservation has not been made. All connectors or the specified connector are occupied.    
    Rejected = 'Rejected'   #Reservation has not been made. Charge Box is not configured to accept reservations.
    Unavailable = 'Unavailable' # Reservation has not been made, because connectors or specified connector are in an unavailable state.


class CancelReservationStatus(Enum):
    Accepted = 'Accepted'   # Reservation for the identifier has been cancelled
    Rejected = 'Rejected'   # Reservation could not be cancelled, because there is no reservation active for the identifier.


class ResetStatus(Enum):
    Accepted = 'Accepted'
    Rejected = 'Rejected'


class ResetType(Enum):
    Hard = 'Hard'   # Full reboot of charge box software.
    Soft = 'Soft'   # Return to initial status, gracefully terminating any transactions in progress.


class ConfigurationStatus(Enum):
    Accepted = 'Accepted'
    Rejected = 'Rejected'           # Configuration key supported, but setting could not be changed.
    NotSupported = 'NotSupported'   # Configuration key is not supported.


class OcppErrorCode(Enum):
    # Requested Action is not known by receiver
    NotImplemented = 'NotImplemented'
    
    # Requested Action is recognized but not supported by the receiver
    NotSupported = 'NotSupported'
    
    # An internal error occurred and the receiver was not able to process the requested 
    # Action successfully
    InternalError = 'InternalError'
    
    # Payload for Action is incomplete
    ProtocolError = 'ProtocolError'
    
    # During the processing of Action a security issue occurred preventing receiver from completing the
    # Action successfully
    SecurityError = 'SecurityError'
    
    # Payload for Action is syntactically incorrect or not
    # conform the PDU structure for Action    
    FormationViolation = 'FormationViolation'
    
    # Payload is syntactically correct but at least one field contains an invalid value
    PropertyConstraintViolation = 'PropertyConstraintViolation'
    
    # Payload for Action is syntactically correct but at least one of the fields 
    # violates occurence constraints
    OccurenceConstraintViolation = 'OccurenceConstraintViolation'
    
    # Payload for Action is syntactically correct but at least one of the 
    # fields violates data type constraints (e.g. “somestring”: 12)
    TypeConstraintViolation = 'TypeConstraintViolation'
    
    # Any other error not covered by the previous ones
    GenericError = 'GenericError'
