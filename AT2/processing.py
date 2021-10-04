"""
    Logical processing classes used in the second assignment for CSSE1001/7030.

    ProcessResults: Abstract class that defines the logical processing interface.
    AthleteResults: Provides details of one athlete’s results for all of the
                    events in which they competed.
    CountryResults: Provides a summary of the results of all athletes who
                    competed for one country.
    EventResults  : Provides details of the results of all athlete's who
                    competed in one event.
    DeterminePlaces: Determines the place ranking of all athletes who competed
                     in one event.
"""

__author__ = "Nikhil Naik"
__email__ = "s4529385@uq.edu.au"



from entities import Athlete, Result, Event, Country, ManagedDictionary
from entities import all_athletes, all_countries, all_events, load_data



class ProcessResults(object) :
    """Superclass for the logical processing commands."""

    _processing_counter = 0  # Number of times any process command has executed.
    
    def process(self) :
        """Abstract method representing collecting and processing results data.
        """
        ProcessResults._processing_counter += 1
    
    def get_results(self) :
        """Abstract method representing obtaining the processed results.

        Return:
            list: Subclasses will determine the contents of the resulting list.
        """
        raise NotImplementedError()



class AthleteResults(ProcessResults) :
    """Determines the resuls achieved by one athlete."""
    
    _athlete_results_counter = 0  # Number of times this command has executed.

    def __init__(self, athlete) :
        """
        Parameters:
            athlete (Athlete): Athlete for whom we wish to determine their results.
        """
        self._athlete = athlete
        self._results = []
        self._placings = []
        self._athlete_final = []

    def process(self) :
        """Obtain all the results for this athlete and
           order them from best to worst placing.
           If two or more results have the same place they should be ordered
           by event name in ascending alphabetical order.
        """
        
        super().process()   #A call to the superclass
        AthleteResults._athlete_results_counter += 1
        
        
        def sorter_key_event1(temp_tuple):
            """
            Parameters:
            temp_tuple (Tuple): A tuple containing the result and eventobject
            Return:
                (int): The place value achieved
                (str): The name of the event
            """
            result, event = temp_tuple
            return int(result.get_place()), event.get_name()
        
        self._athlete_event = self._athlete.get_events()
        for event in self._athlete_event:
            result = self._athlete.get_result(event)
            temp_tuple = (result,event)
            self._results.append(temp_tuple) 
            self._results.sort(key = sorter_key_event1)        #sorts by the 
        for i, (result,eventname) in enumerate(self._results): #the place, if a
            self._athlete_final.append(result)                 #tie the sorts by
                                                               #event name 
            

    def get_results(self) :
        """Obtain the processed results for _athlete.

        Return:
            list[Result]: Ordered list of the _athlete's results.
                          Sorted from best to worst, based on place in event.
                          Results with the same place are ordered by event name
                          in ascending alphabetical order.

        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._athlete_final != []:
            return self._athlete_final  #If the list is empty, accounts for 
        else:                           #a value error
            raise ValueError

    def get_usage_ratio() :
        """Ratio of usage of the AthleteResults command against all commands.

        Return:
            float: ratio of _athlete_results_counter by _processing_counter.
        """
        return (AthleteResults._athlete_results_counter
                / AthleteResults._processing_counter)

    def __str__(self) :
        """(str) Return a formatted string of the results for this athlete."""
        """Implementation of this is optional but useful for observing your
           programs behaviour.
        """
        return ""

class EventResults(ProcessResults):
    _event_results_counter = 0
    """Determine the order of Athletes from best to worst in an event"""
    def __init__(self, event):
        """
        Parameters:
            event (Event): Object representing the event to query.
        """
        self._athlete_list = []
        self._event = event
        self._event_results = []
        self._final_list = []
        
    def process(self):
        """Obtain all the results for this event and
           order the Athletes from best to worst placing.
           If two or more Athletes have the same place they should be ordered
           by Athlete name name in ascending alphabetical order.
        """
        super().process()   #Call for superclass
        EventResults._event_results_counter += 1
        self.order_results()
        self.get_results()
        
        

    def get_results(self):
        """The get_results
        method is to return a list of Athlete objects that are ordered according to the logic implemented in
        the process method, returning a list of Athlete objects in order of thir place in an event.
        
        Return:
            list[Result]: A list of Athletes ordered by their result in the event.
        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._final_list != []:
            return  self._final_list            #If list is empty
        else:                                   #accounts for valueerror
            raise ValueError
    
    def order_results(self):
        """The order_results
        method is to process for each Athlete competing in the event to extract thier result and order these
        results from best to worst in a list format of Athlete objects.If a tie
        occurs, then it is sorted alpabetically by the athletes name
        """

        def sorter_key_event(new_tuple):
            """
            Parameters:
                new_tuple (Tuple): A tuple representing the athlete object and result object for the athlete.
            Return:
            
                float : The place that correlates to the result value achieved by the athlete.
                string: Name of the competing athlete
            """
            resultval, athlete = new_tuple
            return float(resultval.get_place()), athlete.get_full_name()
        
        athletes = self._event.get_athletes() #getting list of athletes
        for athlete in athletes:
            resultval = athlete.get_result(self._event)
            new_tuple = (resultval, athlete)
            self._athlete_list.append(new_tuple)
            self._athlete_list.sort(key = sorter_key_event) #Sorts first by result,
                                                    #if tie, then sorts by name
        for i, (resultval,athlete) in enumerate(self._athlete_list):
            self._final_list.append(athlete)        #adding each athlete to list
                    
       
    def get_usage_ratio() :
        """Ratio of usage of the AthleteResults command against all commands.

        Return:
            float: ratio of _athlete_results_counter by _processing_counter.
        """
        return (EventResults._event_results_counter/ EventResults._processing_counter)


class CountryResults(ProcessResults):
    """Determine the number of medals and Athletes competing for a delegation"""
    _country_results_counter = 0
    def __init__(self, country):
        """
        Parameters:
            country (Country): Country Object representing the country to query.
        """
        
        self._country = country
        self._medel_list = []
        self._gold_num = 0
        self._silver_num = 0
        self._bronze_num = 0
        self._num_athletes = 0
        self._item = ""
        
    def process(self) :
        """Obtain all the results for this country and
           count the number of Gold, Silver and Bronze medals achieved for
           each athlete in the country and the number of athletes for the
           country.
        """
        #Calling all the methods for the country
        super().process() #Inheritance from the superclass
        CountryResults._country_results_counter += 1
        self.get_num_gold()
        self.get_num_silver()
        self.get_num_bronze()
        self.get_num_athletes()
        self.get_results()
    


        
    def get_results(self):
        """Obtain the processed results for the delegations performance in the games. 

        Return:
            list[Result]: Ordered list of the country's performance in the games, with the
            number of Gold, Silver, Bronze and athletes in a list.

        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._num_athletes != 0:
            return [self._gold_num,self._silver_num,self._bronze_num,self._num_athletes]
        else:
            raise ValueError    #Raising a value error if the list is empty
        
        
        
    def get_usage_ratio():
        """Ratio of usage of the CountryResults command against all commands.

        Return:
            float: ratio of _country_results_counter by _processing_counter.
        """
        print(CountryResults._country_results_counter)
        print(CountryResults._processing_counter)
        return (CountryResults._country_results_counter/ CountryResults._processing_counter)
    
    def get_num_gold(self):
        """Calculates the number of Gold medals achieved by the country.
        Where the value 'c' is the event object.
        Return:
            Integer: number of Gold medals achieved by the delegation. 
        """
        athletes = self._country.get_athletes()
        for athlete in athletes:
            events = athlete.get_events()
            for c in events: #C is a numerical value for an event objecr
                result_val = athlete.get_result(c)
                medel = result_val.get_medal()
                if medel == "Gold":
                    self._gold_num = self._gold_num + 1
        return self._gold_num

            
    
    def get_num_silver(self):
        """Calculates the number of Silver medals achieved by the country.

        Return:
            Integer: number of Silver medals achieved by the delegation. 
        """
        athletes = self._country.get_athletes()
        for athlete in athletes:
            events = athlete.get_events()
            for c in events: #c is a numerical constant for event object
                result_val = athlete.get_result(c)
                medel = result_val.get_medal()
                if medel == "Silver": #compraring medal to increment count
                    self._silver_num = self._silver_num + 1
        return self._silver_num
    
    
    def get_num_bronze(self):
        """Calculates the number of Bronze medals achieved by the country.

        Return:
            Integer: number of Bronze medals achieved by the delegation. 
        """
        athletes = self._country.get_athletes()
        for athlete in athletes:
            events = athlete.get_events()
            for c in events: #where c is a numerical constant representing event
                result_val = athlete.get_result(c)  #object
                medel = result_val.get_medal()
                if medel == "Bronze":   #Comparing whether the athlete has a medel
                    self._bronze_num = self._bronze_num + 1
        return self._bronze_num
    
    def get_num_athletes(self):
        """Calculates the number of competing for the country.

        Return:
            Integer: number of athletes competing for the delegation. 
        """
        
        athletes = self._country.get_athletes() #Getting the list of athletes
        for athlete in athletes:                #use of imported classes
            self._num_athletes = self._num_athletes + 1
        
        return self._num_athletes
        
        
    
    def __str__(self) :
        """.
        """
        return ""

            
class DeterminePlaces(ProcessResults):
    """Determines the place ahcieved for an athlete in a given event"""
    _determine_places_counter = 0
    def __init__(self, event):
        """
        Parameters:
            event (Event): Event Object representing the event to query.
        """
        self._event = event
        self._athlete_result_list = []
        self._event_results  = None


        
    def get_results(self):
        """Obtains a list of athletes . 

        Return:
            list[Result]: Ordered list of the country's performance in the games, with the
            number of Gold, Silver, Bronze and athletes in a list.

        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._event_results is not None:
            return self._event_results      
        else:
            raise ValueError            #If the list is empty then the value
                                        #Error is raised

    def process(self) :
        """Obtain all the results  and athlete objects for this event and
           sets the place of the Athlete, based on the result from best to worst,
           accounting for either a scored or a timed event.
        """
        def sorter_key1(result_tuple):
            """
            Parameters:
                result_tuple (Tuple): A tuple representing the athlete object and result object for the athlete.
            Return:
            
                float : The result that correlates to the result object achieved in the event.
            """
            athlete, result = result_tuple
            return float(result.get_result())   #A sub function to return the result
        

        super().process()#Utilizing the superclass

        list_of_athletes =  self._event.get_athletes()
        for athlete in list_of_athletes:#Iterating over each athlete in the event
            resultval = athlete.get_result(self._event)#class structure to access result
            result_tuple = (athlete, resultval)
            self._athlete_result_list.append(result_tuple)
            self._athlete_result_list.sort(key = sorter_key1, reverse = not self._event.is_timed())
        place = 1
        for i, (athlete,result) in enumerate(self._athlete_result_list):
            #This line assigns an index to each tuple so it can be accessed 
            next_result = self._athlete_result_list[i-1][1]
            #This gets the previuos result by indexing the result in the tuple list 
            if i == 0:

                result.set_place(place)
            elif result == next_result:         #If the result is equal, then the
                place = next_result.get_place() #two athletes achieve the same place,
                result.set_place(place)         # This is set using the result class
                next_result.set_place(place)
            else:
                result.set_place(i+1)
            athlete_place = (athlete,place)
        
        self._event_results = [athlete for athlete, result in self._athlete_result_list]
        #Adding each Athlete object and Result to an ordered list
        DeterminePlaces._determine_places_counter += 1

        
    def get_usage_ratio():
        """Ratio of usage of the AthleteResults command against all commands.

        Return:
            float: ratio of _athlete_results_counter by _processing_counter.
        """
        print(DeterminePlaces._determine_places_counter)
        print(DeterminePlaces._processing_counter)
        return (DeterminePlaces._determine_places_counter/DeterminePlaces._processing_counter)            
            
def demo_entities() :
    """Simple test code to demonstrate using the entity classes.
       Output is to console.
    """
    TIMED = True
    SCORED = False

    print("Demonstrate creating country objects:")
    CAN = Country("Canada", "CAN")
    AUS = Country("Australia", "AUS")
    all_countries.add_item(CAN.get_country_code(), CAN)
    all_countries.add_item(AUS.get_country_code(), AUS)
    for country in all_countries.get_items() :
        print(country)

    print("\nDemonstrate creating athlete objects, adding them to",
          "all_athletes and countries:")
    a1 = Athlete("1", "Athlete", "One", CAN)
    a2 = Athlete("2", "Athlete", "Two", CAN)
    a3 = Athlete("10", "Athlete", "Three", CAN)
    a4 = Athlete("4", "Athlete", "Four", AUS)
    a5 = Athlete("5", "Athlete", "Five", AUS)
    a6 = Athlete("20", "Athlete", "Six", AUS)
    for athlete in [a1, a2, a3, a4, a5, a6] :
        all_athletes.add_item(athlete.get_id(), athlete)
    athletes = all_athletes.get_items()
    for athlete in athletes :
        print(athlete)
    CAN.add_athletes([a1, a2, a3])
    AUS.add_athletes([a4, a5, a6])
    print("\nDemonstrate finding an athlete in all_athletes:")
    print(all_athletes.find_item("2"))

    # Create event objects and add athletes to the events.
    e1 = Event("Event1", TIMED, [a1, a2, a3, a4, a5])
    all_events.add_item(e1.get_name(), e1)
    a2.add_event(e1)
    a3.add_event(e1)
    a4.add_event(e1)
    a5.add_event(e1)
    e2 = Event("Event2", SCORED, [a1, a2, a3, a5, a6])
    all_events.add_item(e2.get_name(), e2)
    a2.add_event(e2)
    a3.add_event(e2)
    a5.add_event(e2)
    a6.add_event(e2)
    a1.add_events([e1, e2])

    # Create result objects for each athlete in the events.
    a1.add_result(e1, Result(10.5))
    a2.add_result(e1, Result(9.5))
    a3.add_result(e1, Result(11.5))
    a4.add_result(e1, Result(8.5))
    a5.add_result(e1, Result(12.5))

    a1.add_result(e2, Result(100.5))
    a2.add_result(e2, Result(99.5))
    a3.add_result(e2, Result(98.5))
    a5.add_result(e2, Result(90.5))
    a6.add_result(e2, Result(89.5))



def demo_processing() :
    """Simple test code to demonstrate using the processing classes.
       Output is to console.
    """
    print("\n\nDemonstrate processing of results:")
    for athlete in all_athletes.get_items() :
        athlete_results = AthleteResults(athlete)
        athlete_results.process()
        results = athlete_results.get_results()
        # Do something with this athlete's results.

    print("\nDemonstrate listing the results for an event:")
    event = all_events.find_item("Event1")
    results_dict = {}
    for athlete in event.get_athletes() :
        results_dict[athlete.get_result(event).get_result()] = \
            athlete.get_result(event)
    for result in sorted(results_dict) :
        print(result)

    print("\nAthleteResults was used",
          "{0:.1%}".format(AthleteResults.get_usage_ratio()),
          "of the time of all results processing commands.")



if __name__ == "__main__" :
    #pass
    demo_entities()
    demo_processing()
