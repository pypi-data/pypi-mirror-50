from . import property_exists_checker
from . import property_has_non_empty_value_checker
from . import property_has_value_equals_to_checker
from . import property_has_non_empty_array_value_checker
from . import property_array_value_size_checker

def getPropertyExistsChecker(data, field_name):
    return property_exists_checker.PropertyExistsChecker(data, field_name)

def getPropertyHasNonEmptyValueChecker(data, field_name):
    return property_has_non_empty_value_checker.PropertyHasNonEmptyValueChecker(data, field_name)

def getPropertyHasValueEqualsToChecker(data, field_name, field_value):
    return property_has_value_equals_to_checker.PropertyHasValueEqualsToChecker(data, field_name, field_value)

def getPropertyHasNonEmptyArrayValueChecker(data, field_name):
    return property_has_non_empty_array_value_checker.PropertyHasNonEmptyArrayValueChecker(data, field_name)

def getPropertyArrayValueSizeChecker(data, field_name, size):
    return property_array_value_size_checker.PropertyArrayValueSizeChecker(data, field_name, size)

