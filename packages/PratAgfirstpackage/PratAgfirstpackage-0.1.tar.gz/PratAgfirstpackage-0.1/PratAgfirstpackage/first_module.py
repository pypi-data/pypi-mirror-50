class Name:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def age_next(self):
        return self.age + 10

    def name_len(self):
        return 'Length of name is {}'.format(len(self.name))


class Education(Name):
    def __init__(self, name, age, school, btech, ms):
        Name.__init__(self, name, age)
        self.school = school
        self.btech = btech
        self.ms = ms

    def get_edu_info(self):
        return'{} is the name of the school'.format(self.school), \
              '{} is the name of the undergrad college'.format(self.btech),\
            '{} is the name of the grad college'.format(self.ms), '{} is the name of the person.'.format(self.name),\
              '{} is the age of the person'.format(self.age)


print ("Hey!")
