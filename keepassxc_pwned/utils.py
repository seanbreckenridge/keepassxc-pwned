class AutoRepr:
    """
    Automatically creates a repr for a class given a list of attributes
    """

    # must have self.__class__.attrs set
    def __repr__(self) -> str:
        assert self.__class__.attrs is not None  # type: ignore

        return "{}({})".format(
            self.__class__.__name__,
            ", ".join(
                [
                    "{}={}".format(a, repr(getattr(self, a, None)))
                    for a in self.__class__.attrs  # type: ignore
                ]
            ),
        )

    def __str__(self) -> str:
        return self.__repr__()
