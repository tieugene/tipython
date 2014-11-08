DROP TABLE IF EXISTS "data";
CREATE TABLE "data" (
    "stamp"	INTEGER NOT NULL,
    "ymd"	INTEGER NOT NULL,
    "hour"	INTEGER NOT NULL,
    "proto"	INTEGER NOT NULL,
    "iip"	INTEGER NOT NULL,
    "iport"	INTEGER NOT NULL,
    "oip"	INTEGER NOT NULL,
    "oport"	INTEGER NOT NULL,
    "ibytes"	INTEGER NOT NULL,
    "obytes"	INTEGER NOT NULL
);
CREATE INDEX "stamp"	on data (stamp ASC);
CREATE INDEX "ymd"	on data (ymd ASC);
CREATE INDEX "hour"	on data (hour ASC);
CREATE INDEX "proto"	on data (proto ASC);
CREATE INDEX "iip"	on data (iip ASC);
CREATE INDEX "iport"	on data (iport ASC);
CREATE INDEX "oip"	on data (oip ASC);
CREATE INDEX "oport"	on data (oport ASC);
