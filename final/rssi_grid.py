import csiread
import numpy as np
import matplotlib.pyplot as plt
import re

# 讀取 CSI 資料
static_csifile = '1210_test1.dat'

csifile = '1207_50cm.dat'
csi_timestamp = '1207_50cm.txt'  # format: packet_id,timestamp
roomba_position = 'position_log_1207.txt'  # format: timestamp,position

csifile = '1207_50cm_test2.dat'
csi_timestamp = '1207_50cm_test2.txt'  # format: packet_id,timestamp
roomba_position = '50x_1207.txt'  # format: timestamp,position

# csifile = '1207_50cm_floor.dat'
# csi_timestamp = '1207_50cm_floor.txt'  # format: packet_id,timestamp
# roomba_position = '50x_floor.txt'  # format: timestamp,position

# csifile = '1210_test3.dat'
# csi_timestamp = '1210_test3.txt'  # format: packet_id,timestamp
# roomba_position = '1210_test3_roomba.txt'  # format: timestamp,position

# csifile = '1210_test4.dat'
# csi_timestamp = '1210_test4.txt'  # format: packet_id,timestamp
# roomba_position = '50x_floor_complete.txt'  # format: timestamp,position


csi_data = csiread.Intel(csifile)

# 載入資料
csi_data.read()
rssi_a = csi_data.rssi_a
rssi_b = csi_data.rssi_b
rssi_c = csi_data.rssi_c

# 計算每個 packet 的訊號強度
signal_strength_a = rssi_a
signal_strength_b = rssi_b
signal_strength_c = rssi_c

# 讀取 timestamp 資料
timestamps = np.loadtxt(csi_timestamp, delimiter=',', usecols=1)

# 篩選訊號強度在 1% 到 99% 範圍內的 packet
lower_bound_a = np.percentile(signal_strength_a, 1)
upper_bound_a = np.percentile(signal_strength_a, 99)
mask_a = (signal_strength_a >= lower_bound_a) & (signal_strength_a <= upper_bound_a)

lower_bound_b = np.percentile(signal_strength_b, 1)
upper_bound_b = np.percentile(signal_strength_b, 99)
mask_b = (signal_strength_b >= lower_bound_b) & (signal_strength_b <= upper_bound_b)

lower_bound_c = np.percentile(signal_strength_c, 1)
upper_bound_c = np.percentile(signal_strength_c, 99)
mask_c = (signal_strength_c >= lower_bound_c) & (signal_strength_c <= upper_bound_c)

filtered_timestamps_a = timestamps[mask_a]
filtered_signal_strength_a = signal_strength_a[mask_a]

filtered_timestamps_b = timestamps[mask_b]
filtered_signal_strength_b = signal_strength_b[mask_b]

filtered_timestamps_c = timestamps[mask_c]
filtered_signal_strength_c = signal_strength_c[mask_c]

# 讀取 Roomba 位置資料
with open(roomba_position, 'r') as f:
    lines = f.readlines()

# 解析位置資料，只記錄 x 和 y，並去除小數點
positions = []
timestamps = []
pattern = re.compile(r'Pose \(([^,]+), ([^,]+),')
for line in lines:
    timestamp, pos = line.split(',', 1)
    match = pattern.search(pos)
    if match:
        x, y = match.groups()
        positions.append((int(float(x)), int(float(y))))
        timestamps.append(float(timestamp))
positions = np.array(positions)
# print(positions)
timestamps = np.array(timestamps)


# 計算每個位置的平均訊號強度
def calculate_average_signal_strength(filtered_signal_strength):
    unique_positions = []
    average_signal_strength = []
    current_position = None
    current_signals = []

    for i, (timestamp, (x, y)) in enumerate(zip(timestamps, positions)):
        pos = (x, y)
        if pos != current_position:
            if current_signals:
                unique_positions.append(current_position)
                average_signal_strength.append(np.mean(current_signals))
            current_position = pos
            current_signals = [filtered_signal_strength[i]]
        else:
            current_signals.append(filtered_signal_strength[i])

    # 添加最後一個位置的平均訊號強度
    if current_signals:
        unique_positions.append(current_position)
        average_signal_strength.append(np.mean(current_signals))

    return np.array(unique_positions), np.array(average_signal_strength)

unique_positions_a, average_signal_strength_a = calculate_average_signal_strength(filtered_signal_strength_a)
unique_positions_b, average_signal_strength_b = calculate_average_signal_strength(filtered_signal_strength_b)
unique_positions_c, average_signal_strength_c = calculate_average_signal_strength(filtered_signal_strength_c)

# 創建6x6的網格
grid_size = 6
heatmap_a = np.zeros((grid_size, grid_size))
heatmap_b = np.zeros((grid_size, grid_size))
heatmap_c = np.zeros((grid_size, grid_size))

# 將平均訊號強度填入網格
def fill_heatmap(heatmap, unique_positions, average_signal_strength):
    for (x, y), strength in zip(unique_positions, average_signal_strength):
        grid_x = x // 10
        grid_y = y // 10
        if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
            heatmap[grid_y, grid_x] = strength

fill_heatmap(heatmap_a, unique_positions_a, average_signal_strength_a)
fill_heatmap(heatmap_b, unique_positions_b, average_signal_strength_b)
fill_heatmap(heatmap_c, unique_positions_c, average_signal_strength_c)

# 繪製熱圖
plt.figure()
plt.subplot(1, 3, 1)
plt.imshow(heatmap_a, cmap='hot', interpolation='nearest', origin='lower')
cbar = plt.colorbar(label='dB', shrink=0.3)  # 縮小 color bar
plt.xticks(ticks=np.arange(grid_size), labels=np.arange(0, grid_size * 10, 10))
plt.yticks(ticks=np.arange(grid_size), labels=np.arange(0, grid_size * 10, 10))
plt.xlabel('X Position (cm)')
plt.ylabel('Y Position (cm)')
plt.title('RSSI_A')

plt.subplot(1, 3, 2)
plt.imshow(heatmap_b, cmap='hot', interpolation='nearest', origin='lower')
cbar = plt.colorbar(label='dB', shrink=0.3)  # 縮小 color bar
plt.xticks(ticks=np.arange(grid_size), labels=np.arange(0, grid_size * 10, 10))
plt.yticks(ticks=np.arange(grid_size), labels=np.arange(0, grid_size * 10, 10))
plt.xlabel('X Position (cm)')
plt.ylabel('Y Position (cm)')
plt.title('RSSI_B')

plt.subplot(1, 3, 3)
plt.imshow(heatmap_c, cmap='hot', interpolation='nearest', origin='lower')
cbar = plt.colorbar(label='dB', shrink=0.3)  # 縮小 color bar
plt.xticks(ticks=np.arange(grid_size), labels=np.arange(0, grid_size * 10, 10))
plt.yticks(ticks=np.arange(grid_size), labels=np.arange(0, grid_size * 10, 10))
plt.xlabel('X Position (cm)')
plt.ylabel('Y Position (cm)')
plt.title('RSSI_C')

plt.tight_layout()
plt.show()
