#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Added extra data"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '26845fffb502'
down_revision = '0aea984dbf38'
branch_labels = ()
depends_on = None


def upgrade():
    """Upgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('taxonomy', sa.Column('extra_data', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    """Downgrade database."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('taxonomy', 'extra_data')
    # ### end Alembic commands ###
