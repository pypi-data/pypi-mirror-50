import logging
from time import time
from concurrent.futures import ThreadPoolExecutor
from azure.cosmosdb.table.tableservice import TableService


class AzureTableStorageHandler(logging.Handler):
    """
    A handler class which writes formatted logging records to Azure Table Storage.
    """
    def __init__(self, account_name, account_key, table_name, *, level=logging.NOTSET):
        """
        Setup TableService and the specified table for logging.
        """
        super().__init__(level=level)
        self.table_service = TableService(account_name=account_name, account_key=account_key)
        self.table_name = table_name
        if not self.table_service.exists(self.table_name):
            self.table_service.create_table(self.table_name)
        self.formatter = logging.Formatter("%(message)s")
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="AzHndlr")

    def insert_log(self, record):
        """
        Insert log to Azure Table Storage.
        """
        entity = {
            "PartitionKey": record.name,
            "RowKey": str(time()),
            "LocalTimestamp": self.formatter.formatTime(record),
            "LevelName": record.levelname,
            "Level": record.levelno,
            "Message": self.format(record)
        }
        self.table_service.insert_entity(self.table_name, entity)

    def emit(self, record):
        """
        Emit a record.

        This method just submit the logging task to worker thread and return immediately.
        """
        self.executor.submit(self.insert_log, record)
