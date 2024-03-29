#!/usr/bin/env bash
# test smspilot from ClI (command line interface)
# run 'python3 smspilot.py' before
NUM_GUD=79581000255
NUM_BAD1=123456789
NUM_BAD2=qwert
PHONE_GUD=79012345678
PHONE_BAD1=987654
PHONE_BAD2=qwerty
USER_GUD=10000
USER_BAD1=999
USER_BAD2=qwert
MSG_GUD=456
MSG_BAD1=845
MSG_BAD2=asdfg

doit() {
  curl -X POST -d "id=12345&num=$1&phone=$2&user_id=$3&message=$4" http://localhost:8000/sms.py
}

doit $NUM_GUD $PHONE_GUD $USER_GUD $MSG_GUD
doit $NUM_BAD1 $PHONE_GUD $USER_GUD $MSG_GUD
doit $NUM_BAD2 $PHONE_GUD $USER_GUD $MSG_GUD
doit $NUM_GUD $PHONE_BAD1 $USER_GUD $MSG_GUD
doit $NUM_GUD $PHONE_BAD2 $USER_GUD $MSG_GUD
doit $NUM_GUD $PHONE_GUD $USER_BAD1 $MSG_GUD
doit $NUM_GUD $PHONE_GUD $USER_BAD2 $MSG_GUD
doit $NUM_GUD $PHONE_GUD $USER_GUD $MSG_BAD1
doit $NUM_GUD $PHONE_GUD $USER_GUD $MSG_BAD2
