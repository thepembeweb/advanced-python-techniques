class NEODatabase:
    def __init__(self, neos, approaches):
        self._neos = neos
        self._approaches = approaches
        self._neo_designation_map = {neo.designation: neo for neo in self._neos}
        self._neo_name_map = {neo.name: neo for neo in self._neos}

        for item in self._approaches:
            if self._neo_designation_map.get(item._designation):
                item.neo = self._neo_designation_map[item._designation]
                self._neo_designation_map[item._designation].approaches.append(item)


    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        return self._neo_designation_map.get(designation)

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        return self._neo_name_map.get(name)

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for item in self._approaches:
            if all(f(item) for f in filters):
                yield item
