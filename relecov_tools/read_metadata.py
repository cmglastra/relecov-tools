#!/usr/bin/env python

class ReadMetadata():
    def __init__():
        self.origin_file = file
        slef.metadata = {}


# reade_metadata
def read_metadata_workflow(self):
    def __init__ (self, ):

    '''
    Description :   Starts the read metada workflow
    '''

    # Perform workflow details

wb_file = openpyxl.load_workbook(arguments.inputFile, data_only=True)
ws_metadata_lab = wb_file['METADATA_LAB']
heading = []
for cell in ws_metadata_lab[1]:
    heading.append(cell.value)


for row in islice(ws_metadata_lab.values,1,ws_metadata_lab.max_row):
    sample_data_row = {}
    for idx in range(len(heading)):
        if 'date' in heading[idx]:
            sample_data_row[heading[idx]] = row[idx].strftime('%d/%m/%Y')
        else:
            sample_data_row[heading[idx]] = row[idx]
    try:
        validate(instance=sample_data_row,schema=json_phage_plus_schema)
    except:
        print('Unsuccessful validation for sample ' , sample_data_row['sample_name'])

        continue
