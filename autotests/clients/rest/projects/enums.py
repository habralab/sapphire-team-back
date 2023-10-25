import enum


class ProjectStatusEnum(str, enum.Enum):
    PREPARATION = "preparation"
    IN_WORK = "in_work"
    FINISHED = "finished"


class ParticipantStatusEnum(str, enum.Enum):
    REQUEST = "request"
    DECLINED = "declined"
    JOINED = "joined"
    LEFT = "left"
