from lamia_chan_web import celery_app

@celery_app.task
def check_new_chapters(*args):
    print(*args)