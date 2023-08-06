try:
    from mewo.term import prompt
except ImportError:
    import prmt as prompt


def should_bump_version(
    default: str = 'y',
    fmt=None,
) -> bool:

    return prompt.confirm(
        question='BUMP VERSION number?\n',
        default=default,
        fmt=fmt,
    )
