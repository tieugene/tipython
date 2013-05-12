BEGIN { FS="\t"; print "BEGIN;" }
{
	print "INSERT INTO data (model, record, field, value) VALUES ('ref_okato', " $1 ", 'parent_id', " $2 ");"
	print "INSERT INTO data (model, record, field, value) VALUES ('ref_okato', " $1 ", 'code', '" $3 "');";
	print "INSERT INTO data (model, record, field, value) VALUES ('ref_okato', " $1 ", 'name', '" $4 "');";
	print "INSERT INTO data (model, record, field, value) VALUES ('ref_okato', " $1 ", 'comments', 'patch');";
}
END { print "COMMIT;" }
