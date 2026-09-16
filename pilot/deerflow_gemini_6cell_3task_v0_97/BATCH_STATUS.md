# v0.97 Batch Status

- Batch start: 2026-09-16 02:16:12 UTC
- Frozen planned cells: 18
- Completed cells: 0
- Failed cell: execution-order 1, `T02_RAW100_ASK_R1`
- Failure: the first turn exceeded the frozen 1,800-second hard limit while blocked after streaming 73 trace events.
- Final report: absent
- Score eligibility: false
- Automatic retry: none
- Later cells started: none

The in-process POSIX alarm did not interrupt the blocking call. The process was terminated with `SIGTERM` when the overrun was detected at 2,081 seconds, and the batch stopped as predeclared. The partial trace and input remain in place for engineering diagnosis; they are not a report generation and must not be scored.

For any separately approved future run, the batch wrapper now also imposes an outer process timeout. This engineering repair does not authorize or perform a retry of the failed counted cell.

On 2026-09-16 the user separately approved a fresh full `r2` batch. Its manifest and outputs use new `-r2` thread IDs and `/r2` directories; this r1 status remains immutable.
