import psutil
import subprocess
import time

# Function to get memory usage of a specific process
def get_memory_usage(process):
    try:
        mem_info = process.memory_info()
        return mem_info.rss / (1024 * 1024)  # Convert to MB
    except psutil.NoSuchProcess:
        return 0

# Function to monitor a UCI engine
def monitor_uci_engine(engine_path, commands):
    # Start the UCI engine as a subprocess
    process = subprocess.Popen(
        engine_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    p = psutil.Process(process.pid)
    
    try:
        # Send commands to the UCI engine
        for command in commands:
            process.stdin.write(f"{command}\n")
            process.stdin.flush()
            time.sleep(1)  # Allow some time for processing
            
            # Measure memory usage
            memory_usage = get_memory_usage(p)
            print(f"Memory Usage after '{command}': {memory_usage:.2f} MB")
        
        # Wait for a while to observe idle memory usage
        time.sleep(5)
        idle_memory = get_memory_usage(p)
        print(f"Idle Memory Usage: {idle_memory:.2f} MB")
    
    finally:
        # Terminate the process
        process.stdin.write("quit\n")
        process.stdin.flush()
        process.terminate()
        process.wait()

# Path to your UCI engine executable (adjust as needed)
uci_engine_path = f"/kaggle/working/Ethereal12.5"

# List of commands to send to the engine
uci_commands = [
    "uci",
    "isready", 
    # "setoption name Hash value 0.4",  # Set hash table to 1 MB
    "position startpos moves a2a4 a7a5 e2e4 e7e5 b1c3 b8c6 f1c4 f8c5",
    # "go wtime 10000 wtime 10000"
    "go depth 20"
]

monitor_uci_engine(uci_engine_path, uci_commands)