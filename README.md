# Fibonacci iterator API

## The task

Create a server that will respond to GET requests on http://localhost:8080
with subsequent items in the fibonacci sequence. One at a time. The first
request should return 0, the next 1, the third 1, the fourth 2 etc.

## Assumptions

* Python 3+
* Single process
* Single thread
* Unknown environment specs

## Running the app

Clone this repository

Create a `Python 3` environment with the tools of your choosing, for example the `venv` module

```
 python -mvenv <your_venv_path>
```

Activate it
```
. <your_venv_path>/bin/activate
```

Go to the project dir and install the dependencies 

```
cd <your_project_dir>
pip install -r requirements.txt
```

`(Optional)` Run the test 
```
pytest
```

Start the server
```
uvicorn api.main:app --reload --port 8080
```

Open [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser

`(Optional)` visit the API docs [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)

Enjoy!

## Rationale

### Framework and Server

For the API framework I have used [FastAPI](https://fastapi.tiangolo.com)

The application will be served using [Uvicorn](https://www.uvicorn.org)

Tests are run using [pytest](https://docs.pytest.org/)

---

### Creating the Fibonacci iterator

The default fibonacci iterator implementation uses the known method of storing all of generated numbers in a cache (a list in this case) and the current iteration of the iterator.

The returned result could be described by:

`result[n] = result[n-2] + result[n-1]` where `n` is the current iteration.

Let's implement that as a Python iterator:

```
class RegularFibonacciIterator(object):

     __slots__ = ["__iteration", "__nums"]

    def __init__(self):
        self.__iteration = 0
        self.__nums = [0, 1]

    def __iter__(self):
        return self

    def __next__(self):
        return_value = None
        
        if self.__iteration < 2:
            return_value = self.__iteration, self.__nums
        
        else:
            self.__nums.append(
                self.__nums[self.__iteration - 2] + self.__nums[self.__iteration - 1]
            )
            return_value = self.__nums[-1]
        
        self.__iteration += 1
        
        return return_value

```

[Full code](iterators/regular.py)

Each consecutive call increases the `iteration` and appends the next resulting number to the `nums` var.

But this seems kind of sub-optimal..

---

### ...do we need to store all those numbers? NO.

```
class FibonacciIterator(object):

    __slots__ = ["__first", "__second"]

    def __init__(self):
        self.__first = -1
        self.__second = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.__first == -1:
            self.__first = 0
            return self.__first
        elif self.__second == -1:
            self.__second = 1
            return self.__second
        else:
            self.__first, self.__second = (
                self.__second,
                self.__first + self.__second,
            )  # assign with a shift
            return self.__second

    def _reset(self):
        self.__first = -1
        self.__second = -1
```
[Full code](iterators/optimized.py)

Here we only store `the last two values` from the fibonacci series, and producing the next value during each consecutive call, without keeping track of each iteration. Only the two first calls are special, as we need  to produce the first two values.

---

### Let's compare the above two approaches in terms of memory usage

```
PYTHONPATH=$(pwd) python experiments/run_experiments.py 
```

cProfile for regular fibonacci iterator:
```
PYTHONPATH=$(pwd) python -m cProfile experiments/run_regular_fib.py 
```

cProfile for optimized fibonacci iterator:
```
PYTHONPATH=$(pwd) python -m cProfile experiments/run_fib.py 
```
This command will run 1 000 000 (yes, one million) calls on each of those two iterator and return the total amount of bytes held by the properties.

| iterator   | Result (bytes) | cProfile (s) |
| ----------- | ----------- | ----------- |
| Regular     | 46317041916 | 23.886 |
| Optimized   | 185184      | 12.090 |
| Memory limited   | --      | 15.909 |
| Unified   | --      | 15.676 |

That's `250000x` less memory and almost `2x` faster!

---

### Memory management

In a production environment the system running an app should be properly monitored.

The Fibonacci iterator can run infinitely, as Python does not limit the upper value if `int` and the numbers held in memory will keep growing (although veeeery veeeeery slowly)

Assuming that this app could be run on a tiny pod or a vm tried to implement a very naive memory control.

```
class MemLimitedFibonacciIterator(FibonacciIterator):

    __slots__ = ["__memory_threshold"]

    __memory_threshold = MemoryThreshold()

    def __init__(self, *args, memory_threshold=90, **kwargs):

        current_memory_usage = psutil.virtual_memory().percent
        if current_memory_usage > memory_threshold:
            raise MemoryError("Memory usage over given threshold")

        super().__init__(*args, **kwargs)

        self.__memory_threshold = memory_threshold

    def __next__(self):
        if self._check_limit():
            self._reset()
        return super().__next__()

    def _check_limit(self):
        return psutil.virtual_memory().percent >= self.__memory_threshold

```
[Full code](iterators/memory_limited.py)

This approach uses `psutil` to get the current memory usage, check it before the iteration. Let's check how much slower this approach is than the pure optimized one.

| iterator   | cProfile (s) |
| ----------- | ----------- |
| Optimized   | 12.090 |
| Memory limited | 15.909 |


`25% slower` - could be a good compromise if this would be working in a memory limited environment.

As a bonus check I have created the same iterator but without using inheritance, just to see the result ( ͡° ͜ʖ ͡°) [Full code](iterators/unified.py)

| iterator   | cProfile (s) |
| ----------- | ----------- |
| Memory limited | 15.909 |
| Unified   | 15.676 |

Less than `2%` of an improvement. Negligible as expected.

### Descriptors instead of simple attributes
I have decided to use a descriptor for the memory threshold attribute as it delegates the responsibility of validating the data to a seperate class.

---

## Is the code overengineered?
Yes, but only if we only look at the scope of the task at hand, and not treat it as a potentially production-ready solution.
