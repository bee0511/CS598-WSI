import csiread
import numpy as np
import matplotlib.pyplot as plt
import re

# 讀取 CSI 資料
# csifile = 'static_csi.dat'
csifile = '50cm_1204.dat' 
csi_timestamp = '50cm_1204.txt' # format: packet_id,timestamp 
roomba_position = 'position_log.txt' # format: timestamp,position

csi_data = csiread.Intel(csifile)

# 載入資料
csi_data.read()
csi_matrix = csi_data.get_scaled_csi()  # 獲取 CSI 矩陣

# 計算每個 packet 的訊號強度
signal_strength = np.mean(np.abs(csi_matrix)**2, axis=(1, 2, 3))

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

# 繪製訊號強度與 timestamp 的圖表，並加上位置
plt.figure()
plt.plot(filtered_timestamps, filtered_signal_strength, label='Signal Strength')

annotated_positions = set()
for i, (timestamp, (x, y)) in enumerate(zip(timestamps, positions)):
    pos = (x, y)
    if pos not in annotated_positions:
        plt.annotate(f'({x},{y})', (timestamp, filtered_signal_strength[i]), textcoords="offset points", xytext=(0,10), ha='center')
        plt.plot(timestamp, filtered_signal_strength[i], 'ro')  # 在圖上添加一個點
        annotated_positions.add(pos)

plt.xlabel('Timestamp')
plt.ylabel('Signal Strength')
plt.title('Signal Strength vs Timestamp (1% - 99%)')
plt.legend()
plt.show()

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

# 繪製平均訊號強度與位置的圖表
plt.figure()
plt.plot(range(len(average_signal_strength)), average_signal_strength, label='Average Signal Strength')

for i, (x, y) in enumerate(unique_positions):
    plt.annotate(f'({x},{y})', (i, average_signal_strength[i]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.plot(i, average_signal_strength[i], 'ro')  # 在圖上添加一個點

plt.xlabel('Position Index')
plt.ylabel('Average Signal Strength')
plt.title('Average Signal Strength vs Position')
plt.legend()
plt.show()

# 計算每個位置的訊號強度
unique_positions = []
position_signal_strength = []
current_position = None
current_signals = []

for i, (timestamp, (x, y)) in enumerate(zip(timestamps, positions)):
    pos = (x, y)
    if pos != current_position:
        if current_signals:
            unique_positions.append(current_position)
            position_signal_strength.append(current_signals)
        current_position = pos
        current_signals = [filtered_signal_strength[i]]
    else:
        current_signals.append(filtered_signal_strength[i])

# 添加最後一個位置的訊號強度
if current_signals:
    unique_positions.append(current_position)
    position_signal_strength.append(current_signals)

unique_positions = np.array(unique_positions)

# 繪製每個位置的訊號強度的 box plot
plt.figure()
plt.boxplot(position_signal_strength, labels=[f'({x},{y})' for x, y in unique_positions], vert=True, patch_artist=True)

plt.xlabel('Position')
plt.ylabel('Signal Strength')
plt.title('Signal Strength Distribution by Position')
plt.xticks(rotation=45)
plt.show()