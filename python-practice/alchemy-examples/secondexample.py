from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Department(Base):
	__tablename__ = 'department'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	employees = relationship('Employee', secondary='department_employee')


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    departments = relationship('Department', secondary='department_employee')

class DepartmentEmployee(Base):
    __tablename__ = 'department_employee'
    department_id = Column(Integer, ForeignKey('department.id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///E:/files/python/chinook.db')
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


s = session()
john = Employee(name='john')
s.add(john)
it_department = Department(name='IT')
it_department.employees.append(john)
s.add(it_department)
s.commit()


marry = Employee(name='marry')
financial_department = Department(name='financial')
financial_department.employees.append(marry)
s.add(marry)
s.add(financial_department)
s.commit()
 
it = s.query(Department).filter(Department.name == 'IT').one()
s.refresh(marry)
s.refresh(it)
print(it.employees)
it.employees.append(marry)
s.commit()
print(it.employees)