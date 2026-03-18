from typing import TypedDict


class HumanStage(TypedDict):
    """
    Human-like definition of a stage.

    Example:
    ```python
    HumanStage(duration='1m', users=10, spawn_rate=10)
    ```
    """

    duration: str
    users: int
    spawn_rate: float


class LocustStage(TypedDict):
    """
    Locust-like definition of a stage.

    Example:
    ```python
    LocustStage(duration=60, users=10, spawn_rate=10)
    ```
    """

    duration: int
    users: int
    spawn_rate: float


def _handle_duration(duration: str, total: int) -> tuple[int, int]:
    """
    Processes a duration string and a partial total in seconds and final total

    Parses the string into the integer value:
    - "10s" -> 10
    - "10m" -> 10 * 60
    - "10h" -> 10 * 3600

    Returning, for instance, 9600 if `duration` is "2h40m".

    :param duration: String formatted as shown above
    :type duration: str
    :param total: Intefer to be add to the parsed `duration`
    :type total: int
    :return: Tupla contendo `total` somado à `duration` convertido em segundos.
    :return: Tuple with `total` plus `duration` in seconds.
    :rtype: tuple[int, int]
    """

    new_duration: int = 0

    if 's' in duration:
        new_duration = int(duration[:-1])

    elif 'm' in duration:
        if duration.endswith('m'):
            new_duration = int(duration[:-1]) * 60
        else:
            m, s = duration.split('m')
            new_duration = (int(m) * 60) + int(s)

    elif 'h' in duration:
        if duration.endswith('h'):
            new_duration = int(duration[:-1]) * 3600
        else:
            h, m = duration.split('h')
            new_duration = (int(h) * 3600) + (int(m) * 60)

    r_data: int = new_duration + total

    return r_data, r_data


def handle_stages(*stages: HumanStage) -> list[LocustStage]:
    """
    Transforms a list of `HumanStage` into `list[LocustStage]`

    Receiving a list of HumanStage by the `*args` strategy, it performs a for-loop
    on each stage provided, converting them to the format expected by Locust
    using `_handle_duration` for this task.

    ```python
    handle_stages(
        HumanStage(duration='2m', users=250, spawn_rate=25 / 12),
        HumanStage(duration='2m', users=250, spawn_rate=25 / 12),
    )
    # [
    #     {'duration': '2m', 'users': 250, 'spawn_rate': 25 / 12},
    #     {'duration': '2m', 'users': 250, 'spawn_rate': 25 / 12},
    # ]
    ```

    :param *stages: HumanStage iterable for convertion
    :type *stages: HumanStage
    :return: List of converted values LocustStage
    :rtype: list[LocustStage]
    """

    output: list[LocustStage] = []
    total: int = 0

    for stage in stages:
        duration: str = str(stage['duration'])
        new_duration, total = _handle_duration(duration, total)

        output.append(
            LocustStage(
                duration=new_duration,
                users=stage['users'],
                spawn_rate=stage['spawn_rate'],
            )
        )

    return output
