import asyncio
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Robot, Root

# Initialize the robot
robot = Root(Bluetooth())
speed = 10  # Increase speed to ensure proper movement

# Define the scanning parameters
scan_size = 1  # 1 meter
step_size = 0.1  # 10 cm per step
num_steps = int(scan_size / step_size)

# Asynchronous robot control triggered by the play button
@event(robot.when_play)
async def play(robot):
    for i in range(num_steps):
        # Move forward one step
        await robot.set_wheel_speeds(speed, speed)
        await asyncio.sleep(step_size / speed)
        await robot.set_wheel_speeds(0, 0)
        
        # Turn right at the end of each row
        if i % 2 == 0:
            await robot.turn_right(90)
            await robot.set_wheel_speeds(speed, speed)
            await asyncio.sleep(step_size / speed)
            await robot.set_wheel_speeds(0, 0)
            await robot.turn_right(90)
        else:
            await robot.turn_left(90)
            await robot.set_wheel_speeds(speed, speed)
            await asyncio.sleep(step_size / speed)
            await robot.set_wheel_speeds(0, 0)
            await robot.turn_left(90)

    print("Scanning complete...")

# Start the robot's event system
robot.play()