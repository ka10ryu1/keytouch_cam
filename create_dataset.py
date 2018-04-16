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
    parser.add_argument('ref_img',
                        help='使用する参照画像のパス')
    parser.add_argument('cap_img', nargs='+',
                        help='使用するキャプチャ画像のパス')
    parser.add_argument('--train_per_all', '-t', type=float, default=0.9,
                        help='画像数に対する学習用画像の割合 [default: 0.9]')
    parser.add_argument('-o', '--out_path', default='./result/',
                        help='データの保存先 (default: ./result/)')
    parser.add_argument('-hg', '--homography', default='',
                        help='使用したい透視変換行列のパス ')
    parser.add_argument('--view', action='store_true',
                        help='cv2.imshow()で変換結果を表示する')
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


def main(ref, cam, out_path, num, homography, view):
    # Read reference image
    ref_name = ref
    print('Reading reference image : ', ref_name)
    ref = cv2.imread(ref_name, cv2.IMREAD_COLOR)

    # Read image to be aligned
    img_name = cam
    print('Reading image to align : ', img_name)
    img = cv2.imread(img_name, cv2.IMREAD_COLOR)

    print('Aligning images ...')
    # Registered image will be resotred in imReg.
    # The estimated homography will be stored in h.
    st = time.time()
    if args.homography == '':
        dst, h = alignImages(ref, img)
    else:
        arr = np.load(args.homography)
        height, width, channels = img.shape
        h = arr['h']
        dst = cv2.warpPerspective(ref, h, (width, height))

    print(time.time() - st)

    # Write aligned image to disk.
    outFileName = F.getFilePath(args.out_path, 'aligned_'+str(num).zfill(5), '.jpg')
    print('Saving aligned image : ', outFileName)
    cv2.imwrite(outFileName, dst)

    # Print estimated homography
    print('Estimated homography : \n',  h)
    outFileName = F.getFilePath(args.out_path, 'h_'+str(num).zfill(5), '.npz')
    np.savez(outFileName, h=h)

    if args.view:
        cv2.imshow('view', dst)
        cv2.waitKey()


if __name__ == '__main__':

    args = command()
    F.argsPrint(args)
    for i, cap in enumerate(args.cap_img):
        main(args.ref_img, cap, args.out_path, i, args.homography, args.view)
