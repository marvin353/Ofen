import _thread
import time
import threading

"""
# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while True:
      time.sleep(delay)
      count += 1
      print ("ID:" + str(threading.get_ident()) + "%s: %s" % ( threadName, time.ctime(time.time()) ))

def print_time2( threadName, delay):
   count = 0
   while True:
      time.sleep(delay)
      count += 1
      print ("ID:" + str(threading.get_ident()) + "%s: %s" % ( threadName, time.ctime(time.time()) ))

# Create two threads as follows
try:
   _thread.start_new_thread( print_time, ("Thread-1", 1, ) )
   _thread.start_new_thread( print_time2, ("Thread-2", 1, ) )
except:
   print ("Error: unable to start thread")

while 1:
   pass
   """


class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.t1r, args=(["text2test"]))
        thread.daemon = False                            # Daemonize thread
        thread.start()                                  # Start the execution

        thread2 = threading.Thread(target=self.t2r, args=())
        thread2.daemon = False  # Daemonize thread
        thread2.start()

    def runn(self):
        """ Method that runs forever """
        while True:
            print("While1:" + str(threading.get_ident()))
            time.sleep(self.interval)

    def t1r(self,text):
        i = 0
        while True:
            print("i: " + str(i) + "; hallo while1:" + str(threading.get_ident()) + text)
            i += 1
            if (i >= 5):
                # self.sample_job_every_1s()
                break
            time.sleep(1)

    def t2r(self):
        i = 0
        while True:
            print("i: " + str(i) + "; hallo while2:" + str(threading.get_ident()))
            i += 1
            if (i >= 5):
                # self.sample_job_every_1s()
                break
            time.sleep(1)


example = ThreadingExample()
time.sleep(3)
print('Checkpoint')
time.sleep(2)
print('Bye')