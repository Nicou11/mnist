from mnist.worker import prediction, get_job_img_task

def test_prediction():
    r = prediction(file_path='/a/b/c/d.png', num=1)
    assert r in range(10) 

def test_get_job_task():
    r = get_job_img_task()
    assert True
