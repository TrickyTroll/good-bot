import subprocess

def clean_res():
    '''
    Uses term_finder.sh to find the resolution and top left
    corner of the terminal window.

    It then filters the output of the function so that it will
    be easier to use later on.

    Returns: A list of lists containing resolution and all corners 
    coordinates starting from top left going clockwise to bot left.
    '''
    x = subprocess.run(['./term_finder.sh'], stdout = subprocess.PIPE)

    string_x = x.stdout.decode('utf-8')

    filtered_x = string_x.replace("\n", '')

    listed_params = filtered_x.split(' ')
    
    res = listed_params[0].split('x')

    width = int(res[0])

    height = int(res[1])

    top_left_string = listed_params[1].split(',')

    top_left = list(map(int,top_left_string))

    # This second section finds the other corners of the window.

    top_right = [top_left[0] + width, top_left[1]]

    bot_right = [top_right[0],  top_right[1] + height]

    bot_left = [top_left[0], top_left[1] + height]

    # Creating a list of all params to return

    all_params = [[width, height], top_left, top_right, bot_right, bot_left]

    return all_params



    
