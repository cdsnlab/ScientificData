from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

import os
import sys
import cv2
import json
import copy
import numpy as np
from time import gmtime
from time import strftime
from opts import opts
from detector import Detector


image_ext = ['jpg', 'jpeg', 'png', 'webp']
video_ext = ['mp4', 'mov', 'avi', 'mkv']
time_stats = ['tot', 'load', 'pre', 'net', 'dec', 'post', 'merge', 'display']


def demo(opt):
    os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
    opt.debug = max(opt.debug, 1)
    detector = Detector(opt)

    if opt.demo == 'webcam' or \
            opt.demo[opt.demo.rfind('.') + 1:].lower() in video_ext:
        is_video = True
        # demo on video stream
        cam = cv2.VideoCapture(0 if opt.demo == 'webcam' else opt.demo)
    else:
        is_video = False
        # Demo on images sequences
        if os.path.isdir(opt.demo):
            image_names = []
            ls = os.listdir(opt.demo)
            for file_name in sorted(ls):
                ext = file_name[file_name.rfind('.') + 1:].lower()
                if ext in image_ext:
                    image_names.append(os.path.join(opt.demo, file_name))
        else:
            image_names = [opt.demo]

    # Initialize output video
    out = None
    out_name = opt.demo[opt.demo.rfind('/') + 1:]
    if opt.save_video:
        if not os.path.exists('../results'):
            os.mkdir('../results')
        if not os.path.exists(f'../results/{opt.date}'):
            os.mkdir(f'../results/{opt.date}')
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(f"../results/{opt.date}/{opt.exp_id + '_' + out_name}", fourcc, opt.save_framerate, (
            opt.input_w, opt.input_h))

    if opt.debug < 5:
        detector.pause = False
    cnt = 0
    results = {}

    while True:
        if is_video:
            _, img = cam.read()
            if img is None:
                save_and_exit(opt, out, results, out_name)
        else:
            if cnt < len(image_names):
                img = cv2.imread(image_names[cnt])
            else:
                save_and_exit(opt, out, results, out_name)
        cnt += 1

        # resize the original video for saving video results
        if opt.resize_video:
            img = cv2.resize(img, (opt.input_w, opt.input_h))

        # skip the first X frames of the video
        if cnt < opt.skip_first:
            continue

        if not opt.save_video:
            cv2.imshow('input', img)

        # track or detect the image..
        if cnt % 2 == 1:
            ret = detector.run(img)

        # log run time
        time_str = 'frame {} |'.format(cnt)
        for stat in time_stats:
            time_str = time_str + '{} {:.3f}s |'.format(stat, ret[stat])
        print(time_str)

        # results[cnt] is a list of dicts:
        #  [{'bbox': [x1, y1, x2, y2], 'tracking_id': id, 'category_id': c, ...}]
        results[cnt] = ret['results']

        # save debug image to video
        if opt.save_video:
            out.write(ret['generic'])
            if not is_video:
                cv2.imwrite('../results/demo{}.jpg'.format(cnt),
                            ret['generic'])

        # esc to quit and finish saving video
        if cv2.waitKey(1) == 27:
            save_and_exit(opt, out, results, out_name)
            return
    save_and_exit(opt, out, results)


def save_and_exit(opt, out=None, results=None, out_name=''):
    if opt.save_results and (results is not None):
        save_dir = f'../results/{opt.date}/{opt.exp_id + "_" + out_name}_results.json'
        print('saving results to', save_dir)
        json.dump(_to_list(copy.deepcopy(results)),
                  open(save_dir, 'w'))
        extract_episode(opt, save_dir, out_name)
    if opt.save_video and out is not None:
        out.release()
    sys.exit(0)


def _to_list(results):
    for img_id in results:
        for t in range(len(results[img_id])):
            for k in results[img_id][t]:
                if isinstance(results[img_id][t][k], (np.ndarray, np.float32)):
                    results[img_id][t][k] = results[img_id][t][k].tolist()
    return results


def extract_episode(opt, save_dir, out_name):
    with open(save_dir, 'r') as f:
        json_data = json.load(f)

    video = cv2.VideoCapture(opt.demo)  
    n_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    duration_sec = n_frames / fps
    actual_n_frames = len(json_data)
    est_fps = actual_n_frames / duration_sec
    spf = duration_sec / actual_n_frames

    life = int(est_fps * opt.term_sec)
    count = life
    prev = False
    episodes = {}
    ep = {}
    list_n_human = []
    idx = 0
    for i in json_data.keys():
        n_human = len(json_data[i])
        if  n_human == 0:
            if prev:
                count -= 1 
            else:
                continue
        else:
            list_n_human.append(n_human)
            if prev:
                count = life
            else:  # start point of episode 
                prev = True
                ep['start'] = frame2min(spf, i)

        if count == 0:  # end point of episode
            count = life
            prev = False
            ep['end'] = frame2min(spf, i, opt.term_sec)
            ep['avg_n_human'] = cal_avg(list_n_human)
            episodes[idx] = ep
            ep = {} 
            list_n_human = []
            idx += 1

    if prev:
        ep['end'] = frame2min(spf, i)
        ep['avg_n_human'] = cal_avg(list_n_human)
        episodes[idx] = ep

    save_dir = f'../results/{opt.date}/{opt.exp_id + "_" + out_name}_episode.json'
    with open(save_dir, 'w') as f:
        json.dump(episodes, f, indent='\t')


def frame2min(spf, frame_num, correction=0):
    sec = spf * float(frame_num) - correction
    hms = strftime("%H:%M:%S", gmtime(sec))
    return hms


def cal_avg(numbers):
    return sum(numbers) / len(numbers)


if __name__ == '__main__':
    opt = opts().init()
    demo(opt)
