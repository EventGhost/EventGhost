# -*- coding: utf-8 -*-

import time

from notifier import ToastNotifier

# #############################################################################
# ###### Stand alone program ########
# ###################################
if __name__ == "__main__":
    # Example
    toaster = ToastNotifier()
    # toaster.show_toast(
    #     "Hello World!!!",
    #     "Python is 10 seconds awsm!",
    #     duration=10)
    # # Wait for threaded notification to finish
    # while toaster.notification_active():
    #     time.sleep(0.1)
    # toaster.show_toast(
    #     "Example two",
    #     "This notification is in it's own thread!",
    #     icon_path=None,
    #     duration=5,
    #     threaded=True
    #     )
    # # Wait for threaded notification to finish
    # while toaster.notification_active():
    #     time.sleep(0.1)

    def clicked(*args, **kwargs):
        print "yes, you like me :)"
        print "args =", args
        print "kwargs =", kwargs

    toaster.show_toast(
        "And now with callback",
        "You can call me... ehm, i mean, you can click me.",
        callback_on_click=clicked)
    # # Wait for threaded notification to finish
    # while toaster.notification_active():
    #     time.sleep(0.1)
