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
from myparser import MyTraceParser

if __name__ == '__main__':
    if len(sys.argv) == 3:
        input_file = open(sys.argv[1], 'r') # apre il file in read
        input_file2 = open(sys.argv[2], 'r')
    else:
        print "usage tracana.py input_file"
        sys.exit(1)
    
    parser1 = MyTraceParser(input_file)
    parser2 = MyTraceParser(input_file2)    

    bs_ul_map = parser1.get_bs_ulmap()
    ss_ul_map = parser2.get_ss_ulmap()

    for node_id in bs_ul_map.keys():
        
        for bs_slot in bs_ul_map[node_id]:
            ss_slot = ss_ul_map[node_id].pop()
        
            if bs_slot != ss_slot:
                print 'Slot differ',node_id,bs_slot,ss_slot
            if bs_slot == ss_slot:
                print 'Slot ok',node_id,bs_slot,ss_slot
