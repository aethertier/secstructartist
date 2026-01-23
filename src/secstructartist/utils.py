from typing import Generator, Iterable, Tuple

def aggregate(x: Iterable[str], /) -> Generator[Tuple[str, int], None, None]:
    """
    Aggregate consecutive identical elements and count their occurrences.
    It yields tuples containing each distinct element and the number of times 
    it appears consecutively in the input.

    Parameters
    ----------
    x : Iterable[str]
        An iterable of strings. Consecutive identical elements are grouped
        together and counted.

    Yields
    ------
    tuple of (str, int)
        A tuple containing the element value and the count of its consecutive
        occurrences.
    """
    xiter = iter(x)
    try:
        xval, xcnt = next(xiter), 1
    except StopIteration:
        return
    for xi in xiter:
        if xi == xval:
            xcnt += 1
        else:
            yield xval, xcnt
            xval, xcnt = xi, 1
    yield xval, xcnt