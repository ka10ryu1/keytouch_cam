#!/bin/bash
# auto_train.sh
# train.pyをいろいろな条件で試したい時のスクリプト
# train.pyの引数を手入力するため、ミスが発生しやすい。
# auto_train.shを修正したら、一度-cオプションを実行してミスがないか確認するべき

# オプション引数を判定する部分（変更しない）

usage_exit() {
    echo "Usage: $0 [-c]" 1>&2
    echo " -c: 設定が正常に動作するか確認する"
    exit 1
}

FLAG_CHK=""
while getopts ch OPT
do
    case $OPT in
        c)  FLAG_CHK="--only_check"
            ;;
        h)  usage_exit
            ;;
        \?) usage_exit
            ;;
    esac
done

shift $((OPTIND - 1))

# 以下自由に変更する部分（オプション引数を反映させるなら、$FLG_CHKは必要）

echo -e "\n<< label 01 >>\n"
./create_dataset.py Image/reference.JPG result/01/cap-0* --random -o result/h/01/
./create_dataset.py Image/reference.JPG result/01/cap-0* --random -o result/h/01/
./create_dataset.py Image/reference.JPG result/01/cap-0* --random -o result/h/01/
./create_dataset.py Image/reference.JPG result/01/cap-0* --random -o result/h/01/
./create_dataset.py Image/reference.JPG result/01/cap-0* --random -o result/h/01/

echo -e "\n<< label 02 >>\n"
./create_dataset.py Image/reference.JPG result/02/cap-0* --random -o result/h/02/
./create_dataset.py Image/reference.JPG result/02/cap-0* --random -o result/h/02/
./create_dataset.py Image/reference.JPG result/02/cap-0* --random -o result/h/02/
./create_dataset.py Image/reference.JPG result/02/cap-0* --random -o result/h/02/
./create_dataset.py Image/reference.JPG result/02/cap-0* --random -o result/h/02/


echo -e "\n<< label 03 >>\n"
./create_dataset.py Image/reference.JPG result/03/cap-0* --random -o result/h/03/
./create_dataset.py Image/reference.JPG result/03/cap-0* --random -o result/h/03/
./create_dataset.py Image/reference.JPG result/03/cap-0* --random -o result/h/03/
./create_dataset.py Image/reference.JPG result/03/cap-0* --random -o result/h/03/
./create_dataset.py Image/reference.JPG result/03/cap-0* --random -o result/h/03/


echo -e "\n<< label 04 >>\n"
./create_dataset.py Image/reference.JPG result/04/cap-0* --random -o result/h/04/
./create_dataset.py Image/reference.JPG result/04/cap-0* --random -o result/h/04/
./create_dataset.py Image/reference.JPG result/04/cap-0* --random -o result/h/04/
./create_dataset.py Image/reference.JPG result/04/cap-0* --random -o result/h/04/
./create_dataset.py Image/reference.JPG result/04/cap-0* --random -o result/h/04/


echo -e "\n<< label 05 >>\n"
./create_dataset.py Image/reference.JPG result/05/cap-0* --random -o result/h/05/
./create_dataset.py Image/reference.JPG result/05/cap-0* --random -o result/h/05/
./create_dataset.py Image/reference.JPG result/05/cap-0* --random -o result/h/05/
./create_dataset.py Image/reference.JPG result/05/cap-0* --random -o result/h/05/
./create_dataset.py Image/reference.JPG result/05/cap-0* --random -o result/h/05/


echo -e "\n<< label 06 >>\n"
./create_dataset.py Image/reference.JPG result/06/cap-0* --random -o result/h/06/
./create_dataset.py Image/reference.JPG result/06/cap-0* --random -o result/h/06/
./create_dataset.py Image/reference.JPG result/06/cap-0* --random -o result/h/06/
./create_dataset.py Image/reference.JPG result/06/cap-0* --random -o result/h/06/
./create_dataset.py Image/reference.JPG result/06/cap-0* --random -o result/h/06/


echo -e "\n<< label 07 >>\n"
./create_dataset.py Image/reference.JPG result/07/cap-0* --random -o result/h/07/
./create_dataset.py Image/reference.JPG result/07/cap-0* --random -o result/h/07/
./create_dataset.py Image/reference.JPG result/07/cap-0* --random -o result/h/07/
./create_dataset.py Image/reference.JPG result/07/cap-0* --random -o result/h/07/
./create_dataset.py Image/reference.JPG result/07/cap-0* --random -o result/h/07/
