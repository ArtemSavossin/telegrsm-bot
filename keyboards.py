def keyboard_from_arr(arr):
    keyboard = []
    for i in range(len(arr)):
        if i + 1 % 2 == 1:
            keyboard.append([arr[i - 1], arr[i]])
    if len(arr) % 2 != 0:
        keyboard.append([arr[-1]])
    return keyboard

main_keyboard = [
    ['Check stats', 'Check balance'],
    ['Notifications', 'Shutdown'],
    ['/help'],
]

stats_keyboard = [
    ['Daily', 'Weekly'],
    ['Monthly','Overall'],
    ['/back']
]