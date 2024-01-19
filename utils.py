from typing import TypedDict


class Arguments(TypedDict):
    end: str
    separator: bool


def custom_print(*args, **kwargs: Arguments):
    default_args = {"end": "\n", "separator": True}

    default_args.update(kwargs)

    if default_args["separator"]:
        print("-------------------------")

    print(*args, end=default_args["end"])
