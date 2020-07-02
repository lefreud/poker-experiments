from trainer.trainer import Trainer
from time import time

start_time = time()
iterations = 1_000_000
t = Trainer()
t.train(iterations=iterations)
print(f"Ran {iterations} iterations")
print(f"Took {time() - start_time} seconds")
