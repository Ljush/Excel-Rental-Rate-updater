# verify OS
def current_os():
    import platform
    result = platform.system().lower()
    # WINDOWS os ~ 'Windows'
    if result == 'windows':
        return result
    # MAC OSX ~ 'Darwin'
    if result == 'darwin':
        return result

if __name__ == '__main__':
    current_os()