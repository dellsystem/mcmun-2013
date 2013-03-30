"""
Parses the CCM (including assignments)
Changes made to the csv:

* got rid of accents in 258, 147, 146
* Exxon Mobile --> Exxon Mobil
* Latin American Tissue Banking Association
* Medicines -> Medicines
* replaced commas (in character titles) with semicolons because
  seriously, using commas as both delimiters and as punctuation?
  NOT COOL
* and a bunch more. Worst spreadsheet ever. Never again
"""
import csv
import json

schools = json.load(open('schools.json'))
committees = json.load(open('committees.json'))
joints = json.load(open('joints.json')) # lol

assignment_list = []
num_assignments = 0
total_num_delegates = 0

def create_assignment(school_name, committee_name, assignment):
    #print "Creating assignment for %s, %s, %s" % (school_name, committee_name, assignment)
    global num_assignments, assignment_list, total_num_delegates
    num_assignments += 1

    # Only SOCHUM and WHS are double-delegate committees
    num_delegates = 2 if committee_name in ('SOCHUM', 'WHS ') else 1
    total_num_delegates += num_delegates

    # If the committee is in a joint crisis (awoc, nixon, rwanda),
    # add the specific side to the assignment
    if committee_name in joints:
        assignment += " (" + str(joints[committee_name]) + ")"

    school_id = schools[school_name]
    committee_id = committees[committee_name]
    assignment_list.append({
        'pk': num_assignments,
        'model': 'committees.committeeassignment',
        'fields': {
            'school': school_id,
            'assignment': assignment,
            'notes': '',
            'position_paper': '',
            'committee': committee_id,
            'num_delegates': num_delegates,
        }
    })

reader = csv.reader(open('ccm.csv', 'rb'))
header = None

for i, row in enumerate(reader):
    # Skip the header row
    if i > 0:
        school = row[0]
        total = int(row[-1])

        # Ignore schools with no assignments
        if total > 0:
            # Get the assignments for each committee
            for j in xrange(2, 54, 2):
                committee_name = header[j]
                num_assigned = int(row[j]) if row[j] else 0
                assignments = row[j+1]
                if num_assigned > 0:
                    num_expected = len(assignments.split(','))
                    if num_assigned != num_expected and num_assigned != num_expected*2:
                        print school
                        print "PROBLEM"
                        print assignments
                    for assignment in assignments.split(','):
                        # Replace semicolons with commas (like escaping lol)
                        assignment = assignment.strip().replace(';', ',')
                        if assignment:
                            create_assignment(school, committee_name, assignment)
    else:
        header = row

# Write out the assignments to some file
json.dump(assignment_list, open('committees/fixtures/initial_data.json', 'w'),
    indent=4)

print "Total number of delegates:",
print total_num_delegates
