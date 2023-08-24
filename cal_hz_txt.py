"""
This code is to calculate the hz of each rostopic in the rosbag info txt file
    and output a new rosbag info txt file with hz information.
Author: Zhaoliang Zheng
Email: zhz03@g.ucla.edu
"""
import os
import re

def process_txt_file(input_path, output_path):
    with open(input_path, 'r') as input_file:
        lines = input_file.readlines()

    duration = None
    rostopics = {}

    for line in lines:
        if "duration:" in line:
            duration = float(re.search(r'duration:\s+([\d.]+)', line).group(1))
            print(duration)
        elif line.startswith("             /") or line.startswith("topics:      /"):
            parts = line.strip().split()
            if parts[0] == 'topics:':
                del parts[0]
            # print(parts)
            topic = parts[0]

            msgs = int(parts[1])
            rostopics[topic] = msgs
            
            # print(rostopics[msgs])

    with open(output_path, 'w') as output_file:
        for line in lines:
            if not (line.startswith("             /") or line.startswith("topics:      /")):
                output_file.write(line)
            if line.startswith("             /") or line.startswith("topics:      /"):
                parts = line.strip().split()
                # print(parts)
                if parts[0] == 'topics:':
                    del parts[0]
                topic = parts[0]
                if topic in rostopics:
                    msgs = rostopics[topic]
                    if duration is not None and duration != 0:
                        hz = round(msgs / duration,3)
                        # print(hz)
                        # new_line = line + "    "+ str(hz) + "  hz"
                        # output_file.write(str(hz))
                        # output_file.write(f"\t{msgs} msgs   {hz:.2f} hz   : {line.split(':', 1)[1]}")
                        # output_file.write(f"{line}  {hz:.2f}   hz\n")
                        output_file.write(f"{line.rstrip()}   {hz:.2f} hz\n")
                    else:
                        # new_line = line + "    N/A hz"
                        # output_file.write("    N/A hz")
                        # output_file.write(f"\t{msgs} msgs   N/A hz   : {line.split(':', 1)[1]}")
                        # output_file.write(f"{line}  N/A   hz\n")
                        output_file.write(f"{line.rstrip()}   N/A hz\n")

        
if __name__ == '__main__':
    input_directory = './rosbag_info_txt'  # input txt path
    output_directory = './rosbag_info_txt'  # output txt path
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for filename in os.listdir(input_directory):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_directory, filename)
            output_filename = 'hz_' + filename
            output_path = os.path.join(output_directory, output_filename)
            process_txt_file(input_path, output_path)
            print(f"Processed {filename} and saved as {output_filename}")

