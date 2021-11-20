class PetriNet:
    def __init__(self, master): pass
    def createWidgets(self): pass

    # ----------------------------------------------------------------------------------
    # FEATURE MAIN FUNCTION
    def setup(self): pass
    def reset(self): pass
    def auto_fire(self): pass      
    def stop_fire(self): pass 
    def transition_system(self): pass
    def firing_sequence(self): pass
    # ----------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------
    # TRANSITION SYSTEM 
    def find_transition_relation(self, marking): pass
    def find_near_marking(self, current_marking): pass 
    # ----------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------
    # FIRING SEQUENCE
    def find_firing_sequence(self, current_marking, sequence): pass
    def find_next_sequence(self, current_marking, sequence): pass

    # ----------------------------------------------------------------------------------
    # HANDLE USER CLICK ON FIRING
    def onClick(self, event): pass 
    def fire_start(self): pass     
    def fire_change(self): pass     
    def fire_end(self): pass
    # ----------------------------------------------------------------------------------
    
    # ----------------------------------------------------------------------------------
    # AUTO FIRE     
    def handle_fire(self): pass          
    def fire(self): pass    
    # ----------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------
    # HELPER FUNCTION
    def check_deadlock(self): pass 
    def is_start_enable(self): pass    
    def is_change_enable(self): pass   
    def is_end_enable(self): pass    
    def handler(self): pass
    # ----------------------------------------------------------------------------------