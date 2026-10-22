"""Stop expecting an output file from the regression tests whose reference is empty or a bare BOM.

CCExtractor no longer writes such a file. Without --bom it writes no BOM
(#1268 for non-Windows builds, #1383 for Windows), so a run that finds no
captions leaves a 0-byte file, and since #1877 dinit_write() deletes 0-byte
output files. These tests have reported "No output generated" since then
(test 7702 -> 7704 on Linux), although CCExtractor does what it is meant to:

    RT 3    expects a BOM-only .srt   exit code 10
    RT 7    expects an empty .txt     exit code 0
    RT 16   expects an empty .srt     exit code 0
    RT 20   expects an empty .srt     exit code 10
    RT 63   expects an empty .srt     exit code 10
    RT 167  expects a BOM-only .srt   exit code 10
    RT 218  expects a BOM-only .srt   exit code 10
    RT 220  expects a BOM-only .srt   exit code 10

None of their commands passes --bom. Each has exactly one output. Ignoring it
is how the platform already says "no file expected": the runner doesn't look
for the file, and get_test_results() judges the test on its exit code alone.

Revision ID: 7a38d6077940
Revises: e7c9b4a2d1f0
Create Date: 2026-10-22 14:32:31.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '7a38d6077940'
down_revision = 'e7c9b4a2d1f0'
branch_labels = None
depends_on = None


def upgrade():
    """Stop expecting an output file from these tests."""
    # `ignore` is a reserved word in MySQL and has to stay quoted.
    op.execute("UPDATE regression_test_output SET `ignore` = 1 "
               "WHERE regression_id IN (3, 7, 16, 20, 63, 167, 218, 220)")


def downgrade():
    """Expect the output files again."""
    op.execute("UPDATE regression_test_output SET `ignore` = 0 "
               "WHERE regression_id IN (3, 7, 16, 20, 63, 167, 218, 220)")
