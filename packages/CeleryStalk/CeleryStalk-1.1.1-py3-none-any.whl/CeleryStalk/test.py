from celery import Celery

app = Celery('CeleryStalk123',
             broker='redis://localhost:6379/0',
             backend='redis',
             include=[])


@app.task
def pass_test():
    print("PASS")

def master_run(x,y):
    pass_test.delay()
