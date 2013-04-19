import os
import shlex
import datetime
import subprocess
from junit_xml import TestSuite, TestCase
from fabric.decorators import task

@task
def ramsey():
    """Run foodcritic and output the data as junit xml"""

    outFile = "junit.xml"
    cookbookPath = "cookbooks"

    if not os.path.isdir(cookbookPath):
        print "No valid cookbook found"
        return

    if not os.listdir(cookbookPath):
        print "No valid cookbooks found"
        return

    if os.path.exists(outFile):
        os.remove(outFile)

    testSuites = []
    for cookbook in os.listdir(cookbookPath):
        timestamp = datetime.datetime.now()
        cmd = "foodcritic %s/%s" % (cookbookPath, cookbook)
        p = subprocess.Popen(shlex.split(cmd), stdout = subprocess.PIPE)
        result = p.communicate()[0]

        # Find all failed tests
        failedTestCases = {}
        for line in result.split('\n'):
            if ":" not in line:
                continue

            testCaseId, testCaseExplanation = line.split(":", 1)
            testCase = TestCase(testCaseId)
            testCase.failure_message = testCaseExplanation
            failedTestCases[testCaseId] = testCase

        testCases = []
        for testCaseNumber in xrange(1, 46):
            testCaseId = "FC%.3d" % testCaseNumber
            if testCaseId not in failedTestCases:
                testCases.append(TestCase(testCaseId))
            else:
                testCases.append(failedTestCases[testCaseId])

        testSuites.append(TestSuite("Cookbook: %s" % cookbook, test_cases=testCases, timestamp=timestamp))
        print "Done with testcase for %s" % cookbook

    # output to file
    with open(outFile, 'w') as f:
        TestSuite.to_file(f, testSuites, prettyprint=False)

