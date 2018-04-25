#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
help = 'データセットテキスト生成部分'
#

import os

import cv2
import time
import argparse
import numpy as np

import Tools.func as F
import Tools.imgfunc as IMG

from glob import glob


def command():
    parser = argparse.ArgumentParser(description=help)
    parser.add_argument('img_root_path',
                        help='テキストデータを作成したいデータセットのルートパス')
    parser.add_argument('--train_per_all', '-t', type=float, default=0.9,
                        help='画像数に対する学習用画像の割合 [default: 0.9]')
    parser.add_argument('-o', '--out_path', default='./result/',
                        help='データの保存先 (default: ./result/)')
    return parser.parse_args()


def writeTXT(folder, name, data):
    """
    テキストファイルを書き出す
    [in] folder: テキストを保存するフォルダ
    [in] name:   テキストの名前
    [in] data:   保存するデータ

    dataは[(path1, val1), (path2, val2), ... , (pathN, valN)]の形式であること
    pathN: N番目の画像パス
    valN:  N番目の画像の分類番号
    """

    with open(os.path.join(folder, name), 'w') as f:
        [f.write('./' + i + ' ' + j + '\n') for i, j in data]


def main(args):
    # 画像データを探索し、画像データのパスと、サブディレクトリの値を格納する
    search = os.path.join(args.img_root_path, '**')
    data = [(img, int(img.split('/')[1])) for img in glob(search, recursive=True)
            if IMG.isImgPath(img, True)]
    # 取得したデータをランダムに学習用とテスト用に分類する
    data_arr = np.array(data)
    data_len = len(data_arr)
    shuffle = np.random.permutation(range(data_len))
    train_size = int(data_len * args.train_per_all)
    train = data_arr[shuffle[:train_size]]
    test = data_arr[shuffle[train_size:]]
    # chainer.datasets.LabeledImageDataset形式で出力する
    writeTXT(args.out_path, 'train.txt', train)
    writeTXT(args.out_path, 'test.txt', test)


if __name__ == '__main__':
    args = command()
    F.argsPrint(args)
    main(args)
