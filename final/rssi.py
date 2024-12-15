import csiread
import numpy as np
import matplotlib.pyplot as plt
import re
import seaborn as sns

# 讀取 CSI 資料
# static_csifile = '1210_test1.dat'
static_csifile = '1210_test2.dat'

csifile = '1207_50cm.dat'
csi_timestamp = '1207_50cm.txt'  # format: packet_id,timestamp
roomba_position = 'position_log_1207.txt'  # format: timestamp,position

# csifile = '1207_50cm_test2.dat'
csi_timestamp = '1207_50cm_test2.txt'  # format: packet_id,timestamp
roomba_position = '50x_1207.txt'  # format: timestamp,position

# csifile = '1207_50cm_floor.dat'
# csi_timestamp = '1207_50cm_floor.txt'  # format: packet_id,timestamp
# roomba_position = '50x_floor.txt'  # format: timestamp,position

# csifile = '1210_test3.dat'
# csi_timestamp = '1210_test3.txt'  # format: packet_id,timestamp
# roomba_position = '1210_test3_roomba.txt'  # format: timestamp,position

csifile = '1210_test4.dat'
# csi_timestamp = '1210_test4.txt'  # format: packet_id,timestamp
# roomba_position = '50x_floor_complete.txt'  # format: timestamp,position

csi_data = csiread.Intel(csifile)
# csi_data = csiread.Intel(static_csifile)

# # 載入資料
csi_data.read()
# csi_matrix = csi_data.apply_sm(csi_matrix)
rssi_a = csi_data.rssi_a
rssi_b = csi_data.rssi_b
rssi_c = csi_data.rssi_c
# Plot signal strength over time
plt.figure()
plt.plot(rssi_a, label='RSSI_A')
plt.plot(rssi_b, label='RSSI_B')
plt.plot(rssi_c, label='RSSI_C')
plt.xlabel('Packet Index')
plt.ylabel('Signal Strength')
plt.title('Signal Strength over Time')
plt.legend(loc='lower right')
plt.show()