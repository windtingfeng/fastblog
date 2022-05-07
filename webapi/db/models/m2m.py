from sqlalchemy import Table, Integer, Column, ForeignKey

from webapi.db.config import Base

post_category = Table(
    'post_category',  # �����ű���
    Base.metadata,  # Ԫ�������
    Column('post_id', Integer, ForeignKey('Post.id'), primary_key=True),  # �������µ��ֶ�
    Column('category_id', Integer, ForeignKey('Category.id'), primary_key=True),  # ��ǩ����������ֶ�
    # ���ֶ�primary_key������True���������Ψһ����ֹ����һ��
)
