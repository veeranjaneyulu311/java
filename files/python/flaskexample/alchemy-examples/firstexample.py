from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship,backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

#tables creation

Base=declarative_base()
print(type(Base))
#engine = create_engine('postgresql://postgres:admin@localhost/postgres', echo = True)
engine = create_engine('sqlite:///E:/files/python/chinook.db', echo = True)
class Department(Base):
	__tablename__='department'
	id = Column(Integer,primary_key=True)
	name=Column(String)

class Employee(Base):
	__tablename__="employee"
	id=Column(Integer,primary_key=True)
	name=Column(String)
	department_id=Column(Integer, ForeignKey('department.id'))
	department = relationship(Department, backref=backref('employees', uselist=True))
	
session=sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)	

def inserting():
	john = Employee(name='john')
	it_department = Department(name='IT')
	john.department = it_department
	s = session()
	s.add(john)
	s.add(it_department)
	s.commit()
	it = s.query(Department).filter(Department.name == 'IT').one()
	print(it.employees)
	print(it.employees[0].name)

def reading():
	s = session()
	find_it=select([Department.id]).where(Department.name == 'IT')
	print(type(find_it))
	rs = s.execute(find_it)
	print(rs)
	print(rs.fetchone())
	print(rs.fetchone())
	print(rs.fetchone())

reading()	