#!/usr/bin/bash
for port in 8000 8001 8002 8003
do
	nohup python $@ --port=$port &
done
