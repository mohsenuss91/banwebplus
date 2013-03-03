import re
import banweb_terms

# given a course from a sem_[0-9]+.py file, it will verify that the course is valid
def courseIsValid(course):
    for index in [u'Enroll', u'Seats', u'Hrs', u'CRN', u'Limit']:
        if not re.search('\-?[0-9]+', course[index]):
            #print index
            return False
    if not re.search('[\ U][\ M][\ T][\ W][\ R][\ F][\ S]', course[u'Days']):
        if course[u'Days'] != ' ':
            #print u'Days'
            return False
    if not re.search('[A-Z]+[\ ]+[0-9]+', course[u'Course']):
        #print u'Course'
        return False
    if u'Time' in course:
        if not re.search('[0-9]+\-[0-9]+', course[u'Time']):
            #print u'Time'
            return False
    else:
        course[u'Time'] = '';
    return True

# translates the given python file into something that php can understand
def translate_file(filename):
    m = __import__(filename)
    fout = file(filename+".php", "w")
    fout.write("<?php\n")
    fout.write("class semesterData() {\n")
    
    fout.write("\t$name = "+m.name+";\n")
    fout.write("\t$subjects = array(\n")
    for subject in m.subjects:
        fout.write("\t\t'"+subject[0]+"'=>'"+subject[1]+"';\n")
    fout.write("\t);\n")
    fout.write("\t$classes = array(\n")
    
    subject_index = 0
    for subject in m.classes:
        for course in subject:
            if not courseIsValid(course):
                print course
                print ''
                continue
            fout.write("\t\tarray(\n");
            fout.write("\t\t\t'subject'=>'"+m.subjects[subject_index][0]+"'")
            for part in course:
                fout.write(",\n\t\t\t'"+part+"'=>'"+course[part].replace("'", "")+"'")
            fout.write("\n\t\t),\n")
        subject_index += 1
    
    fout.write("\t);\n")
    fout.write("}\n")
    fout.write("?>\n")
    fout.close()

def main():
    filenames = []
    
    for term in banweb_terms.terms:
        semester = term[0]
        filenames.append("sem_"+semester)
    
    fout = file("banweb_terms.php", "w")
    fout.write("<?php\n")
    fout.write("$terms = array();\n")
    for term in banweb_terms.terms:
        fout.write("terms[] = array('")
        first = True
        for part in term:
            if (first):
                first = False
            else:
                fout.write(',')
            fout.write(part)
    fout.write("?>\n");
    
    for filename in filenames:
        translate_file(filename)

if __name__ == '__main__':
    main()