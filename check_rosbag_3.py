"""
This code is to check rosbag information and output rosbag info to txt file
Author: Zhaoliang Zheng
Email: zhz03@g.ucla.edu
"""
import os
import rospkg
import rosbag
import subprocess

def get_rosbag_info(bag_path):
    info = {}
    
    rospack = rospkg.RosPack()  # Initialize rospack
    
    with rosbag.Bag(bag_path, 'r') as bag:
        info['path'] = os.path.basename(bag_path)
        info['version'] = get_rosbag_version()  # Get rosbag version
        info['duration'] = str(bag.get_end_time() - bag.get_start_time()) + "s"
        info['start'] = str(bag.get_start_time())
        info['end'] = str(bag.get_end_time())
        info['size'] = "{:.2f} GB".format(os.path.getsize(bag_path) / (1024.0 * 1024.0 * 1024.0))
        info['messages'] = sum(1 for _ in bag.read_messages())
        
        topics = {}
        for topic, msg, _ in bag.read_messages():
            if topic not in topics:
                topics[topic] = 1
            else:
                topics[topic] += 1
        info['topics'] = topics
    
    return info

def get_rosbag_version():
    try:
        output = subprocess.check_output(['rosbag', '--version'], stderr=subprocess.STDOUT, universal_newlines=True)
        version_line = output.strip().split('\n')[0]
        version = version_line.split(' ')[-1]
        return version
    except subprocess.CalledProcessError:
        return "Unknown"

def save_info_to_txt(info, output_dir):
    output_path = os.path.join(output_dir, info['path'] + '.txt')
    with open(output_path, 'w') as f:
        f.write(f"path:        {info['path']}\n")
        f.write(f"version:     {info['version']}\n")
        f.write(f"duration:    {info['duration']}\n")
        f.write(f"start:       {info['start']}\n")
        f.write(f"end:         {info['end']}\n")
        f.write(f"size:        {info['size']}\n")
        f.write(f"messages:    {info['messages']}\n")
        
        f.write("topics:\n")
        for topic, count in info['topics'].items():
            f.write(f"  {topic:48} {count} msgs\n")

def main(input_dir, output_dir):
    rospack = rospkg.RosPack()
    
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.bag'):
                bag_path = os.path.join(root, file)
                info = get_rosbag_info(bag_path)
                save_info_to_txt(info, output_dir)

if __name__ == '__main__':
    input_directory = './'  # Input path that includes rosbag output files
    output_directory = './bag_info'   # output txt file path 
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    main(input_directory, output_directory)
