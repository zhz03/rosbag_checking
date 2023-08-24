# rosbag checking

## How to use

### check_rosbag.sh

Change the following code:

```
input_directory="./"  # Input directory containing checked rosbag files
output_directory="./rosbag_info_txt"   # Output directory for txt files
```

Then run it:

```shell
chmod +x check_rosbag.sh
./check_rosbag.sh
```

### cal_hz_txt.py

Run the `check_rosbag.sh` first.

The change the following code:

```python
    input_directory = './rosbag_info_txt'  # input txt path
    output_directory = './rosbag_info_txt'  # output txt path
```

