import time
class Brandywine:
    
    def __init__(self, duration=25, break_duration=5):
        self.duration = int(duration)
        self.break_duration = int(break_duration)
        self.run()
    
    def notify(self, message):
        print(message)
        
    def run(self):
        choice = "yes I wanna be a busy bee"
        while choice != "n":
            self.countdown(self.duration*60)
            self.notify("Pomodoro finished, time for a break!")
            self.countdown(self.break_duration*60)
            self.notify("Your break is over -- time to zone back in again!")
            choice = input("Start another pomodoro? (Y/n)").strip()
        print("Goodbye!")
        
    def countdown(self, seconds):
        for i in range(0, seconds):
            print(time.strftime('%H:%M:%S', time.gmtime(seconds-i)), end = '\r')
            time.sleep(1)
        return None