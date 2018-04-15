#!/usr/bin/env python3
# -*-coding: utf-8 -*-
#
help = '画像を読み込んでデータセットを作成する'
#

import cv2
import time
import argparse
import numpy as np


def command():
    parser = argparse.ArgumentParser(description=help)
    parser.add_argument('jpeg', nargs='+',
                        help='使用する画像のパス')
    parser.add_argument('--channel', '-c', type=int, default=1,
                        help='画像のチャンネル数 [default: 1 channel]')
    parser.add_argument('--img_size', '-s', type=int, default=32,
                        help='生成される画像サイズ [default: 32 pixel]')
    parser.add_argument('--round', '-r', type=int, default=1000,
                        help='切り捨てる数 [default: 1000]')
    parser.add_argument('--quality', '-q', type=int, default=5,
                        help='画像の圧縮率 [default: 5]')
    parser.add_argument('--train_per_all', '-t', type=float, default=0.9,
                        help='画像数に対する学習用画像の割合 [default: 0.9]')
    parser.add_argument('-o', '--out_path', default='./result/',
                        help='・ (default: ./result/)')
    parser.add_argument('-hg', '--homography', default='',
                        help='・ ')
    return parser.parse_args()


def main(args):
    cap = cv2.VideoCapture(0)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            cv2.imshow('frame', frame)
        else:
            time.sleep(2)

        # Display the resulting frame
        if cv2.waitKey(20) == 27:
            cv2.imwrite('cam.jpg', frame)
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    args = command()
    main(args)
