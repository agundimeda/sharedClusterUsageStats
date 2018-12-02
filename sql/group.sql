SET @uma_name := 'uma_gregory_grason';

SET @SoMDate := '2018-11-01';
SET @SoYDate := '2018-07-01'; 

SELECT @uma_name AS 'Principal Investigator: ';

SELECT 'Month-to-Date Usage by User: ' AS '';
SELECT username, SUM(cpuseconds)
FROM uma
WHERE PI = @uma_name AND endtime >= @SoMDate
GROUP by username
ORDER by cpuseconds DESC
; 
	
SELECT 'Total Month-to-Date Usage: ' AS '';
SELECT SUM(cpuseconds) 
FROM uma 
WHERE PI = @uma_name AND endtime >= @SoMDate
;

SELECT 'Year-to-Date Usage by User: ' AS '';
SELECT username, SUM(cpuseconds)
FROM uma
WHERE PI = @uma_name AND endtime >= @SoYDate
GROUP by username
ORDER by cpuseconds DESC
; 
	
SELECT 'Total Year-to-Date Usage: ' AS '';
SELECT SUM(cpuseconds) 
FROM uma 
WHERE PI = @uma_name AND endtime >= @SoYDate
;
