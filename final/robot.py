import asyncio
import time
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note

def print_pos(robot):
    print('Timestamp: ', time.time(), 'Position: ', robot.pose)

# Initialize the robot
robot = Root(Bluetooth())
speed = 10  # Increase speed to ensure proper movement

# Define the scanning parameters
scan_size = 1  # 1 meter
step_size = 0.1  # 10 cm per step
num_steps = int(scan_size / step_size)
total_cm = 60 
distance = 5
# Asynchronous robot control triggered by the play button
@event(robot.when_play)
async def play(robot):
    # await robot.reset_navigation()
    print_pos(robot)
    with open('position_log.txt', 'w') as file:
        for x in range(0, total_cm, distance):
            for y in range(0, total_cm, distance):
                await robot.navigate_to(x, y)
                for _ in range(5):
                    timestamp = time.time()
                    position = robot.pose
                    print_pos(robot)
                    file.write(f'{timestamp}, {position}\n')
                    await asyncio.sleep(1)
                    
    print("Scanning complete...")

# Start the robot's event system
robot.play()