class Notification:
    def get_text_notification(self, machineType):
        """
        Returns the string of text customized to the user for a SMS notification

        Args:
            machineType (str): 'Washer' or 'Dryer'

        Returns:
            str: customized text notification
        """
        return "Your {machineType} cycle has finished. Please swap or pick up your laundry\n\nSincerely,\nWasherBuddie Team".format(machineType=machineType)

    def get_email_notification(self, userName, machineType):
        """
        Returns the string of text customized to the user for an email notification

        Args:
            userName (str): user's full name
            machineType (str): 'Washer' or 'Dryer'

        Returns:
            str: customized email notification
        """
        return "Hello {userName},\n\nYour {machineType} cycle has finished. Please swap or pick up your laundry from the laundry room at your earliest convenience.\n\nSincerely,\nWasherBuddie Team".format(userName=userName, machineType=machineType)
    
    def get_follow_up_text_notification(self, machineType):
        """
        Returns the string of text customized to the user for a follow-up SMS notification

        Args:
            machineType (str): 'Washer' or 'Dryer'

        Returns:
            str: customized follow-up text notification
        """
        return "Your {machineType} cycle has been stagnant and other people would like to use this machine.\n\nPlease swap or pick up your laundry as soon as possible to be courteous to others. If you are unable to do attend to your laundry at this time, please send a message in the House group chat.\n\nSincerely,\nWasherBuddie Team".format(machineType=machineType)
    
    def get_follow_up_email_notification(self, userName, machineType):
        """
        Returns the string of text customized to the user for a follow-up email notification

        Args:
            userName (str): user's full name
            machineType (str): 'washer' or 'dryer'

        Returns:
            str: customized follow-up email notification
        """
        return "Hello {userName},\n\nYour {machineType} cycle has been stagnant and other people would like to use this machine. Please swap or pick up your laundry as soon as possible to be courteous to others. If you are unable to do attend to your laundry at this time, please send a message in the House group chat.\n\nSincerely,\nWasherBuddie Team".format(userName=userName, machineType=machineType)
