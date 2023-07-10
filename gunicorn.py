workers = 2
keepalive = 180
timeout = 180
threads = 2

bind = '0.0.0.0:9246'
worker_class = 'uvicorn.workers.UvicornWorker'