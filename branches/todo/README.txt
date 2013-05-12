Task:
	ID	PK
	Prio	Enum	1..5
	State	Enum	New/Accepted/Completed/Approved/Rejected
	Author	User
	Doer	User
	Created	DateTime(auto)
	Updated	DateTime(auto)
	Title	Char
	Comment	Text (reSt, creole, markdown, textile)
TaskHistory:
	Prio
	State
	Author (of change)
	Doer
	Date
	Title
	Comment (of change)
	====
So, in tasklist I need show 1st datetime and 1st author

Solutions:
	1) Just ID in Task - and current values in History. Then show last history record. BUT - init author and date
	2) Just ID in Task - and _new_ values in History. Then show last records.
	3) Full record in Task (current value) - and difs/old values in History
Feautres:
	* Task list:
		*