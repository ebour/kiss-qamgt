SELECT date, sum(workload) as workload FROM testplan WHERE status IN ('PASSED') GROUP BY date ORDER BY date ASC