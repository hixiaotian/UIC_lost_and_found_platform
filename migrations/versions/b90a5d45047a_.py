"""empty message

Revision ID: b90a5d45047a
Revises: 
Create Date: 2019-05-18 23:50:36.377712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b90a5d45047a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store_location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location_name', sa.String(length=50), nullable=False),
    sa.Column('available_time', sa.String(length=50), nullable=True),
    sa.Column('phone_number', sa.String(length=50), nullable=True),
    sa.Column('pic', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('true_name', sa.String(length=32), nullable=False),
    sa.Column('phone_number', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.Column('storage_id', sa.Integer(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.Column('icon', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['storage_id'], ['store_location.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('broadcast',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('uploader_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('content', sa.String(length=400), nullable=True),
    sa.ForeignKeyConstraint(['uploader_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('change_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('changer_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('item_name', sa.String(length=50), nullable=True),
    sa.Column('method', sa.String(length=50), nullable=False),
    sa.Column('content', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['changer_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=50), nullable=False),
    sa.Column('time', sa.String(length=50), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('uploader_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('location', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=400), nullable=True),
    sa.Column('pic', sa.String(length=64), nullable=True),
    sa.Column('store_location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['store_location_id'], ['store_location.id'], ),
    sa.ForeignKeyConstraint(['uploader_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('store_location_id', sa.Integer(), nullable=True),
    sa.Column('is_recieve', sa.Boolean(), nullable=True),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('content', sa.String(length=400), nullable=True),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['store_location_id'], ['store_location.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('uploader_id', sa.Integer(), nullable=True),
    sa.Column('comment_item', sa.Integer(), nullable=True),
    sa.Column('content', sa.String(length=400), nullable=True),
    sa.ForeignKeyConstraint(['comment_item'], ['items.id'], ),
    sa.ForeignKeyConstraint(['uploader_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('messages')
    op.drop_table('items')
    op.drop_table('change_log')
    op.drop_table('broadcast')
    op.drop_table('users')
    op.drop_table('store_location')
    op.drop_table('group')
    op.drop_table('category')
    # ### end Alembic commands ###
