import pandas as pd

# Sample log data
logs = [
    "2023-01-01 10:00:00 ERROR Disk space low on /dev/sda1",
    "2023-01-01 10:05:00 WARNING CPU usage exceeded 90%",
    "2023-01-01 10:10:00 INFO Backup completed successfully"
]

# Convert to DataFrame
df = pd.DataFrame([log.split(' ', 3) for log in logs], 
                 columns=['Date', 'Time', 'Level', 'Message'])
print(df)

