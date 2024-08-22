from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c20dfc28c614'
down_revision = 'cabbd1b61dbd'
branch_labels = None
depends_on = None

def upgrade():
    # Create the new table
    op.create_table(
        'token_blocked_list',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('jti', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Check if columns already exist before adding them
    with op.batch_alter_table('user', schema=None) as batch_op:
        # Check if 'first_name' column already exists
        if 'first_name' not in [col['name'] for col in batch_op.get_columns()]:
            batch_op.add_column(sa.Column('first_name', sa.String(length=120), nullable=False))
        # Check if 'last_name' column already exists
        if 'last_name' not in [col['name'] for col in batch_op.get_columns()]:
            batch_op.add_column(sa.Column('last_name', sa.String(length=120), nullable=False))

def downgrade():
    # Drop the columns if they exist
    with op.batch_alter_table('user', schema=None) as batch_op:
        if 'last_name' in [col['name'] for col in batch_op.get_columns()]:
            batch_op.drop_column('last_name')
        if 'first_name' in [col['name'] for col in batch_op.get_columns()]:
            batch_op.drop_column('first_name')

    # Drop the table
    op.drop_table('token_blocked_list')
