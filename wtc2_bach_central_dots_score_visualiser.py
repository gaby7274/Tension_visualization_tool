#!/usr/bin/env python2
#
# wtc2_central_dots_score_visualiser.py
#
#  Copyright 2014-2022 by Randall E. Cone.  All Rights Reserved.
#
# Score Analysis machine
#
#
import math
from NoteClass import NoteClass
from ScoreParserClass import ScoreParserClass

# Message verbosity level:
#  (0 = none, 1 = note, rest, measure score info only, 2 = fuller score info)
verbose = 1

# What file to store the SVG information for this:
outputfile = 'wtc2_bach_dots_visualisation.svg'


# File containing musicxml information:
inputfiles = [ 
               {'filename': 'musicxml/BWV870-Prelude-Breitkopf-SATB-v2.musicxml',
                'title': 'Prelude',
                'bwv': 'BWV 870',
                'key': 'C Major',
                'colorscheme': 1},
               {'filename': 'musicxml/BWV870-Fugue-Breitkopf-SATB-v2.musicxml',
                'title': 'Fugue',
                'bwv': 'BWV 870',
                'key': 'C Major',
                'colorscheme': 1},
               {'filename': 'musicxml/BWV871-Prelude-Breitkopf-SATB-v2.musicxml',
                'title': 'Prelude',
                'bwv': 'BWV 871',
                'key': 'C Minor',
                'colorscheme': 1},
               {'filename': 'musicxml/BWV871-Fugue-Breitkopf-SATB-v2.musicxml',
                'title': 'Fugue',
                'bwv': 'BWV 871',
                'key': 'C Minor',
                'colorscheme': 1},
               {'filename': 'musicxml/BWV872-Prelude-Breitkopf-SATB-v2.musicxml',
                'title': 'Prelude',
                'bwv': 'BWV 872',
                'key': 'C&#9839; Major',   # sharp symbol
                'colorscheme': 1},
               {'filename': 'musicxml/BWV872-Fugue-Breitkopf-SATB-v2.musicxml',
                'title': 'Fugue',
                'bwv': 'BWV 872',
                'key': 'C&#9839; Major',   # sharp symbol
                'colorscheme': 1},
#               {'filename': 'musicxml/BWV873-Prelude-Breitkopf-SATB-v2.musicxml',
#                'title': 'Prelude',
#                'bwv': 'BWV 873',
#                'key': 'C&#9839; Minor',   # sharp symbol
#                'colorscheme': 1},
#               {'filename': 'musicxml/BWV850-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 850',
#                'key': 'D Major'},
#               {'filename': 'musicxml/BWV850-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 850',
#                'key': 'D Major'},
#               {'filename': 'musicxml/BWV851-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 851',
#                'key': 'D Minor'},
#               {'filename': 'musicxml/BWV851-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 851',
#                'key': 'D Minor'},
#               {'filename': 'musicxml/BWV852-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 852',
#                'key': 'E&#9837; Major'},   # flat symbol
#               {'filename': 'musicxml/BWV852-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 852',
#                'key': 'E&#9837; Major'},   # flat symbol
#               {'filename': 'musicxml/BWV853-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 853',
#                'key': 'E&#9837; Minor'},   # flat symbol
#               {'filename': 'musicxml/BWV853-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 853',
#                'key': 'D&#9839; Minor'},   # sharp symbol
#               {'filename': 'musicxml/BWV854-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 854',
#                'key': 'E Major'},
#               {'filename': 'musicxml/BWV854-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 854',
#                'key': 'E Major'},
#               {'filename': 'musicxml/BWV855-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 855',
#                'key': 'E Minor'},
#               {'filename': 'musicxml/BWV855-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 855',
#                'key': 'E Minor'},
#               {'filename': 'musicxml/BWV856-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 856',
#                'key': 'F Major'},
#               {'filename': 'musicxml/BWV856-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 856',
#                'key': 'F Major'},
#               {'filename': 'musicxml/BWV857-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 857',
#                'key': 'F Minor'},
#               {'filename': 'musicxml/BWV857-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 857',
#                'key': 'F Minor'},
#               {'filename': 'musicxml/BWV858-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 858',
#                'key': 'F&#9839; Major'},
#               {'filename': 'musicxml/BWV858-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 858',
#                'key': 'F&#9839; Major'},
#               {'filename': 'musicxml/BWV859-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 859',
#                'key': 'F&#9839; Minor'},
#               {'filename': 'musicxml/BWV859-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 859',
#                'key': 'F&#9839; Minor'},
#               {'filename': 'musicxml/BWV860-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 860',
#                'key': 'G Major'},
#               {'filename': 'musicxml/BWV860-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 860',
#                'key': 'G Major'},
#               {'filename': 'musicxml/BWV861-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 861',
#                'key': 'G Minor'},
#               {'filename': 'musicxml/BWV861-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 861',
#                'key': 'G Minor'},
#               {'filename': 'musicxml/BWV862-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 862',
#                'key': 'A&#9837; Major'},
#               {'filename': 'musicxml/BWV862-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 862',
#                'key': 'A&#9837; Major'},
#               {'filename': 'musicxml/BWV863-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 863',
#                'key': 'G&#9839; Minor'},
#               {'filename': 'musicxml/BWV863-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 863',
#                'key': 'G&#9839; Minor'},
#               {'filename': 'musicxml/BWV864-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 864',
#                'key': 'A Major'},
#               {'filename': 'musicxml/BWV864-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 864',
#                'key': 'A Major'},
#               {'filename': 'musicxml/BWV865-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 865',
#                'key': 'A Minor'},
#               {'filename': 'musicxml/BWV865-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 865',
#                'key': 'A Minor'},
#               {'filename': 'musicxml/BWV866-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 866',
#                'key': 'B&#9837; Major'},
#               {'filename': 'musicxml/BWV866-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 866',
#                'key': 'B&#9837; Major'},
#               {'filename': 'musicxml/BWV867-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 867',
#                'key': 'B&#9837; Minor'},
#               {'filename': 'musicxml/BWV867-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 867',
#                'key': 'B&#9837; Minor'},
#               {'filename': 'musicxml/BWV868-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 868',
#                'key': 'B Major'},
#               {'filename': 'musicxml/BWV868-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 868',
#                'key': 'B Major'},
#               {'filename': 'musicxml/BWV869-Prelude-Breitkopf-SATB.musicxml',
#                'title': 'Prelude in',
#                'bwv': 'BWV 869',
#                'key': 'B Minor'},
#               {'filename': 'musicxml/BWV869-Fugue-Breitkopf-SATB.musicxml',
#                'title': 'Fugue in',
#                'bwv': 'BWV 869',
#                'key': 'B Minor'},
             ]



###############################3
#  Visualization:
#
    
# Rotate colors:
def rotate(l, n):
    return l[-n:] + l[:-n]

# Color dictionary:          
rest_color = '#AAAAAA'  # grey
#colors = [ 'green', 'blue', 'red', 'yellow', 'orange']
#colors = [ '#36688D', '#F3CD05', '#F49F05', '#F18904', '#BDA589']   # blue/orange sunset
#colors = [ '#A7414A', '#6A8A82', '#A37C27', '#563838', '#BDA589']   # retro
#colors = [ '#6975A6', '#F3E96B', '#F28A30', '#F05837', '#6465A5']   # pastel sunset
#colors = [ '#1D65A6', '#F2A104', '#00743F', '#72A2C0', '#192E5B']   #
#colors = [ '#FFDF14', '#095C03',  '#027EEF', '#CD0000', '#D16007']   # bright

# (4 color, All slightly greyed) Medium blue, yellow, orange, red:
colors4 = [ '#6975A6', '#F3E96B', '#F28A30', '#F03737']   # pastel sunset

# (5 color, All slightly greyed) Medium blue, yellow, orange, red, purple:
colors5 = [ '#6975A6', '#F3E96B', '#F28A30', '#F03737', '#7e37f0']   # pastel sunset 2 w/purple

# (6 color, All slightly greyed) Medium blue, fushia, yellow, orange, red, purple:
colors6 = [ '#6975A6', '#db37f0', '#F3E96B', '#F28A30', '#F03737', '#7e37f0' ]   # pastel sunset 6 color

# Pick basic theme:
poster_theme = 1

# Establish Global Theme:
if (poster_theme == 1):

  # Theme #1:
  #colors = rotate(colors, 0)
  font_size = 24
  font_color = 'white'
  bg_color = 'black'
  signature_image = 'data/jsbach_sig_white.png'

elif (poster_theme == 2):

  # Theme #2:
  #colors = rotate(colors, 0)
  font_size = 24
  font_color = 'black'
  bg_color = 'floralwhite'
  signature_image = 'data/2000px-Johann_Sebastian_Bach_signature.svg_.png'

# Establish Global border color
border_color = font_color

# Initialize starting position for first score:
mainy = 400.0

score_height = 280.0  # Height of a single score
bg_height = score_height * float(len(inputfiles)+1.5) + mainy
bg_width = 6500.0
#bg_width = bg_height/1.618
#bg_width = bg_height * 9.0/16.0
#bg_width = bg_height * 19.0/32.0
#bg_width = bg_height * 5.0/8.0
xmargin = 275.0
border_margin = 30.0
top_margin = border_margin * 1.5   # used for bottom margin too

# Open Output file:
of = open(outputfile,'w')


# Create and write SVG Header:
svg_header_string = ('<svg baseProfile="full" height="' + str(bg_height)+ '"'
                      ' version="1.1" width="' + str(bg_width) + '"'
                      ' xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events"'
                      ' xmlns:xlink="http://www.w3.org/1999/xlink">\n'
                      '<defs>'
                      '\t<filter id="f1"> <feGaussianBlur in="SourceGraphic" stdDeviation="2" /> '
                      '\t</filter>'
                      '</defs>' )

of.write( svg_header_string )

# Create and write BIG Background rectangle:
bg_string = ( '<rect width="100%" height="100%" x="{}"'.format(0)
               +  ' y="{}"'.format(0) + ' style="fill:{};stroke-width:0" />\n'.format(bg_color))

# Border line around outer edge (rectangle): 
bg_string += ( '<rect width="{}"'.format(bg_width - 2.0 * border_margin)
               +  ' height="{}"'.format(bg_height - 2.0 * top_margin)
               + ' x="{}"'.format(border_margin)
               + ' y="{}"'.format(top_margin)
               + ' stroke="{}"'.format(border_color)
               + ' style="fill:None;stroke-width:3" />\n' )

of.write( bg_string )



########
#
# Main title, signature and copyright:
#


# Create Titling:
#title_string = ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Serif"'
#title_string = ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Baskerville"'
#title_string = ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Bodoni MT"'
#title_string = ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Copperplate"'
#title_string = ( '<text xml:space="preserve" fill="' + font_color + '" font-family="fantasy"'
#title_string = ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Hoefler Text"'  # good
#title_string = ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Georgia"'        # okay 

# Main title:
title_string = ( '<text xml:space="preserve" fill="' + str(font_color) + '" font-family="Didot"'         # good'
         + ' font-size="' + str(0.6*mainy) + '" text-anchor="middle"'
         + ' stroke="' + str(font_color) + '" stroke-width="1.0"'
         + ' x="' + str(bg_width/2.0) + '" y="' + str(0.6*mainy + 2.0*top_margin) + '">'
         + 'The Well-Tempered Clavier - Book II' + '</text>\n' )


#  REMOVE temporarily for the printing process, whereby the JS Bach signature png is
#      embedded via Inkscape
#
# JS Bach Signature image:
title_string += ( '<image href="' + str(signature_image) + '" x="' + str(bg_width - 2250 - 2.0*border_margin) + '"'
                  + ' y="' + str(bg_height - 1.5*top_margin - 400) + '"'
                  + '  height="400px" width="2000px"/>\n' )

# Copyright string:
title_string += ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Times"'
                  + ' stroke="' + str(font_color) + '" stroke-width="1.0"'
                  + ' font-size="' + str(font_size) + '" text-anchor="left"' 
                  + ' x="' + str(top_margin) +'" y="' + str(bg_height - 0.8*border_margin) + '">'
                  + '&#169; Copyright 2014-2022  Randall E. Cone.  All Rights Reserved.</text>\n' )

of.write( title_string )



######
#
#  Loop through all input files:


for filedict in inputfiles:
    
    SP = ScoreParserClass( filename=filedict['filename'], verbose=verbose )

    ##
    #
    #   Set up color scheme:
    #
    if (filedict['colorscheme'] == 3):
      colors = colors6
      if (verbose >= 1):
        print('Using six-color scheme: {}'.format(colors6))
    elif (filedict['colorscheme'] == 2):
      colors = colors5
      if (verbose >= 1):
        print('Using five-color scheme: {}'.format(colors))
    else:  # 4-color scheme:
      colors = colors4
      if (verbose >= 1):
        print('Using four-color scheme: {}'.format(colors))

    # Call rotate colors function:          
    colors = rotate(colors, 0)

    ##
    #
    # Get information about this score:
    #
    # (PREPROCESS)
    
    # Preprocess the note width parameters by calculating the duration of each
    #    part, then dividing up a common image width by using this duration:
    # Iterate through each part:
    print(filedict['filename'])
    
    max_part_duration = 0

    if (verbose >= 1):
      print('Number of parts in this piece: {}'.format(len(SP.parts.keys())))
    
    for partkey in SP.parts.keys():
        
        part_duration = 0

        # Iterate through the notes of this part:
        numnotes = len( SP.parts[ partkey ]['notes'])

        for i in range(numnotes):
            note = SP.parts[ partkey ]['notes'][i]
            
            # Check to see if this is a backup or forward (false) note:
            if (note.backup):
                part_duration -= note.duration
                            
            else:
                
                # Careful about grace notes:
                if note.duration:
                    part_duration += note.duration
        
        # Update max_part_duration if new maximum found:        
        if (part_duration > max_part_duration):
            max_part_duration = part_duration
    
        print('Part ' + str(partkey) + ' has duration: ' + str(part_duration ))
        
    if (verbose >= 1):
        print('Maximum part duration: {}'.format(max_part_duration))
           
    # Use the last part to create smallest note width, based on the width of
    #   of the image:
    score_width = bg_width - 2.0 * xmargin
    smallest_note_width = score_width/float(max_part_duration)      
            

    # Set up part colors index:
    pcidx = 0
    
    # Iterate through each part, giving each part a unique color:
    for partkey in reversed(SP.parts.keys()):
    
        # Do work, only if the part is not empty:
        if (not SP.parts[ partkey ][ 'is_empty' ] ):
                                
            ##
            #
            #   Create a purely linear version of the score:
            #
            note_height = score_height/(7.0 * 8.0)  #  3.5 octaves above and below middle C at center of image, 8 notes per octave
            c_line_width = bg_width - 2.0 * xmargin
            c_line_height = 0.2
            center_line_y = mainy + score_height/2.0
            center_piano_note = 39       # 39 is middle C
            
            c_string = ( '<line x1="' + str(xmargin) + '" y1="' + str(center_line_y) + '" '
                         + 'x2="' + str(xmargin+c_line_width) + '" y2="' + str(center_line_y) + '" '
                         + 'stroke="' + font_color + '" '
                         + 'stroke-width="' + str(0.3) + '" '
                         + 'stroke-linecap="round" />\n' )
            
            of.write( c_string )
            
            # Create Left Titling:
            left_string = ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Serif"'
                     + ' stroke="' + str(font_color) + '" stroke-width="1.0"'
                     + ' font-size="' + str(font_size) + '" text-anchor="left"'
                     + ' x="' + str(xmargin/3.0) + '" y="' + str(center_line_y - font_size/2.0) + '">'
                     + filedict['key'] + '</text>\n' )
            left_string += ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Serif"'
                     + ' stroke="' + str(font_color) + '" stroke-width="1.0"'
                     ' font-size="' + str(font_size) + '" text-anchor="center"'
                     ' x="' + str(xmargin/3.0) + '" y="' + str(center_line_y + font_size - 5.0) + '">'
                     + filedict['title'] + '</text>\n' )
            of.write( left_string )

            # Create Right Titling:
            right_string = ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Serif"'
                     + ' stroke="' + str(font_color) + '" stroke-width="1.0"'
                     ' font-size="' + str(font_size) + '" text-anchor="left"'
                     ' x="' + str(xmargin + c_line_width + xmargin*0.25) + '" y="' + str(center_line_y) + '">'
                     + filedict['bwv'] + '</text>\n' )
            of.write( right_string )

            # Set up note_width and pitch for tied notes:
            note_width = 0
            tied_note_number = 0
            
            # For each part, reset the x-coordinate for the first note:
            notex = 0 + xmargin
            
            # Update part color and index:
            part_color = colors[ pcidx ]
            pcidx += 1
                      
            # FOR NOW, we set the y coordinate to start at middle c, in the center of the image:
            centery = center_line_y - note_height/2.0
     
            # Iterate through the notes of this part:
            numnotes = len( SP.parts[ partkey ]['notes'])
            
            for i in range(numnotes):
                
                # Retrieve next note for this part:
                note = SP.parts[ partkey ]['notes'][i]
                
                # Is this the start of a tied note?  If so, in the first
                #  voice of this part, then we keep track of the tied position,
                #  and it's duration:
                
                if ((note.tiestart) and (note.voice == 1)):
                    # Is this a fresh tie or a continued tie?
                    if note.tiestop: # continued tie
                        note_width = note_width + smallest_note_width * note.duration
                        if (verbose >= 2):
                            print("\tOLD tie: {}".format(note_width))
                    
                    else: # fresh tie
                        note_width = smallest_note_width * note.duration
                        tied_note_number = note.piano_note_number
                        if (verbose >= 2):
                            print("\tnew tie: {}".format(note_width))
                
                else:
                
                    # Check to see if this is a backup or forward (false) note:
                    if (note.backup):
                        note_width = smallest_note_width * note.duration
                        notex = notex - note_width
                        
                    elif (note.forward):
                        note_width = smallest_note_width * note.duration
                        notex = notex + note_width
                    
                    #Normal Note:
                    else:                          
                        # Get number of divisions in the measure that contains this note:
                        #mdur = SP.parts[ partkey ]['measure_durations'][ note.measure_number - 1 ]
                        
                        if ((note.tiestop) and (note.voice == 1)):
                            note_width = note_width + smallest_note_width * note.duration
                            
                            # Check that this is really tied to last note:
                            if (note.piano_note_number != tied_note_number):
                                print("\n*****PROBLEM*****\n");
                            
                        #  Establish note width & handle grace notes:
                        elif note.grace:
                            note_width = smallest_note_width    # NOTE: This needs to be made correct
                        else:
                            note_width = smallest_note_width * note.duration
                            
                        # Change output color and position if note or rest is detected:
                        if note.pitch_class:
            
                            # Establish note position in even-temperament, preserving semitone relationships:
                            notey = centery - note_height * (note.piano_note_number - center_piano_note) * 8.0/12.0
                            note_color = part_color
                            note_outline = 'black'

                        else:
                            # Center rests:
                            notey = centery
                            
                            # Default color setting for rest:
                            note_color = 'None'   #note_color = 'gray'
                            note_outline = 'None'
                        
                        #nradius = math.sqrt(note_width)
                        nradius = math.pow(note_width, 0.6)

                        
                        # Center of circle coords:
                        cnx = notex + nradius
                        cny = notey
                        
                        # If note is not the start of a tie, create visualization:
                        note_string = ('<circle cx="' + str(cnx) + '" cy="' + str(cny)
                                       + '" r="' + str(nradius)
                                       + '" stroke="' + note_color
                                       # + '" stroke="' + note_outline
                                       # + '" stroke-width=".2" fill="' + note_color + '"'
                                       + '" stroke-width="1.0" fill="' + note_color + '"'
                                       + ' />')

                        if note.pitch_class:
                          of.write( note_string )
            
                        # Move x-coordinate along, if not a grace note:
                        if (not note.grace):
                            notex = notex + note_width
                
    
    # END of Part loop (exterior)              
    #
    ####

    # Update main y-coordinate (for each score)
    mainy = mainy + score_height           
                    
#### END of FILE LOOP
                
    
###
#
# Create color legend:
#
shape_width = 50
max_word_len = 10
legend_x = 10 + (max_word_len + 1)
legend_y = 10

legend_string = ''

"""
li = 0  # counter
for note in SP.note_palette:  # (they come pre-sorted)
    l_color = note_colors[note]

    # Color box:
    legend_string += ( '<rect x="' + str(legend_x) + '" y="' + str(legend_y + 1.2 * (li-.45) * font_size) + '"'
                       ' width="' + str(shape_width) + '" height="' + str( 0.6 * font_size) + '"'
                       ' stroke="' + l_color + '" fill="' + l_color + '"/>\n' )

    # Color text:
    legend_string += ( '<text xml:space="preserve" fill="' + font_color + '" font-family="Garamond"'
                     ' font-size="' + str(font_size) + '" text-anchor="left"'
                     ' x="' + str(legend_x + shape_width + 10) + '" y="' + str(legend_y + 1.2 * li * font_size ) + '">'
                     + note + '</text>\n' )
    li = li + 1
"""


#of.write( legend_string )
#
###


footer_string = ('</svg>\n')
of.write( footer_string )

# Close SVG file
of.close()



