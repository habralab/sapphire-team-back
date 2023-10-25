import enum


class ProjectStatusEnum(str, enum.Enum):
    PREPARATION = "preparation"
    IN_WORK = "in_work"
    FINISHED = "finished"
