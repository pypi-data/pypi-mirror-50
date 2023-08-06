# system modules
import logging
import threading
import copy
import functools
import datetime
import collections

# internal modules

# external modules

logger = logging.getLogger(__name__)


class StorageQueue(collections.deque):
    @property
    def lock(self):
        try:
            return self._lock
        except AttributeError:
            self._lock = threading.Lock()
        return self._lock

    @property
    def bundle_interval(self):
        return getattr(self, "_bundle_interval", 0)

    @bundle_interval.setter
    def bundle_interval(self, interval):
        self._bundle_interval = float(interval)

    def locked(decorated_function):
        """
        Decorator for methods that should be locked with UploadQueue.lock
        """

        @functools.wraps(decorated_function)
        def wrapper(self, *args, **kwargs):
            with self.lock:
                return decorated_function(self, *args, **kwargs)

        return wrapper

    def log_queue_len(self):
        logger.debug("Now {n} datasets are queued".format(n=len(self)))

    @property
    @locked
    def old_datasets(self):
        """
        Generator yielding datasets from the queue that don't lie within the
        :any:`bundle_interval` anymore.

        .. note::


        """
        try:
            skipped = list()
            while self:
                ds = self.popleft()
                if (
                    datetime.datetime.utcnow().replace(
                        tzinfo=datetime.timezone.utc
                    )
                    - ds[0]
                ).total_seconds() > self.bundle_interval:
                    logger.debug(
                        "Dataset {dataset} doesn't lie "
                        "within the bundle interval of {interval:.2f} "
                        "seconds anymore".format(
                            dataset=ds, interval=self.bundle_interval
                        )
                    )
                    yield ds
                else:
                    logger.debug(
                        "Dataset {dataset} still lies "
                        "within the bundle interval of {interval:.2f} "
                        "seconds. Remembering it for re-queueing.".format(
                            dataset=ds, interval=self.bundle_interval
                        )
                    )
                    skipped.append(ds)
        finally:
            for ds in skipped:
                logger.debug(
                    "Re-queueing previously remembered dataset "
                    "{} which lied within the bundle interval".format(ds)
                )
                self.appendleft(ds)

    @property
    @locked
    def dataset(self):
        """
        Generator yielding the next queued dataset and removing it from the
        queue
        """
        while self:
            logger.debug("Retrieving a queued dataset")
            ds = self.popleft()
            self.log_queue_len()
            yield ds

    @locked
    def add(self, dataset, dataset_time=None, prioritized=False):
        """
        Queue another dataset as tuple ``(now, dataset)``, where ``now`` is the
        current :any:`datetime.datetime.utcnow` with the timezone set to
        :any:`datetime.timezone.utc`.

        Args:
            dataset (dict): the dataset to queue. Dict structured like
                ``dataset["table1"]["column1"] = value`` with an arbitrary
                number of tables and columns
            dataset_time (datetime.datetime, optional): the time of the dataset
            prioritized (bool, optional): if ``True``, insert at the
                prioritized side of the queue.
        """
        if not dataset_time:
            dataset_time = datetime.datetime.utcnow().replace(
                tzinfo=datetime.timezone.utc
            )
        if self.bundle_interval > 0:
            dataset = copy.deepcopy(dataset)
            for n, (queued_time, queued_dataset) in enumerate(self):
                seconds_queued = (dataset_time - queued_time).total_seconds()
                if seconds_queued > self.bundle_interval:
                    continue
                logger.debug(
                    "Queued dataset Nr. {n} ({dataset}) "
                    "has been queued for "
                    "{seconds:.2f} seconds, which is within "
                    "the bundle inverval of {interval} seconds".format(
                        n=n,
                        seconds=seconds_queued,
                        dataset=queued_dataset,
                        interval=self.bundle_interval,
                    )
                )
                for table, column_data in copy.deepcopy(dataset).items():
                    queued_dataset.setdefault(table, {})
                    queued_table = queued_dataset[table]
                    for column, value in column_data.items():
                        if column in queued_table:
                            continue
                        logger.debug(
                            "Table {table} ({table_dict}) of queued "
                            "dataset Nr. {n} ({dataset}) "
                            "doesn't have a {column} column yet, so "
                            "we fill it with our value {value}".format(
                                n=n,
                                dataset=queued_dataset,
                                column=repr(column),
                                table=repr(table),
                                table_dict=queued_table,
                                value=value,
                            )
                        )
                        queued_table[column] = dataset[table].pop(column)
                    if not dataset[table]:
                        dataset.pop(table)
            if dataset:
                if not self:
                    logger.warning(
                        "Couldn't sort this remaining data into "
                        "recent queued datasets, "
                        "adding to the queue: {dataset}".format(
                            dataset=dataset
                        )
                    )
        if dataset:
            (self.appendleft if prioritized else self.append)(
                (dataset_time, dataset)
            )
        self.log_queue_len()
