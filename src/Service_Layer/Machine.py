from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from mongoDB.CRUD_api import Database_Manager
    from src.Service_Layer.User import User

class Machine:
    """
    A class representing a washer or dryer machine
    """

    def __init__(self, machine_type: str, machine_id: int):
        """
        Creates a new instance of a Machine

        Args:
            machine_type (str): either a washer or dryer
            machine_id (int): id of the machine

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
        
        from mongoDB.CRUD_api import Database_Manager
        CRUD = Database_Manager()
        if self._machine_type == 'Washer':
            CRUD.insert_washer(self)
        elif self._machine_type == 'Dryer':
            CRUD.insert_dryer(self)
        

    @property
    def machine_id(self) -> int:
        """Getter for the machine id."""
        return self._machine_id
    
    @machine_id.setter
    def machine_id(self, value: int):
        """
        Sets the machine id

        Args:
            value (int): id for the machine
        """
        self._machine_id = value

    @property
    def current_state(self) -> str:
        """Getter for the current state."""
        return self._current_state

    @current_state.setter
    def current_state(self, value: tuple) -> None:
        from .User import User
        from mongoDB.CRUD_api import Database_Manager
       
        if not isinstance(value, tuple) or len(value) != 2 or not isinstance(value[1], User):
            raise TypeError("Invalid state or user type")
        
        next_state = value[0]
        user = value[1]
        
        if self.current_state == 'Out of Order' and not user.is_admin:
            raise ValueError("Machine is out of order and cannot be changed")
        
        CRUD = Database_Manager()

        if next_state == "Out of Order" and user.is_admin == True:
            self._current_state = "Out of Order"
            CRUD.change_machine_state(self.machine_id, "Out of Order")
            self._who_is_using = None
            self._start_time = None
            self._end_time = None
            return
        
        if next_state == "Out of Order" and user.is_admin == False:
            raise ValueError("Only admins can set the machine to 'Out of Order'")
        
        if self._current_state == 'Available' and next_state == 'In Use':
            # Starting cycle
            self._start_time = datetime.now()
            self._current_state = 'In Use'
            CRUD.change_machine_state(self.machine_id, 'In Use')
            self._who_is_using = user.user_name 
            '''
            CHANGE TIME DELTA BASED ON MACHINE TYPE AFTER DEMO
            '''
            time_change = timedelta(minutes=1 if self.machine_type == 'Washer' else 1)
            self._end_time = self.start_time + time_change
        elif self._current_state == 'In Use' and next_state == 'Available':
            # Ending cycle
            self._current_state = 'Available'
            CRUD.change_machine_state(self.machine_id, 'Available')
            self._who_is_using = None  
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
    def start_time(self, start_time:Optional[Union[datetime, None]]=None):
        """
        Sets the time the machine cycle was started

        Args:
            start_time (datetime, optional): Specific time. Defaults to datetime.now().
        """
        self._start_time = start_time if start_time else datetime.now()
        from mongoDB.CRUD_api import Database_Manager
        CRUD = Database_Manager()
        CRUD.change_machine_start_time(self.machine_id, self._start_time)

    @property
    def end_time(self):
        """
        Returns the time the machine cycle will end

        Returns:
            datetime: date and time the machine cycle will end 
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time: Union[datetime, None]):
        """
        Sets the time the machine cycle will end

        Args:
            end_time (datetime): date and time the machine cycle will end
        """
        self._end_time = end_time
        from mongoDB.CRUD_api import Database_Manager
        CRUD = Database_Manager()
        CRUD.change_machine_end_time(self.machine_id, end_time)

    @property
    def machine_type(self) -> str:
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
    def who_is_using(self, user_name: Union[str, None]):
        """
        Sets the user who is currently using the machine

        Args:
            user_name (str): current machine user's name
        """
        self._who_is_using = user_name
        from mongoDB.CRUD_api import Database_Manager
        CRUD = Database_Manager()
        CRUD.change_machine_user(self.machine_id, user_name)
