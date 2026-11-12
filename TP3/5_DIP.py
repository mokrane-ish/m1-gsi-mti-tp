from abc import ABC, abstractmethod

# --- Part 1: Notification System ---
class NotificationService(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailService(NotificationService):
    def send(self, message):
        print(f"Sending email: {message}")

class SMSService(NotificationService):
    def send(self, message):
        print(f"Sending SMS: {message}")

# Question 1: Add Push Notification Service
class PushService(NotificationService):
    def send(self, message):
        print(f"Sending Push Notification: {message}")

class Notification:
    def __init__(self, service: NotificationService):
        self.service = service

    def send(self, message):
        self.service.send(message)

# --- Part 3 & 4: Refactoring Application & Logger ---
class ILogger(ABC):
    @abstractmethod
    def log(self, message: str):
        pass

class FileLogger(ILogger):
    def log(self, message: str):
        print(f"Logging to file: {message}")

class DatabaseLogger(ILogger):
    def log(self, message: str):
        print(f"Logging to database: {message}")

class Application:
    def __init__(self, logger: ILogger):
        self.logger = logger

    def start(self):
        self.logger.log("Application started")

if __name__ == '__main__':
    print("--- Testing Notification Services ---")
    email_notif = Notification(EmailService())
    sms_notif = Notification(SMSService())
    push_notif = Notification(PushService())

    email_notif.send("Welcome!")
    sms_notif.send("Your OTP is 1234")
    push_notif.send("New message received")

    print("\n--- Testing Application Logger Injection ---")
    app_file = Application(FileLogger())
    app_file.start()

    app_db = Application(DatabaseLogger())
    app_db.start()