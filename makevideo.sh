#!/bin/sh

cd /root/grs/capture

# rename images to be sequential (according to time)
a=1
for i in `ls -tv *.jpg`; do
  new=$(printf "%d.jpg" "$a") #04 pad to length of 4
  mv -- "$i" "$new"
  let a=a+1
done

# call ffmpeg to create our video
ffmpeg -r 6 -start_number 1 -i %d.jpg -s 1280x720 -q:v 1 `date +"%Y-%m-%d_%H%M%S"`.mp4
