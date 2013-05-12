#!/bin/sh
# resetting all data
gunzip -c data.db.gz > data.db
cat postsqlite.sql | sqlite3 data.db
cat convert_0.sql | sqlite3 data.db
cat convert_1.sql | sqlite3 data.db
