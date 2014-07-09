#### Imports ####
from traits.api import HasTraits, Str, Int
from jigna.api import Template, QtApp

#### Domain model ####

class Employee(HasTraits):
    name = Str
    salary = Int

    def update_salary(self):
        self.salary += int(0.2*self.salary)

employee = Employee(name='Tom', salary=2000)

#### UI layer ####

body_html = """
  Employee name is {{employee.name}} <br/>
  Salary is ${{employee.salary}} <br/>

  <button ng-click='employee.update_salary()'>
    Update salary
  </button>
"""
template = Template(body_html=body_html, recommended_size=(250, 100))

#### Entry point ####

def main():
    app = QtApp(template=template, context={'employee': employee})
    app.start()

if __name__ == '__main__':
    main()