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
        if skip_depth is not None:
            if entry.depth <= skip_depth:
                yield entry
                skip_depth = None
        elif filt(entry):
            skip_depth = entry.depth
            continue
        else:
            yield entry


            
def inline(filt, seq):
    # TODO: normalization
    stack_trace = [] # pairs (depth, inlining or not)
    
    for entry in seq:
        depth = entry.depth
        while stack_trace and depth <= stack_trace[-1][0]:
            stack_trace.pop()

        is_inlining = filt(entry)

        p_depth, p_inlining = stack_trace[-1] if stack_trace else (None, False)

        if p_inlining or is_inlining and p_depth is not None:
            entry = entry.with_depth(p_depth)

        stack_trace.append((entry.depth, is_inlining))

        if not is_inlining:
            yield entry
            
                    

        
