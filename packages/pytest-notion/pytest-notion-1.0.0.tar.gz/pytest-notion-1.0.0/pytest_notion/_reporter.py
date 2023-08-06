from notion.client import NotionClient
from notion.collection import NotionDate
from notion.block import CollectionViewBlock
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)

CYCLE_COVER = 'https://images.unsplash.com/photo-1518623001395-125242310d0c?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb'
EXECUTION_COVER = 'https://images.unsplash.com/photo-1533738630286-f1f4a61705f8?ixlib=rb-1.2.1&q=85&fm=jpg&crop=entropy&cs=srgb'


class NotionReporter(object):
    def __init__(self, token, cycle_url, test_url, execution_url, cycle_name):
        logger.info('Inside NotionReporter')
        self.cycle_name = cycle_name
        self.notion = NotionClient(token_v2=token)
        self.cycles = self.notion.get_collection_view(cycle_url)
        self.tests = self.notion.get_collection_view(test_url)
        self.test_executions = self.notion.get_collection_view(execution_url)
        # Add test cycle
        self.cycle = self.cycles.collection.add_row(
            icon='🚴',
            name=cycle_name,
            date_executed=NotionDate(datetime.now()),
            execution_status='Unexecuted'
        )
        self.cycle.set('format.page_cover', CYCLE_COVER)
        self.cycle.set('format.page_cover_position', 0.5)

    def pytest_collection_modifyitems(self, config, items):
        for item in items:
            notion_marker = [mark for mark in item.own_markers if mark.name == 'notion_test']
            if notion_marker:
                test_case_name = notion_marker[0].args[0]
                test_cases = self.tests.build_query(search=test_case_name).execute()
                if test_cases:
                    item.user_properties.append(test_cases[0])

    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            test_execution = self.test_executions.collection.add_row(
                icon='🔫',
                name='{0} - {1}'.format(self.cycle_name, report.nodeid),
                date_executed=NotionDate(datetime.now()),
                executed_by=self.notion.current_user,
                test_cycle=self.cycle.id
            )
            test_execution.set('format.page_cover', EXECUTION_COVER)
            test_execution.set('format.page_cover_position', 0.5)
            if report.user_properties:
                test_execution.name = '{0} - {1}'.format(self.cycle_name, report.user_properties[0].title)
                test_execution.test_case = report.user_properties[0].id
            if report.passed:
                test_execution.status = 'Passed'
            if report.failed:
                test_execution.status = 'Failed'
                test_execution.notes = report.longreprtext

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        if exitstatus == 0:
            self.cycle.execution_status = 'Passed'
        if exitstatus == 1:
            self.cycle.execution_status = 'Failed'
        exec_records = self.test_executions.collection.get_rows()
        test_exec_prop = [item for item in exec_records[0].schema if item.get('slug') == 'test_cycle'][0]
        filter = [
            {
                'property': test_exec_prop.get('id'),
                'comparator': 'enum_contains',
                'value': self.cycle.id,
                'type': 'relation'
            }
        ]
        cvb = self.cycle.children.add_new(CollectionViewBlock)
        view = self.notion.get_collection_view(self.notion.create_record("collection_view", parent=cvb, type="board"), collection=self.test_executions.collection)
        view.set("collection_id", self.test_executions.collection.id)
        cvb.set("collection_id", self.test_executions.collection.id)
        cvb.set("view_ids", [view.id])
        cvb.title = "Test Executions"
        view.set('query.filter', filter)
