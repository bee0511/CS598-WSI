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

csifile = '1207_50cm_floor.dat'
csi_timestamp = '1207_50cm_floor.txt'  # format: packet_id,timestamp
roomba_position = '50x_floor.txt'  # format: timestamp,position

# csifile = '1210_test3.dat'
# csi_timestamp = '1210_test3.txt'  # format: packet_id,timestamp
# roomba_position = '1210_test3_roomba.txt'  # format: timestamp,position

# csifile = '1210_test4.dat'
# csi_timestamp = '1210_test4.txt'  # format: packet_id,timestamp
# roomba_position = '50x_floor_complete.txt'  # format: timestamp,position


csi_data = csiread.Intel(csifile)

# 載入資料
csi_data.read()
csi_matrix = csi_data.get_scaled_csi()  # 獲取 CSI 矩陣

# 計算每個 packet 的訊號強度
signal_strength = np.mean(np.abs(csi_matrix), axis=(1, 2, 3))

# 讀取 timestamp 資料
timestamps = np.loadtxt(csi_timestamp, delimiter=',', usecols=1)

# 篩選訊號強度在 1% 到 99% 範圍內的 packet
lower_bound = np.percentile(signal_strength, 1)
upper_bound = np.percentile(signal_strength, 99)
mask = (signal_strength >= lower_bound) & (signal_strength <= upper_bound)

filtered_timestamps = timestamps[mask]
filtered_signal_strength = signal_strength[mask]

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

unique_positions = np.array(unique_positions)
average_signal_strength = np.array(average_signal_strength)

# 創建6x6的網格
grid_size = 6
heatmap = np.zeros((grid_size, grid_size))

# 將平均訊號強度填入網格
for (x, y), strength in zip(unique_positions, average_signal_strength):
    grid_x = x // 10
    grid_y = y // 10
    if 0 <= grid_x < grid_size and 0 <= grid_y < grid_size:
        heatmap[grid_y, grid_x] = strength

# 繪製熱圖
plt.figure()
plt.imshow(heatmap, cmap='hot', interpolation='nearest', origin='lower')
plt.colorbar(label='Average Signal Strength')
plt.xticks(ticks=np.arange(grid_size), labels=np.arange(0, grid_size * 10, 10))
plt.yticks(ticks=np.arange(grid_size), labels=np.arange(0, grid_size * 10, 10))
plt.xlabel('X Position (cm)')
plt.ylabel('Y Position (cm)')
plt.title('Heatmap of Average Signal Strength')
plt.show()
