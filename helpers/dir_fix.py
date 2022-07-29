# __main__ helper function
# hope this would save the text file in this folder instead
from verify_OS import current_os
from tkinter import Tk, filedialog
TK_SILENCE_DEPRECATION = 1
def file_open(OS):
    if OS == 'windows':
        try:
            with open('win_directories.txt', 'r') as w:
                folder = w.read()
        except:
            more = open('resources/win_directories.txt', 'x')
            with open('resources/win_directories.txt', 'w') as useless:
                folder = get_user_input()
                pointers = useless.write(folder)

    if OS == 'darwin':
        # open directory txt file to get string of user pathway to sheets folder
        try:
            with open('resources/mac_directories.txt', 'r') as m:
                folder = m.read()
        # otherwise create the txt file and continue as normal
        except:
            marvel = open('resources/mac_directories.txt', 'x')
            """ GRAB SHEETS FOLDER PATH HERE """
            print('\n', '*'*35, '\n **** SELECT THE SHEETS FOLDER ****\n', '*'*35, '\n')
            with open('resources/mac_directories.txt', 'w') as stinks:
                folder = get_user_input()
                yo = stinks.write(folder)
                
            #sheets_folder = new.read()
    #print(sheets_folder)
    pass

def get_user_input():
    root = Tk()
    
    root.withdraw()
    folder = filedialog.askdirectory()
    return folder


def dir_fix_main():
    OS = current_os()
    temp = file_open(OS)

if __name__ == '__main__':
    dir_fix_main()