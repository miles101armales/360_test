from enum import StrEnum, auto


class StepEnum(StrEnum):
	FIRST = auto()
	SECOND = auto()

class MessageStatusEnum(StrEnum):
	PENDING = auto()
	SENT = auto()
	FAILED = auto()