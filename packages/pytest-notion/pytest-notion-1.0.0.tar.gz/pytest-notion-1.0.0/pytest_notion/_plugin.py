from ._reporter import NotionReporter
from datetime import datetime


def pytest_addoption(parser):
    group = parser.getgroup('terminal reporting')
    group.addoption(
        '--notion-token',
        dest='notion_token',
        action='store',
        type=str,
        default=None,
        help='Notion API Token (see README for details on how to extract)'
    )
    group.addoption(
        '--test-cycle-url',
        dest='notion_test_cycle_url',
        action='store',
        type=str,
        default=None,
        help='URL for the Test Cycle Collection'
    )
    group.addoption(
        '--test-case-url',
        dest='notion_test_case_url',
        action='store',
        type=str,
        default=None,
        help='URL for the Test Case Collection'
    )
    group.addoption(
        '--test-execution-url',
        dest='notion_test_execution_url',
        action='store',
        type=str,
        default=None,
        help='URL for the Test Execution Collection'
    )
    group.addoption(
        '--test-cycle-name',
        dest='notion_test_cycle_name',
        action='store',
        type=str,
        default='PyTest - {0}'.format(datetime.now().strftime('%Y-%m-%d')),
        help='Name to use for the test cycle'
    )


def pytest_configure(config):
    token = config.option.notion_token
    cycle_url = config.option.notion_test_cycle_url
    case_url = config.option.notion_test_case_url
    execution_url = config.option.notion_test_execution_url
    cycle_name = config.option.notion_test_cycle_name
    config.addinivalue_line('markers', 'notion_test(name): Name of test case')
    if token and cycle_url and case_url and execution_url:
        config._notion_reporter = NotionReporter(token, cycle_url, case_url, execution_url, cycle_name)
        config.pluginmanager.register(config._notion_reporter)


def pytest_unconfigure(config):
    notion_reporter = getattr(config, '_notion_reporter', None)
    if notion_reporter:
        del config._notion_reporter
        config.pluginmanager.unregister(notion_reporter)
