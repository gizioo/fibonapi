from fastapi import FastAPI
from iterators import MemLimitedFibonacciIterator
from .models import ResponseModel

app = FastAPI()
fib = MemLimitedFibonacciIterator()


@app.get("/", response_model=ResponseModel)
def get_next_fib():
    next_fib = next(fib)
    return {"result": next_fib}
