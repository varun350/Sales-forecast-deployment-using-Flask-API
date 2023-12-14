"""
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

start = 50
end = 100

print(f"Prime numbers between {start} and {end}:")
for num in range(start, end + 1):
    if is_prime(num):
        print(num)

"""       
"""
import datetime
import time

# Get the current time
start_time = datetime.datetime.now()

# Calculate the end time after 24 hours
end_time = start_time + datetime.timedelta(hours=4)

# Print continuously until the end time is reached
while datetime.datetime.now() < end_time:
    current_time = datetime.datetime.now()
    print(f"Current time: {current_time}")

    # Delay for 1 second before the next print
    time.sleep(1)

"""

print("hello world........!")

