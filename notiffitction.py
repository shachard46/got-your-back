from win10toast import ToastNotifier

toaster = ToastNotifier()


def nottfitcation(Title, Message):
    toaster.show_toast(Title, Message, duration=10)
