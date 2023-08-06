'''
Storage for common doc strings and templates shared in non-related classes and methods.
'''


import typing as tp

from static_frame.core.util import AnyCallable


class DOC_TEMPLATE:

    #---------------------------------------------------------------------------
    # functions

    to_html = '''
    Return an HTML table representation of this {class_name} using standard TABLE, TR, and TD tags. This is not a complete HTML page.

    Args:
        config: Optional :py:class:`static_frame.DisplayConfig` instance.
    '''

    to_html_datatables = '''
    Return a complete HTML representation of this {class_name} using the DataTables JS library for table naviagation and search. The page links to CDNs for JS resources, and thus will not fully render without an internet connection.

    Args:
        fp: optional file path to write; if not provided, a temporary file will be created. Note: the caller is responsible for deleting this file.
        show: if True, the file will be opened with a webbrowser.
        config: Optional :py:class:`static_frame.DisplayConfig` instance.

    Returns:
        Absolute file path to the file written.
    '''

    clip = '''Apply a clip opertion to this {class_name}. Note that clip operations can be applied to object types, but cannot be applied to non-numerical objects (e.g., strings, None)'''

    ufunc_skipna = '''{header}

    Args:
        axis: Axis, defaulting to axis 0.
        skipna: Skip missing (NaN) values, defaulting to True.
    '''

    #---------------------------------------------------------------------------
    # dict entries

    reindex = dict(
            count='''Positive integer values drop that many outer-most levels; negative integer values drop that many inner-most levels.'''
            )

    index_init = dict(
            args = '''
        Args:
            labels: Iterable of hashable values to be used as the index labels. If an Index or IndexHierarchy class is passed, values will be appropriately extracted.
            name: A hashable object to name the Index.
            loc_is_iloc: Optimization when a contiguous integer index is provided as labels. Generally only set by internal clients.
            dtype: Optional dtype to be used for labels.'''
            )

    index_date_time_init = dict(
            args = '''
        Args:
            labels: Iterable of hashable values to be used as the index labels. If strings, NumPy datetime conversions will be applied.
            name: A hashable object to name the Index.
            '''
            )

    from_pandas = dict(
            own_data='''own_data: If True, the underlying NumPy data array will be made immutable and used without a copy.''',
            own_index='''own_index: If True, the underlying NumPy index label array will be made immutable and used without a copy.''',
            own_columns='''own_columns: If True, the underlying NumPy column label array will be made immutable and used without a copy.''',
            )

    container_init = dict(
            index='''index: Optional index initializer. If provided in addition to data values, lengths must be compatible.''',
            columns='''columns: Optional column initializer. If provided in addition to data values, lengths must be compatible.
            ''',
            own_index='''own_index: Flag passed index as ownable by this {class_name}. Primarily used by internal clients.''',
            own_data='''own_data: Flag the data values as ownable by this {class_name}. Primarily used by internal clients.''',
            own_columns='''own_columns: Flag passed columns as ownable by this {class_name}. Primarily used by internal clients.'''
    )

    constructor_frame = dict(
            dtypes='''dtypes: Optionally provide an iterable of dtypes, equal in length to the length of each row, or a mapping by column name. If a dtype is given as None, NumPy's default type determination will be used.
            ''',
            name='name: A hashable object to name the Frame.',
            consolidate_blocks='consolidate_blocks: Optionally consolidate adjacent same-typed columns into contiguous arrays.'
    )

    fillna = dict(
            limit='limit: Set the maximum count of missing values (NaN or None) to be filled per contiguous region of missing vlaues. A value of 0 is equivalent to no limit.',
            value='value: Value to be used to replace missing values (NaN or None).',
            axis='axis: Axis upon which to evaluate contiguous missing values, where 0 is vertically (between row values) and 1 is horizontally (between column values).'
    )



def doc_inject(*,
        selector: tp.Optional[str] = None,
        **kwargs: object
        ) -> tp.Callable[[AnyCallable], AnyCallable]:
    '''
    Args:
        selector: optionally specify name of doc template dictionary to use; if not provided, the name of the function will be used.
    '''
    def decorator(f: AnyCallable) -> AnyCallable:

        assert f.__doc__ is not None, f'{f} must have a docstring!'

        nonlocal selector
        selector = f.__name__ if selector is None else selector
        # get doc string, template with decorator args, then template existing doc string
        doc_src = getattr(DOC_TEMPLATE, selector)
        if isinstance(doc_src, str):
            doc = doc_src.format(**kwargs)
            f.__doc__ = f.__doc__.format(doc)
        else: # assume it is a dictionary
            # try to format each value
            doc_dict = {k: v.format(**kwargs) for k, v in doc_src.items()}
            f.__doc__ = f.__doc__.format(**doc_dict)

        return f

    return decorator
