#!/bin/bash

gitRemote="remote.origin.url"

function addAuthInfo() {
	echo "$1" | sed "s/https:\/\//&$2:$3@/g"
}

function removeAuthInfo() {
	echo "$1" | sed "s/\/\/[^@]*@/\/\//g"
}

function findString() {
	if echo "$1" | grep "$2" > /dev/null ;then
		return 0;
	else
		return -1;
	fi
}

function checkAuthExist() {
	if findString $1 "\/\/[^@]*@" ;then
		return 0;
	else
		return -1;
	fi
}

function getURL() {
	echo `git config --get ${gitRemote}`
}

if [ "$1" == "" ];then
	echo "帳號無輸入"
	exit 1
fi

if [ "$2" == "" ];then
	echo "密碼無輸入"
	exit 2
fi

if ! test -d "${3}/.git/"; then
	echo "repo輸入錯誤"
	exit 3
fi

cd $3

URL=`getURL`

if ! findString $URL "https://"; then
	echo "repo通訊協定錯誤，請設定成https"
	exit 4
fi

## 如果已經有認證資訊，先拔掉
if checkAuthExist; then
	git config ${gitRemote} `removeAuthInfo $URL`
	URL=`getURL`
fi

## 設定帳號
git config $gitRemote `addAuthInfo $URL $1 $2`

## 推檔案上去
git add .
git commit -m "$4"
git push

## 移除認證資訊
git config ${gitRemote} `removeAuthInfo $(getURL) `


