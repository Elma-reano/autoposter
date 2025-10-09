try:
    from notifications import Notification, send_notification
except ModuleNotFoundError:
    # define them but dont do anything
    class Notification:
        def __init__(self, message: str):
            self.message = message
    def send_notification(notification: Notification):
        print('--', notification.message, '--')
except Exception as e:
    print(f"Error. {e}")

def notify(text: str) -> None:
    """
    This function should work on Pyto, sending a notification
    On other platforms, such as desktop, it prints the message to console

    Args:
        text (str): The text of the notification
    """
    notif = Notification(message= text)
    send_notification(notif)

if __name__ == '__main__':
    notify("Hello There!")