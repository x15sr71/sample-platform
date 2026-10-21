"""Correct the CEA-708 expected filenames and reclassify regression test 154.

Companion to the change that makes a CEA-708 entry lead with the bare sample
name for CCExtractor to use as -o. That alone is not enough: the name each test
then looks for still has to match what CCExtractor writes, which is
``.p<program>.svc<service>`` with the program number taken from the stream.

Measured against each sample with a full-Rust build, which is what the platform
now downloads. A ``-min-rust`` build emits no CEA-708 at all, so it cannot be
used to establish these. Cross-check: RT 138's output hashes to 285da9c8cf22…,
the same hash the platform has been recording for RT 145, which picked that file
up from RT 139's run.

    RT 137  ea83ff7b…  ->  .p0.svc01   (stored .p1.svc01)
    RT 138  f17524b5…  ->  .p0.svc01   (stored .p1.svc01)
    RT 139  da904de3…  ->  .p1.svc01   (stored '', and ignored)
    RT 154  c83f765c…  ->  .p1.svc01   (stored '')
    all others                          already correct

RT 139 and RT 154 stored the bare ``-o`` name rather than the name of a file
CCExtractor produces. The platform now emits that bare name itself, so both can
name the service file they are actually meant to check. RT 139 was additionally
ignored, which is why it has been reporting Pass while producing nothing at all.

RT 154 is a 708-only test (``--service 1``) that was typed as a plain file test,
so it takes the same broken path as the CEA-708 category without being part of
it.

Note RT 140 is deliberately left alone. Its sample carries no CEA-708 data at
all (``CC type 2: 0``, ``CC type 3: 0``), so no expected filename can make it
pass; it needs a decision about what that test is for.

Revision ID: f2c71a9b5e04
Revises: e7c9b4a2d1f0
Create Date: 2026-09-16 17:20:00.000000

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f2c71a9b5e04'
down_revision = 'e7c9b4a2d1f0'
branch_labels = None
depends_on = None


def upgrade():
    """Point the CEA-708 outputs at the files CCExtractor actually writes."""
    # `ignore` is a reserved word in MySQL and has to stay quoted.
    op.execute("UPDATE regression_test_output SET expected_filename = '.p0.svc01' WHERE regression_id IN (137, 138)")
    op.execute("UPDATE regression_test_output SET expected_filename = '.p1.svc01', `ignore` = 0 "
               "WHERE regression_id = 139")
    op.execute("UPDATE regression_test_output SET expected_filename = '.p1.svc01' WHERE regression_id = 154")
    op.execute("UPDATE regression_test SET output_type = 'cea708' WHERE id = 154")


def downgrade():
    """Restore the previous expected filenames and output type."""
    op.execute("UPDATE regression_test_output SET expected_filename = '.p1.svc01' WHERE regression_id IN (137, 138)")
    op.execute("UPDATE regression_test_output SET expected_filename = '', `ignore` = 1 WHERE regression_id = 139")
    op.execute("UPDATE regression_test_output SET expected_filename = '' WHERE regression_id = 154")
    op.execute("UPDATE regression_test SET output_type = 'file' WHERE id = 154")
