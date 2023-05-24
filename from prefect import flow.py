from prefect import flow

@flow
def foo():
    print("Hello world")

foo()