SEPARATOR = '\t'


def convert_array_to_string(array, sep=SEPARATOR, auto_type_caster=str):
    return sep.join(map(auto_type_caster, array))


def convert_string_to_array(string, sep=SEPARATOR, auto_type_caster=str):
    return list(map(auto_type_caster, string.split(sep)))
