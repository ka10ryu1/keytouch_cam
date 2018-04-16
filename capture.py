#!/usr/bin/env python3
# -*-coding: utf-8 -*-
#
help = 'Webカメラから画像を取得する'
#

import cv2
import time
import argparse


def command():
    parser = argparse.ArgumentParser(description=help)
    parser.add_argument('--channel', '-c', type=int, default=0,
                        help='使用するWebカメラのチャンネル [default: 0]')
    parser.add_argument('-o', '--out_path', default='./result/',
                        help='画像の保存先 (default: ./result/)')
    parser.add_argument('--lower', action='store_true',
                        help='select timeoutが発生する場合に画質を落とす')
    return parser.parse_args()


def main(args):
    cap = cv2.VideoCapture(args.channel)

    if args.lower:
        cap.set(3, 200)
        cap.set(4, 200)
        cap.set(5, 5)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            cv2.imshow('frame', frame)
        else:
            time.sleep(2)

        key = cv2.waitKey(20) & 0xff
        # Display the resulting frame
        if key == 27:
            print('exit!')
            break
        elif key == ord('s'):
            print('capture!')
            cv2.imwrite('cam.jpg', frame)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    args = command()

    print('Key bindings')
    print('[Esc] Exit')
    print('[ s ] Save image')

    main(args)
