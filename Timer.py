import time
import datetime

class Timer:
    #Initiate the timer.
    #onDone indicates is a function that should be called when the time runs out
    def __init__(self, onDone):
        self.onDone = onDone
        
        self.startTime = 0
        self.duration = 0
        self.counting = False

    def start(self, duration):
        self.duration = duration
        self.counting = True
        self.startTime = time.time()

    def pause(self):
        self.counting = False

    def resume(self):
        self.counting = True

    def update(self):
        if self.counting:
            if time.time() - self.startTime > self.duration:
                self.onDone()
                self.counting = False
                self.duration = 0

    def getTimeLeft(self):
        secondsLeft = self.duration - (time.time() - self.startTime)
        
        timeLeft = datetime.timedelta(seconds=secondsLeft)

        return timeLeft


