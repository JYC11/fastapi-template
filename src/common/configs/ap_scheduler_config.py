from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor  # type: ignore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore  # type: ignore
from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
from pytz import timezone

from src.common.configs.settings import settings

background_scheduler: BackgroundScheduler | None = None


jobstores = {
    "default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")
    # use an in memory scheduler for now, don't think ap scheduler supports asyncpg yet
}
executors = {"default": ThreadPoolExecutor(20), "processpool": ProcessPoolExecutor(5)}
job_defaults = {"coalesce": False, "max_instances": 3}


def background_scheduler_factory(jobstores: dict, executors: dict, job_defaults: dict):
    return BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone=timezone(settings.timezone),
    )


if settings.stage != "TEST":
    background_scheduler = background_scheduler_factory(
        jobstores=jobstores, executors=executors, job_defaults=job_defaults
    )
    assert background_scheduler is not None
else:
    background_scheduler = background_scheduler_factory(
        jobstores=jobstores, executors=executors, job_defaults=job_defaults
    )
    assert background_scheduler is not None
# in case if we need a different configuration for tests
