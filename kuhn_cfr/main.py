from trainer import Trainer


iterations = 1_000_000
t = Trainer()
t.train(iterations=iterations)
print(f"Ran {iterations} iterations")
