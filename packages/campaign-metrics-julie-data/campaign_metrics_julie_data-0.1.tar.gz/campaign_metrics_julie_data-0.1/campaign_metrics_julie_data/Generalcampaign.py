from datetime import datetime
from dateutil.parser import parse

class Campaign:
    
    def __init__(self, name, start, end, eligible_customers, control_proportion):
        
        """ Generic campaign class to calculate 
        performance metrics on the campaign.
        
        Attributes
            name (string) representing the campaign name
            start_date (string YYYY-MM-DD) representing the first day of the campaign
            end_date (string YYYY-MM-DD) representing the last day of the campaign
            eligible_customers (float) representing the number of customers eligible
            control_proportion (flot) representing the proportion of customers in the control group
            """
        
        self.name = name
        self.start = start
        self.end = end
        self.eligible_customers = eligible_customers
        self.control_proportion = control_proportion
        
    def calculate_length(self):
        
        """ Function to calculate the length of the campaign
        in days.
        
        Args:
            None
            
        Returns:
            length (float) represents campaign length in days
        """
        
        format_str = '%Y-%m-%d'
        delta = datetime.strptime(self.end, format_str) - datetime.strptime(self.start, format_str)
        length = delta.days
        
        return length
    
    
        
    def calculate_treatment_size(self):
        
        """Function to calculate the number of eligible customers
        in the treatment group.
        
        Args:
            None
            
        Returns:
            treatment_size (float) represents the number of eligible customers in the treatment group
        """
        
        treatment_size = self.eligible_customers * (1 - self.control_proportion)
        
        return treatment_size
    
    
    
    def calculate_control_size(self):
        
        """Function to calculate the number of eligible customers
        in the treatment group.
        
        Args:
            None
            
        Returns:
            control_size (float) represents the number of eligible customers in the control group
        """
        
        control_size = self.eligible_customers * self.control_proportion
        
        return control_size