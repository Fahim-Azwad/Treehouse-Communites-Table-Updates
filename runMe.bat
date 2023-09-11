:: Name:     postgres-insert.bat
:: Purpose:  Update postgres tables with data from various sources- mainly from Manage America
:: Author:   joshua.mayberry1991@gmail.com

:: Revision: 
	:: 03/09/2022 - Initial Version
	:: 03/11/2022 - Args Support

:: Python
	:: See: https://datatofish.com/batch-python-script/
	:: See: https://superuser.com/questions/1374997/pass-arguments-of-bat-file-to-executed-exe-file/1375009#1375009

:: Logging
	:: Use: https://stackoverflow.com/questions/7757525/printing-batch-file-results-to-a-text-file/15951294#15951294
	:: See: https://stackoverflow.com/questions/132799/how-can-i-echo-a-newline-in-a-batch-file/3123194#3123194
	:: See: https://stackoverflow.com/questions/1420965/redirect-windows-cmd-stdout-and-stderr-to-a-single-file/1420981#1420981
	:: See: https://serverfault.com/questions/245393/how-do-you-wait-for-an-exe-to-complete-in-batch-file/245394#245394
	:: See: https://stackoverflow.com/questions/154075/using-the-start-command-with-parameters-passed-to-the-started-program/37229957#37229957
	:: See: https://docs.microsoft.com/en-us/answers/questions/76050/task-scheduler-start-a-task-and-shows-running-but.html

@ECHO off
SETLOCAL

:: TIME VARIABLES
	SET year=%DATE:~10,4%
	SET dow=%DATE:~0,3%
	SET day=%DATE:~7,2%
	SET mnt=%DATE:~4,2%
	SET hr=%TIME:~0,2%
	SET min=%TIME:~3,2%

	:: If the time is less than two digits insert a zero so there is no space to break the filename
	IF %day% LSS 10 SET day=0%day:~1,1%
	IF %mnt% LSS 10 SET mnt=0%mnt:~1,1%
	IF %hr% LSS 10 SET hr=0%hr:~1,1%
	IF %min% LSS 10 SET min=0%min:~1,1%

	SET currentTime=%year%-%mnt%-%day%-%hr%-%min%

	:: Number of days to retain log files
	SET retaindays=7

:: DIRECTORIES
	SET hostname=%COMPUTERNAME%
	If "%hostname%" == "ROOTSMG-PF2ZPQJ" (
		SET exe_python=C:\Program Files\Python310\python.exe
		SET dir_log=C:\Users\JoshuaMayberry\Stonebrink Leads Dropbox\Joshua Mayberry\systems_data\logs
		SET dir_postgresDBtst=C:\Users\JoshuaMayberry\Documents\Jeremy\posgresDBtst
	) ELSE (
		SET exe_python=C:\Program Files\Python310\python.exe
		SET dir_log=C:\Users\jmayberry\Stonebrink Leads Dropbox\Joshua Mayberry\systems_data\logs
		SET dir_postgresDBtst=C:\Projects\postgresDBtst
	)

:: LOG OUTPUT
	IF "%1" == "--log_subname" (
		SET log_subname=%2
	) ELSE (
		SET log_subname=general
	)

	SET LOGFILE=%dir_log%\postgres-insert__%log_subname%__%currentTime%.log
	CALL :Logit %* 2>&1 > "%LOGFILE%"

:: pause
ENDLOCAL
exit /b 0

:Logit
	:: Run Scrapers
		PUSHD "%dir_postgresDBtst%"

			ECHO:
			ECHO Running file...
			START /b /wait "" "%exe_python%" controller.py %* 2>&1

		POPD

	:: REMOVE OLD LOGS
		ECHO:
		ECHO Deleting log files older than %retaindays% days

		FOR %%A IN ("%dir_log%",) DO (
			PUSHD %%A 
				ForFiles /m *.log /D -%retaindays% /c "cmd /c del @path"
			POPD
			)
		
	:: FINISH
		ECHO Done
