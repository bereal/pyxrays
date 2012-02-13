
def fold(filt, seq):
    skip_depth = None
    for entry in seq:
        if skip_depth:
            depth = entry.depth
            if depth <= skip_depth:
                yield entry
                skip_depth = None
                continue
        elif filt(entry):
            skip_depth = entry.depth
            yield entry
            continue
        else:
            yield entry


def prune(filt, seq):
    skip_depth = None
    for entry in seq:
        if skip_depth:
            if entry.depth <= skip_depth:
                yield entry
                skip_depth = None
        elif not filt(entry):
            skip_depth = entry.depth
            continue
        else:
            yield entry


