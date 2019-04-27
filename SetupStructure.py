import os

dir_name = os.path.join(os.path.dirname(__file__), 'data')

check_dirs = ['models',
              'audio',
              'plots',
              'map_data',
              os.path.join('audio', 'Original_Files'),
              os.path.join('audio', 'Original_Files', 'Added_Audio'),
              os.path.join('audio', 'Original_Files', 'Road_Noise'),
              os.path.join('audio', 'Test'),
              os.path.join('audio', 'Test', 'No_Traffic_Incident'),
              os.path.join('audio', 'Test', 'Traffic_Incident'),
              os.path.join('audio', 'Train'),
              os.path.join('audio', 'Train', 'No_Traffic_Incident'),
              os.path.join('audio', 'Train', 'Traffic_Incident'),
             ]


for directory in check_dirs:
    if not os.path.isdir(os.path.join(dir_name, directory)):
        os.mkdir(os.path.join(dir_name, directory))

