#! /usr/bin/env python
# -*- Python -*-
###########################################################################
#                       Trace Analizer Example                            #
#                        --------------------                             #
#  copyright         (C) 2008  Giuseppe "denever" Martino                 #
#  email                : denever@users.sf.net                            #
###########################################################################
###########################################################################
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program; if not, write to the Free Software            #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA#
#                                                                         #
###########################################################################

import sys
from myprintfparser import MyTraceParser
from decimal import * # using decimal for decimal precision

if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_file = open(sys.argv[1], 'r') # apre il file in read
    else:
        print "usage tracana.py input_file"
        sys.exit(1)
    
    parser = MyTraceParser(input_file)

    ul_map = parser.get_ss_ulmap() # This gets UpLink Map from file in MyPrintf format
    bursts = parser.get_sent_bursts() # This gets bursts (start,stop) of trasmission from a file in MyPrintf format
    ulsubframe_start_times = parser.get_ulsubframe_start_times() # This gets start times of UpLink Sub Frame

    nodes = bursts.keys()
    nodes_map = ul_map.keys()
    nodes_map.sort()
    nodes.sort()

    # This compares UpLink Map and transmission burts for each UpLink Subframe    
    for frameno, frame_start in enumerate(ulsubframe_start_times):
        print "UpLink SubFrame number:",frameno, "Start:",frame_start
        for nodeid in nodes_map:
            if nodeid != '0':
                (start, duration) = bursts[nodeid][frameno]
                (ul_start, ul_duration) = ul_map[nodeid][frameno]

                insubframe_start = Decimal(start) - Decimal(frame_start)
                
                if insubframe_start != Decimal(ul_start):
                    print "Node id:", nodeid, "In SubFrame start:",insubframe_start, "Ul_start:", ul_start
                if duration != Decimal(ul_duration):
                    print "Node id:", nodeid, "Duration:",duration, "Ul_Duration:", ul_duration
