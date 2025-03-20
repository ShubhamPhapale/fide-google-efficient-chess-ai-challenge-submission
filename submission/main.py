%%writefile main1.py
import os
import atexit
import subprocess


if os.path.exists("/kaggle_simulations"):
    engine_file_path = "/kaggle_simulations/agent/berserk4rammin1"
else:
    engine_file_path = "./berserk4rammin1"

class Engine:
    
    def __init__(self, engine_file):
        self.engine_file = engine_file
        self.bestmove = ""
        self.engine_process = None

    def write(self, input_text):
        self.engine_process.stdin.write(input_text)
        self.engine_process.stdin.flush()

    def connect(self):
        self.engine_process = subprocess.Popen([self.engine_file], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                               universal_newlines=True)

    def listen(self):
        while True:
            response = self.engine_process.stdout.readline().strip()
            tokens = response.split()
            if len(tokens) >= 2 and tokens[0] == "bestmove":
                self.bestmove = tokens[1]
                break

    def think(self, allocated_time, fen):
        self.write("uci" + "\n")
        # self.write("setoption name Hash value 0.1" + "\n")
        self.write("position fen " + fen + "\n")
        self.write("go wtime " + str(allocated_time) + " btime " + str(allocated_time) + "\n")

        self.listen()

    def cleanup(self):
        if self.engine_process:
            self.engine_process.kill()
            self.engine_process = None

engine = Engine(engine_file_path)

def cleanup_process():
    global engine
    engine.cleanup()

atexit.register(cleanup_process)
engine.connect()

def main(obs):
    fen = obs.board
    time_left = obs.remainingOverageTime * 1000

    engine.think(time_left, fen)

    return engine.bestmove