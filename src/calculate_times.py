from datetime import timedelta

class CalculateTimes:
    def __init__(self, list_with_rest, list_without_rest):
        # Input: two lists of activities with time strings (with and without rest)
        self.list_with_rest = list_with_rest
        self.list_without_rest = list_without_rest

    def calcualte_rest_times(self):
        # Calculates activity times with and without rest (returns lists)
        
        # Convert initial list to dictionaries
        time_with_rest_dict = self.convert_list_to_dict(self.list_with_rest)
        # Split long tasks (>= 5 hours) into smaller chunks
        time_with_rest_dict = self.split_long_tasks(time_with_rest_dict)
        # Add appropriate rest times
        time_with_rest_dict = self.add_rest_times(time_with_rest_dict)


        # Do the same for the list without rest
        time_without_rest_dict = self.convert_list_to_dict(self.list_without_rest)
        time_without_rest_dict = self.add_rest_times(time_without_rest_dict, has_rest=False)


        # Convert back to list format
        time_with_rest_dict = self.convert_dict_to_list(time_with_rest_dict)
        time_without_rest_dict = self.convert_dict_to_list(time_without_rest_dict)
    
        return time_with_rest_dict, time_without_rest_dict

    def calculate_total_times(self):
        # Calculates total time (in seconds) with and without rest
        total_with_rest_seconds = 0
        total_without_rest_seconds = 0

        # Convert and process list with rest
        time_with_rest_dict = self.convert_list_to_dict(self.list_with_rest)
        time_with_rest_dict = self.split_long_tasks(time_with_rest_dict)
        time_with_rest_dict = self.add_rest_times(time_with_rest_dict)


        # Convert and process list without rest
        time_without_rest_dict = self.convert_list_to_dict(self.list_without_rest)
        time_without_rest_dict = self.add_rest_times(time_without_rest_dict, has_rest=False)


        # Sum time with rest
        for item in time_with_rest_dict:
            for i in item['time_with_rest']:
                total_with_rest_seconds += i.seconds

        # Sum time without rest
        for item in time_without_rest_dict:
            total_without_rest_seconds += item['time'].seconds

        return total_with_rest_seconds, total_without_rest_seconds

    def split_long_tasks(self, time_dict):
        # Splits tasks longer than or equal to 5 hours into 4-hour chunks
        new_time_dict = []
        for item in time_dict:
            if item['time'] >= timedelta(hours=5):
                # Split into 4-hour chunks
                remaining_time = item['time']
                while remaining_time > timedelta(hours=0):
                    chunk = min(remaining_time, timedelta(hours=4))
                    new_time_dict.append({
                        'name': item['name'],
                        'time': chunk
                    })
                    remaining_time -= chunk
            else:
                new_time_dict.append(item)
        return new_time_dict

    def timestr_spliter(self, timestr):
        # Converts time string "hh:mm" into a timedelta object
        try:
            if not timestr or ':' not in timestr:
                raise ValueError("Invalid time format")
                
            time_parts = timestr.split(':')
            if len(time_parts) != 2:
                raise ValueError("Time should be in hh:mm format")
                
            hours = time_parts[0].strip()
            minutes = time_parts[1].strip()
            
            if not hours or not minutes:
                raise ValueError("Hours and minutes cannot be empty")
                
            return timedelta(hours=int(hours), minutes=int(minutes))
        except ValueError as e:
            raise ValueError(f"Invalid time format '{timestr}'. Please use hh:mm format. Error: {str(e)}")

    def convert_list_to_dict(self, times_list):
        # Converts list of [name, time_str] into list of dictionaries with 'name' and 'time' as timedelta
        valid_items = []
        for v in times_list:
            try:
                if not v[0].strip() or not v[1].strip():
                    continue
                time_delta = self.timestr_spliter(v[1])
                valid_items.append({'name': v[0], 'time': time_delta})
            except ValueError as e:
                print(f"Skipping invalid activity '{v[0]}' with time '{v[1]}': {str(e)}")
                continue
                
        return valid_items
    
    def convert_dict_to_list(self, times_dict):
        # Converts processed dicts (with rest times) back into list format
        final_list = []
        for item in times_dict:
            total_time = timedelta(hours=0, minutes=0)
            time_with_rest = ""
            for i in item['time_with_rest']:
                time_with_rest += str(i) + '\n'
                total_time += i
            final_list.append([item['name'], time_with_rest.strip(), str(total_time)])

        return final_list

    def add_rest_times(self, time_dict, has_rest=True):
        # Adds rest times based on task duration
        if not has_rest:
            for item in time_dict:
                item['time_with_rest'] = [item['time']]
        else:        
            for item in time_dict:
                if item['time'] < timedelta(hours=0, minutes=30):
                    item['time_with_rest'] = [item['time'],
                                            timedelta(hours=0, minutes=5),]
                elif item['time'] < timedelta(hours=2, minutes=0):
                    item['time_with_rest'] = [item['time'], 
                                            timedelta(hours=0, minutes=10)]
                elif item['time'] <= timedelta(hours=3, minutes=0, seconds=0):
                    mid_time = item['time']/2
                    if int(str(item['time']).split(':')[1]) % 2 == 0:
                        item['time_with_rest'] = [mid_time, 
                                                timedelta(hours=0, minutes=10),
                                                mid_time, 
                                                timedelta(hours=0, minutes=15)]
                    else:
                        item['time_with_rest'] = [mid_time + timedelta(seconds=30),
                                                timedelta(hours=0, minutes=10), 
                                                mid_time - timedelta(seconds=30), 
                                                timedelta(hours=0, minutes=15)]
                elif item['time'] < timedelta(hours=5, minutes=0):
                    time1 = item['time']-timedelta(hours=1, minutes=0, seconds=0)
                    mid_time = time1/2
                    if int(str(time1).split(':')[1]) % 2 == 0:
                        item['time_with_rest'] = [timedelta(hours=1, minutes=0), 
                                                timedelta(hours=0, minutes=10), 
                                                mid_time,
                                                timedelta(hours=0, minutes=10), 
                                                mid_time,
                                                timedelta(hours=0, minutes=20)]
                    else:
                        item['time_with_rest'] = [timedelta(hours=1, minutes=0),
                                                timedelta(hours=0, minutes=10),
                                                time1 - mid_time + timedelta(seconds=30),
                                                timedelta(hours=0, minutes=10),
                                                mid_time - timedelta(seconds=30),
                                                timedelta(hours=0, minutes=20)]
        return time_dict