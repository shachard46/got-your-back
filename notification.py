import platform
os = platform.system()

if os == 'Darwin':
    import notify2
else:
    from win10toast import ToastNotifier


class Notification:
    def __init__(self, title, message) -> None:
        self.title = title
        self.message = message
        self.is_mac = os == 'Darwin'

    def set_message(self, message):
        self.message = message

    def notify(self):
        if self.is_mac:
            notify2.init("Got Your Back")
            notification = notify2.Notification(self.title, self.message)
            notification.set_timeout(2000)
            notification.show()
        else:
            toaster = ToastNotifier()
            toaster.show_toast(self.title, self.message, duration=10)
