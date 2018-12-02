SELECT PI, SUM(cpuseconds) 
FROM uma 
WHERE endtime > '2018-07-01' 
GROUP by PI 
HAVING SUM(cpuseconds) > 315360000 
ORDER by SUM(cpuseconds) DESC;

