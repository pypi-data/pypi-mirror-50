cron-lock
========

Features
--------
- 计数锁，根据指定的时间恢复次数.
- 无需额外依赖.
- 支持python2、python3

Usage
-----

.. code-block:: bash

    $ pip install cron-lock

.. code-block:: python3
    
    import threading
    from cron_lock import CountLock

    def job():
        lock.acquire()  # 获取锁，不用release
        print("I'm working...")
    
    lock = CountLock(count=60, seconds=second_test) # 初始化锁，支持'seconds, minutes'
    
    # 执行线程
    thread_pool = []
    for i in range(60):
        thread_obj = threading.Thread(target=job)
        thread_obj.start()
        thread_pool.append(thread_obj)
    for i in thread_pool:
        i.join()