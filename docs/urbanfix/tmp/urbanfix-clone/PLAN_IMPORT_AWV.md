# Plan: Filter incident reports from aldo.fieuw@gmail IMAP

Steps (broken up — don't do all at once):
1. ✅ Filter IMAP import: only AWV subject codes (KM-/MB-/G-...) or AWV senders
2. ✅ Remove UNSEEN filter — read incident reports must also import
3. ⏸ Clear bad reports from previous unfiltered import (Brave, newsletter)
4. ⏸ Re-run import with maxMessages=20 (inbox has 3,889 emails)
5. ⏸ Verify reports in data/reports.json match AWV codes
6. ⏸ Confirm frontend shows them (maps / list view)

Note: IMAP import takes >180s on full inbox; must run with limit.
