import os

DIR = '/home/student/more_space/stitch'
print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))