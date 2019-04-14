#!/usr/bin/python3

import argparse
import csv
import os
import subprocess
from collections import deque
from copy import deepcopy
from pathlib import Path


PROPERTY_NAME_INDEX = 0
PROPERTY_VALUES_INDEX = 1


class Precondition(object):
    def __init__(self, name, values):
        self.name = name
        self.values = values


class Trigger(object):
    def __init__(self, name, values):
        self.name = name
        self.values = values


class Postcondition(object):
    def __init__(self, name):
        self.name = name


def parseCommonProperty(line):
    namesAndValues = line.split(':')
    name = namesAndValues[PROPERTY_NAME_INDEX]
    values = namesAndValues[PROPERTY_VALUES_INDEX].split(',')
    values = [value.strip() for value in values]
    return (name, values)


def parsePrecondition(line):
    name, values = parseCommonProperty(line)
    return Precondition(name, values)


def parseTrigger(line):
    name, values = parseCommonProperty(line)
    return Trigger(name, values)


def parsePostcondition(line):
    return Postcondition(name=line)


class InputTemplate(object):
    def __init__(self, preconditions, triggers, postconditions):
        self.preconditions = preconditions
        self.triggers = triggers
        self.postconditions = postconditions


def parseInputTemplate(path):
    preconditions = []
    triggers = []
    postconditions = []
    with open(path) as file:
        for line in file.readlines():
            line = line.strip()
            if line == 'GIVEN':
                lineParser = parsePrecondition
                container = preconditions
            elif line == 'WHEN':
                lineParser = parseTrigger
                container = triggers
            elif line == 'THEN':
                lineParser = parsePostcondition
                container = postconditions
            else:
                container.append(lineParser(line))
    return InputTemplate(preconditions, triggers, postconditions)


def addEmptyFields(properties, row):
    emptyFieldsToAdd = len(properties) - 1
    while emptyFieldsToAdd:
        row.append('')
        emptyFieldsToAdd = emptyFieldsToAdd - 1


def generateGherkinHeaders(template):
    row = ['', 'GIVEN']
    addEmptyFields(template.preconditions, row)
    row.append('WHEN')
    addEmptyFields(template.triggers, row)
    row.append('THEN')
    return row


def generatePropertyHeaders(template):
    row = ['#AC']
    for precondition in template.preconditions:
        row.append(precondition.name)
    for trigger in template.triggers:
        row.append(trigger.name)
    for postcondition in template.postconditions:
        row.append(postcondition.name)
    return row


class Property(object):
    def __init__(self, values):
        self.values = values


def convertToProperties(template):
    properties = []
    for precondition in template.preconditions:
        properties.append(Property(precondition.values))
    for trigger in template.triggers:
        properties.append(Property(trigger.values))
    return properties


def generateValuesFor(propertyIndex, row, rows, properties):
    if propertyIndex == len(properties):
        rows.append(row)
        return

    property = properties[propertyIndex]
    for value in property.values:
        newRow = deepcopy(row)
        newRow.append(value)
        generateValuesFor(propertyIndex+1, newRow, rows, properties)


def generateValues(template):
    properties = convertToProperties(template)
    rows = []
    generateValuesFor(propertyIndex=0, row=deque(), rows=rows, properties=properties)
    for acNumber, row in enumerate(rows):
        row.appendleft(acNumber+1)
    return rows


def generateOutputTable(template):
    table = []
    table.append(generateGherkinHeaders(template))
    table.append(generatePropertyHeaders(template))
    for row in generateValues(template):
        table.append(row)
    return table


def fixOutputFileName(fileName):
    if fileName.endswith('.csv'):
        return fileName
    else:
        return fileName + '.csv'


def canSaveToFile(fileName, forceOverwrite):
    if os.path.exists(fileName):
        if Path(fileName).is_file():
            if forceOverwrite:
                return True
            else:
                print('Error: Output file {} already exists, use --force flag if you want to overwrite it.'.format(fileName))
                return False
        else:
            print('Error: Output path {} exists, but is not a file.')
            return False
    else:
        return True


def saveToFile(table, fileName, forceOverwrite):
    if not canSaveToFile(fileName, forceOverwrite):
        exit(1)

    with open(fileName, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in table:
            writer.writerow(row)


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i',
                        help='Path to input file with a template of acceptamce criteria. See examples/template.')
    parser.add_argument('--output', '-o',
                        help='Name of generated output file with a table of acceptance criteria, in CSV format.')
    parser.add_argument('--force-overwrite', '-f',
                        help='Overwrite generated output file if it already exists.', action="store_true")
    parser.add_argument('--open-output', '-p',
                        help='Automatically open output file in Libreoffice', action='store_true')
    args = parser.parse_args()

    inputPath = args.input
    if not inputPath:
        print("Error: Input path is missing.")
        parser.print_help()
        exit(1)

    outputFileName = args.output
    if not outputFileName:
        print("Error: Output file name is missing.")
        parser.print_help()
        exit(1)

    forceOverwrite = args.force_overwrite
    openOutput = args.open_output

    return (inputPath, outputFileName, forceOverwrite, openOutput)


def showOutputFile(fileName, openOutput):
    print('Acceptance criteria have been generated to file {}.'.format(fileName))
    if openOutput:
        subprocess.Popen(['/usr/bin/libreoffice', fileName])
        print('Libreoffice has been opened automatically.')
    else:
        print('You can open it with:\nlibreoffice {}\n'.format(fileName))
        print('(Hint: You can use --open-output or -p to open it automatically.)')


def main():
    inputPath, outputFileName, forceOverwrite, openOutput = parseArguments()
    outputFileName = fixOutputFileName(outputFileName)
    template = parseInputTemplate(inputPath)
    table = generateOutputTable(template)
    saveToFile(table, outputFileName, forceOverwrite)
    showOutputFile(outputFileName, openOutput)


if __name__ == '__main__':
    main()