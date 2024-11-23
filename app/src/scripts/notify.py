from notifypy import Notify

notification = Notify()
notification.title = "Notification Title"
notification.message = "Message"
notification.icon = "./images/notification_icon_no_bg.png"
#notification.audio = "path/to/audio/file.wav"
notification.send()