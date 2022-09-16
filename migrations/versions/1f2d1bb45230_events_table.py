"""events table

Revision ID: 1f2d1bb45230
Revises: 
Create Date: 2022-09-13 11:57:53.234434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f2d1bb45230'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attendee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=64), nullable=True),
    sa.Column('lastname', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=64), nullable=True),
    sa.Column('diet', sa.String(length=64), nullable=True),
    sa.Column('guests', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_attendee_diet'), 'attendee', ['diet'], unique=False)
    op.create_index(op.f('ix_attendee_email'), 'attendee', ['email'], unique=True)
    op.create_index(op.f('ix_attendee_firstname'), 'attendee', ['firstname'], unique=False)
    op.create_index(op.f('ix_attendee_guests'), 'attendee', ['guests'], unique=True)
    op.create_index(op.f('ix_attendee_lastname'), 'attendee', ['lastname'], unique=False)
    op.create_index(op.f('ix_attendee_phone'), 'attendee', ['phone'], unique=True)
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_name', sa.String(length=64), nullable=True),
    sa.Column('event_date', sa.String(length=64), nullable=True),
    sa.Column('event_time', sa.String(length=64), nullable=True),
    sa.Column('event_location', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_event_event_date'), 'event', ['event_date'], unique=False)
    op.create_index(op.f('ix_event_event_location'), 'event', ['event_location'], unique=False)
    op.create_index(op.f('ix_event_event_name'), 'event', ['event_name'], unique=False)
    op.create_index(op.f('ix_event_event_time'), 'event', ['event_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_event_event_time'), table_name='event')
    op.drop_index(op.f('ix_event_event_name'), table_name='event')
    op.drop_index(op.f('ix_event_event_location'), table_name='event')
    op.drop_index(op.f('ix_event_event_date'), table_name='event')
    op.drop_table('event')
    op.drop_index(op.f('ix_attendee_phone'), table_name='attendee')
    op.drop_index(op.f('ix_attendee_lastname'), table_name='attendee')
    op.drop_index(op.f('ix_attendee_guests'), table_name='attendee')
    op.drop_index(op.f('ix_attendee_firstname'), table_name='attendee')
    op.drop_index(op.f('ix_attendee_email'), table_name='attendee')
    op.drop_index(op.f('ix_attendee_diet'), table_name='attendee')
    op.drop_table('attendee')
    # ### end Alembic commands ###