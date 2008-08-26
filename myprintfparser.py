#! /usr/bin/env python
# -*- Python -*-
###########################################################################
#                           NS2NewTraceParser                             #
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

import re
import sys
from decimal import *

find_ss_sending = re.compile("^MacSS::send - Sending -")
find_ss_ulmap = re.compile("^MacSS::recvUL_MAP - UL_MAP: ")
find_bs_ulmap = re.compile("^MacBS::sendUL_MAP - UL_MAP: ")
find_frame_start = re.compile("^MacBS::FrameHandler -")
find_ulsubframe_start = re.compile("^MacBS::HandlerUL -")
find_sstxof_handler = re.compile("^MacSS::ToHandler -")
find_sswait_handler = re.compile("^MacSS::SsWaitHandler -")
find_sphandler = re.compile("^MacSS::SPHandler -")

get_node_id = re.compile("NodeId: (\d+),")
get_event_time = re.compile("Time: ([0-9.]*)")
get_start_time = re.compile("start: ([0-9.]*)",)
get_duration = re.compile("Duration: ([0-9.]*)")
get_shortpreamble = re.compile("ShortPreamble: ([0-9.]*)")

class MyTraceParser:
    def __init__(self, input_file):
        self.input_lines = input_file.readlines()
    
    def old_get_sent_bursts(self):
        last_node_id = str(0)
        last_time = str(0)        
        burst_times = {}
        
        for line in self.input_lines:
            ss_sending_found = find_ss_sending.search(line)
            node_id_found = get_node_id.search(line)
            event_time_found = get_event_time.search(line)
            
            if ss_sending_found != None and node_id_found != None and event_time_found != None:
                new_node_id = node_id_found.group(1)
                new_time = event_time_found.group(1)

                if new_node_id != last_node_id:
                    if not burst_times.has_key(last_node_id):
                        burst_times[last_node_id] = []

                    burst_times[last_node_id].append((last_time, new_time))

                    last_node_id = new_node_id
                    last_time = new_time
            
        return burst_times

    def get_sent_bursts(self):
        current_node_id = 'NoNode'
        current_time = Decimal('0.000000')
        short_preamble = Decimal('0.000000')
        total_duration = Decimal('0.000000')
        burst_times = {}
        
        for line in self.input_lines:
            ss_sending_found = find_ss_sending.search(line)
            sswait_handler_found = find_sswait_handler.search(line)
            sphandler_found = find_sphandler.search(line)
            
            node_id_found = get_node_id.search(line)
            event_time_found = get_event_time.search(line)
            duration_found = get_duration.search(line)
            shortpreamble_found = get_shortpreamble.search(line)
            
            if sswait_handler_found and node_id_found and event_time_found:
                new_node_id = node_id_found.group(1)

                if current_node_id == 'NoNode':
                    current_node_id = new_node_id
                    current_time = Decimal(event_time_found.group(1))
                    continue
                
                if new_node_id != current_node_id:
                    if not burst_times.has_key(current_node_id):
                        burst_times[current_node_id] = []

                    burst_times[current_node_id].append((current_time,total_duration))

                    current_node_id = new_node_id
                    current_time = Decimal(event_time_found.group(1))
                continue

            if sphandler_found and node_id_found and shortpreamble_found:
                if node_id_found.group(1) == current_node_id:
                    short_preamble = Decimal(shortpreamble_found.group(1))
                    total_duration = short_preamble
                continue
            
            if ss_sending_found and node_id_found and event_time_found and duration_found:
                new_node_id = node_id_found.group(1)
                new_time = event_time_found.group(1)
                duration = Decimal(duration_found.group(1))

                if new_node_id == current_node_id:
                    total_duration = total_duration + duration

                continue
            
        return burst_times

    
    def get_ss_ulmap(self):
        ulmap = {}
        
        for line in self.input_lines:
            ulmap_found = find_ss_ulmap.search(line)
            node_id_found = get_node_id.search(line)
            start_time_found = get_start_time.search(line)
            duration_found = get_duration.search(line)
            
            if not ulmap_found == None and not start_time_found == None and not duration_found == None:
                node_id = node_id_found.group(1)
                start_time = start_time_found.group(1)
                duration = duration_found.group(1)
                
                if not ulmap.has_key(node_id):
                    ulmap[node_id] = []

                ulmap[node_id].append((start_time,duration))
                
        return ulmap

    def get_bs_ulmap(self):
        ulmap = {}
        
        for line in self.input_lines:
            ulmap_found = find_bs_ulmap.search(line)
            node_id_found = get_node_id.search(line)
            start_time_found = get_start_time.search(line)
            duration_found = get_duration.search(line)
            
            if not ulmap_found == None and not start_time_found == None and not duration_found == None:
                node_id = node_id_found.group(1)
                start_time = start_time_found.group(1)
                duration = duration_found.group(1)
                
                if not ulmap.has_key(node_id):
                    ulmap[node_id] = []

                ulmap[node_id].append((start_time,duration))
                
        return ulmap

    def get_frame_start_times(self):
        frame_start_times = []
        for line in self.input_lines:
            frame_start_found = find_frame_start.search(line)
            if frame_start_found:
                time_found = get_event_time.search(line)
                if time_found:
                    frame_start_times.append(time_found.group(1))
        return frame_start_times

    def get_ulsubframe_start_times(self):
        ulsubframe_start_times = []
        for line in self.input_lines:
            ulsubframe_start_found = find_ulsubframe_start.search(line)
            if ulsubframe_start_found:
                time_found = get_event_time.search(line)
                if time_found:
                    ulsubframe_start_times.append(time_found.group(1))
        return ulsubframe_start_times

    def get_ss_txoff_times(self):
        txoff_times = {}
        for line in self.input_lines:
            txoff_handler_found = find_sstxof_handler.search(line)
            node_id_found = get_node_id.search(line)
            event_time_found = get_event_time.search(line)

            if txoff_handler_found and node_id_found and event_time_found:
                node_id = node_id_found.group(1)
                if not txoff_times.has_key(node_id):
                    txoff_times[node_id] = []
                    
                txoff_times[node_id].append(event_time_found.group(1))
        return txoff_times
