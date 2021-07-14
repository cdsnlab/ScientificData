import os 

PATH = 'C:/Users/skygu/Downloads/2017N1SeminarRoom825 (3)'

print(os.listdir(PATH))


def fname_extractor(path):
    result_fname = 'fnames.csv'

    days = os.listdir(path)
    fnames = []
    for day in days:
        fnames.extend(os.listdir(f'{path}/{day}'))
    
    result = '\n'.join(fnames)
    with open(result_fname, 'w') as f:
        f.write(result)
        f.close()

if __name__ == '__main__':
    path = PATH
    fname_extractor(path)
