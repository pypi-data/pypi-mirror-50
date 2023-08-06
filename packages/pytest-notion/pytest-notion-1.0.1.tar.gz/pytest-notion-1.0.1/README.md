# notion-pytest-reporter
A PyTest Reporter to send test runs to Notion.so and enable bi-directional 
traceability.

![Example Test Cycle Report](https://github.com/Gimpneek/notion-pytest-reporter/raw/master/images/test-cycle.png)
Test Cycle Report - Shows Test Execution Results from run

![Example Test Execution](https://github.com/Gimpneek/notion-pytest-reporter/raw/master/images/test-execution.png)
Test Execution - Shows Stack trace if failed

![Example Test Case](https://github.com/Gimpneek/notion-pytest-reporter/raw/master/images/test-case.png)
Test Case - Shows Test Executions

## How it works
`notion-pytest-reporter` uses the unofficial Notion API to create new items in
the Test collection templates found here: [Test Report Template](https://www.notion.so/colinwren/Test-Reports-4415da888bf84457af49f18e9d25e62b)

For every test run `notion-pytest-reporter` will create a new Test Cycle and
within the Test Cycle create a Test Execution.

The Test Execution can be linked to a Test Case using the `@pytest.mark.notion_test(test_name)` decorator 
with the `test_name` argument being the title of the test case.

If a Test Case has been linked to a Test Execution then the Test Case page will
be updated to show that Test Execution allowing for bi-directional traceability
between the executed test and the test case.

If the Test Case is linked to a user story or specification then you'll
have bi-directional traceability between the tests and the user story!

## Running the reporter
The reporter takes the following arguments:

| Argument              | Description                                |
|-----------------------|--------------------------------------------|
| `--notion-token`      | API token used to authenticate with Notion |
| `--test-cycle-url`    | URL of the Test Cycle collection           |
| `--test-case-url`     | URL of the Test Case collection            |
| `--test-execution-url`| URL of the Test Execution collection       |
| `--test-cycle-name`   | Name to use for the Test Cycle             |

All arguments execpt `--test-cycle-name` are required for the reporter to run.

### Getting the Authentication Token and collections URLS
In order to get the authentication token used by the test reporter
you'll need to use the web version of Notion.

Once you've logged into Notion open the inspector panel on your web browser
and locate the cookie named `token_v2` - the value stored in that cookie is
authentication token.

The Test Cycle and Test Case URLs are simpler to extract. 

Right click the Test Cycle page in the side navigation and select `Copy Link` to
get the URL for the Test Cycle collection.

Right click the Test Cases page in the side navigation and select `Copy Link` to
get the URL for the Test Cases collection.

Right click the Test Executions page in the side navigation and select `Copy Link` to
get the URL for the Test Executions collection.
