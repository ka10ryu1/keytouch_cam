#!/usr/bin/env python3
# -*-coding: utf-8 -*-
#
help = '画像を読み込んでデータセットを作成する'
#

import cv2
import time
import argparse
import numpy as np

import Tools.func as F


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


def alignImages(img1, img2,
                max_pts=500, good_match_rate=0.15, min_match=10):
    # https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html#feature-homography

    # Initiate SIFT detector
    detector = cv2.ORB_create(max_pts)
    # find the keypoints and descriptors with SIFT
    kp1, des1 = detector.detectAndCompute(
        cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), None
    )
    kp2, des2 = detector.detectAndCompute(
        cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), None
    )
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(des1, des2)
    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)
    good = matches[:int(len(matches) * good_match_rate)]
    if len(good) > min_match:
        src_pts = np.float32(
            [kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32(
            [kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # Find homography
        h, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC)
        # Use homography
        height, width, channels = img1.shape
        dst_img = cv2.warpPerspective(img2, h, (width, height))
        return dst_img, h
    else:
        return img1, np.zeros((3, 3))


def main(args):
    # Read reference image
    ref_name = args.jpeg[0]
    print('Reading reference image : ', ref_name)
    ref = cv2.imread(ref_name, cv2.IMREAD_COLOR)

    # Read image to be aligned
    img_name = args.jpeg[1]
    print('Reading image to align : ', img_name)
    img = cv2.imread(img_name, cv2.IMREAD_COLOR)

    num = 1

    print('Aligning images ...')
    # Registered image will be resotred in imReg.
    # The estimated homography will be stored in h.
    st = time.time()
    for i in range(num):
        dst, h = alignImages(ref, img)

    print(time.time() - st)

    if args.homography != '':
        arr = np.load(args.homography)
        print(arr['h'])
        height, width, channels = img.shape
        h = arr['h']
        st = time.time()
        for i in range(num):
            dst = cv2.warpPerspective(ref, h, (width, height))

        print(time.time() - st)

    # Write aligned image to disk.
    outFileName = F.getFilePath(args.out_path, 'aligned', '.jpg')
    print('Saving aligned image : ', outFileName)
    cv2.imwrite(outFileName, dst)

    # Print estimated homography
    print('Estimated homography : \n',  h)
    outFileName = F.getFilePath(args.out_path, 'h', '.npz')
    np.savez(outFileName, h=h)

    cv2.imshow('view', dst)
    cv2.waitKey()


if __name__ == '__main__':

    args = command()
    F.argsPrint(args)
    main(args)
