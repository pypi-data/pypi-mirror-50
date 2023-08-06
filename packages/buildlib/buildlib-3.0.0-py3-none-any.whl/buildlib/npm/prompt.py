try:
    from mewo.term import prompt
except ImportError:
    import prmt as prompt


def should_push(
    dst: str,
    default: str = 'y',
    fmt=None,
) -> bool:

    return prompt.confirm(
        question=f'Do you want to PUSH package to {dst}?\n',
        default=default,
        fmt=fmt,
    )
