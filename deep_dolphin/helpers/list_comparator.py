class ListComparator(object):
    def __init__(self, list_a, list_b):
        self.list_a = list(map(lambda item: SpecialString(item), list_a))
        self.list_b = list(map(lambda item: SpecialString(item), list_b))
        self.common_length = min(len(list_a), len(list_b))

    def get_differences(self, tags_to_ignore=[]):
        differences = []

        for i in range(self.common_length):
            string_a = self.list_a[i]
            string_b = self.list_b[i]
            if (
                (string_a != string_b)
                and string_a.ommits(tags_to_ignore)
                and string_b.ommits(tags_to_ignore)
            ):
                differences.append("- " + string_a)
                differences.append("+ " + string_b)

        return differences


class SpecialString(str):
    def __init__(self, object):
        self.string = str(object)

    def ommits(self, tags):
        for tag in tags:
            if tag in self.string:
                return False
        return True
