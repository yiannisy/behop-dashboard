#!/bin/bash

dst_dir=/home/yiannis/behop_dashboard/static/img/

./get_netflix.py
./get_youtube.py
./analyze_sessions.py
./get_usage.py

cp /tmp/usage.png ${dst_dir}
cp /tmp/s*_sum.png ${dst_dir}
cp /tmp/client_cdf.png ${dst_dir}
cp /tmp/netflix_s5.png ${dst_dir}
cp /tmp/youtube_s5.png ${dst_dir}
cp /tmp/studio*_session*_cdf.png ${dst_dir}
