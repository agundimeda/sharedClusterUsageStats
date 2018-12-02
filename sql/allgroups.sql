SELECT PI 
FROM uma 
WHERE endtime > '2013-07-01'
GROUP by PI 
ORDER by SUM(cpuseconds) DESC;

