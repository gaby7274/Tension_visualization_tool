# NoteClass.py
#
# Note class from which to create note objects which contain complete knowledge about a given note.
#
# Copyright 2018-2022 by Randall E. Cone.  All rights reserved.
#

class NoteClass(object):

    def __init__( self ):
	
        self.pitch_class = None
        self.backup = False
        self.forward = False
        self.rest = False
        self.grace = False
        self.tiestart = False
        self.tiestop = False
        self.octave = None
        self.piano_note_number = None
        self.piano_note_name = None
        self.duration = None
        self.type = None
        self.accidental = None
        self.measure_number = None
        self.order_in_measure = None
        self.order_in_part = None
        self.part = None
        self.voice = None
        self.staff = None
        self.x_coordinate = None
        self.y_coordinate = None
        #self.next_note_pitch_class = None
        #self.next_note_piano_name = None
        #self.next_note_piano_number = None
        
        
    # Make this object serializable:
    def __to_json__( self ):
         """
         A function takes in a custom object and returns a dictionary representation of the object.
         This dict representation includes meta data such as the object's module and class names.
         """
         
         #  Populate the dictionary with object meta data 
         obj_dict = {
             "__class__": self.__class__.__name__,
             "__module__": self.__module__
             }
        
         #  Populate the dictionary with object properties
         obj_dict.update(self.__dict__)
         
         return obj_dict
     
        
         
    # Shorter representation    
    def __repr__(self):
        rep = ''
        
        if self.rest:
            rep += 'rest'
        else:
            rep += '{}{}'.format(self.pitch_class, self.octave)
        
        if self.duration:
            rep += ' dur {}'.format(self.duration)
        else:
            rep += ' no duration'
        
        return rep
    
    
    def __str__( self ):
        
        rep = 'This note is:\n'
        
        if self.rest:
            rep += '\ta rest\n'
        elif self.backup:
            rep += '\ta (false) backup note\n'
        elif self.forward:
            rep += '\ta (false) forward note\n'
        else:
            rep += '\tof pitch class: {}\n'.format(self.pitch_class)
            rep += '\tin octave: {}\n'.format(self.octave)
            rep += '\twith piano note number {} and name {}\n'.format(self.piano_note_number, self.piano_note_name)

            
        # Other info:
        if self.duration:
            rep += '\twith duration: {}\n'.format(self.duration)
        else:
            rep += '\twith no duration\n'
            
        # Measure number:
        rep += '\toccurs in measure: {}\n'.format(self.measure_number)
            
        return rep
