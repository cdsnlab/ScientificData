import os
import glob

def meta_processing():
    meta_path = 'metadata'
    meta_list = glob.glob(meta_path+'/*')

    for meta in meta_list:
        new_text = ''
        with open(meta, 'r') as f:
            texts = f.readlines()
            for i in range(len(texts)):
                texts[i] = texts[i].replace('\n', ' ')
            texts = list(filter(lambda x: x != ' ', texts))
            new_text = '\n'.join(texts)
            f.close()
        
        with open(meta, 'w') as f:
            f.write(new_text)
            f.close()

def rearrange_data():
    pass


if __name__ == '__main__':
    meta_processing()
    rearrange_data()