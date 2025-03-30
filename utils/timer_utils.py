import time
from collections import namedtuple
from IPython.display import display, Markdown

PERF = namedtuple('PERF', ['algo', 'duration'])

timings = []

def timeit(algo, purpose, func, count, items='documents', observer=timings):
  start = time.perf_counter()
  result = func()
  elapsed = time.perf_counter()-start
  observer.append(PERF(algo, elapsed))
  display(Markdown(f'It took ${elapsed/60:.1f}$ minutes to {purpose} for ${count:,d}$ {items}.'))
  return result

