from datetime import datetime, timedelta
from Service_Layer.User import User

class Machine:
    """
    A class representing a washer or dryer machine
    """

    def __init__(self, machine_type, machine_id):
        """
        Creates a new instance of a Machine

        Args:
            machine_type (str): either a washer or dryer

        Raises:
            ValueError: raises error if the machine type is not a washer or dryer
        """
        if machine_type.title() == 'Washer' or machine_type.title() == 'Dryer':
            self._machine_type = machine_type
        else:
            raise ValueError("Invalid machine type")

        self._machine_id = machine_id
        self._current_state = 'Available'
        self._start_time = None
        self._end_time = None
        self._who_is_using = None

    @property
    def machine_id(self):
        """Getter for the machine id."""
        return self._machine_id
    
    @machine_id.setter
    def machine_id(self, value):
        """
        Sets the machine id

        Args:
            value (int): id for the machine
        """
        self._machine_id = value

    @property
    def current_state(self):
        """Getter for the current state."""
        return self._current_state

    @current_state.setter
    def current_state(self, value):

        if not isinstance(value, tuple) or len(value) != 2 or not isinstance(value[1], User):
            raise TypeError("Invalid state or user type")
        
        next_state = value[0]
        user = value[1]

        if next_state == "Out of Order" and user.is_admin == True:
            self._current_state = "Out of Order"
            return
        
        if next_state == "Out of Order" and user.is_admin == False:
            raise ValueError("Only admins can set the machine to 'Out of Order'")
        

        if self._current_state == 'Available' and next_state == 'In Use':
            # Starting cycle
            self._start_time = datetime.now()
            self._current_state = 'In Use'
            self.who_is_using = user.user_name 
            '''
            CHANGE TIME DELTA BASED ON MACHINE TYPE AFTER DEMO
            '''
            time_change = timedelta(minutes=50 if self.machine_type == 'Washer' else 60)
            self.end_time = self.start_time + time_change
        elif self._current_state == 'In Use' and next_state == 'Available':
            # Ending cycle
            self._current_state = 'Available'
            self.who_is_using = None  
            self._end_time = None
            self._start_time = None
        else:
            raise ValueError("Invalid state transition")

    @property
    def start_time(self):
        """
        Returns the time the machine cycle was started

        Returns:
            datetime: date and time the machine cycle was started
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time=None):
        """
        Sets the time the machine cycle was started

        Args:
            start_time (datetime, optional): Specific time. Defaults to datetime.now().
        """
        self._start_time = start_time if start_time else datetime.now()

    @property
    def end_time(self):
        """
        Returns the time the machine cycle will end

        Returns:
            datetime: date and time the machine cycle will end 
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """
        Sets the time the machine cycle will end

        Args:
            end_time (datetime): date and time the machine cycle will end
        """
        self._end_time = end_time

    @property
    def machine_type(self):
        """
        Returns the type of machine

        Returns:
            str: 'Washer' or 'Dryer'
        """
        return self._machine_type
                
    @property
    def who_is_using(self):
        """
        Returns the user who is currently using the machine

        Returns:
            str: current machine user's name
        """
        return self._who_is_using
    
    @who_is_using.setter
    def who_is_using(self, user_name):
        """
        Sets the user who is currently using the machine

        Args:
            user_name (str): current machine user's name
        """
        self._who_is_using = user_name
