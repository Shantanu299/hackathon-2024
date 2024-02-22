from abc import abstractmethod
import copy


class BaseTransformer:
    def __init__(self, json_builder_config):
        """
        :param json_builder_config: json format configuration, this will be a json
        """
        self.json_builder_config = json_builder_config

    @property
    def json_builder_config(self):
        return self._json_builder_config

    @json_builder_config.setter
    def json_builder_config(self, value):
        if not value:
            raise ValueError("json_builder_config is required to proceed")
        self._json_builder_config = value

    def apply_transformation(self, row_dict, location_config):
        """
        This function prepares value to be substituted in json format for each field wherever
        we have lambda function defined and do substitution as well.
        :param row_dict: dictionary of a row
        :param location_config: mapping between location and transformation function
        """
        json_template = copy.deepcopy(self.json_builder_config)
        transformed_values = []
        for location, transformation_func in location_config.items():
            value = transformation_func(row_dict)
            transformed_values.append(value)
            latest_ref = json_template
            for location_element in location[:-1]:
                latest_ref = latest_ref[location_element]
            latest_ref[location[-1]] = value
        return json_template, transformed_values

    def get_location_config(self):
        """
        This function will provide the location path mapping with the provided lambda functions.
        As each field can have its own lambda function configured, so this mapping basically
        tells at which location path in JSON we need to apply what transformation function to
        prepare data for a particular field.

        Input eg: ->
        json_builder_config = {
            "fields": [
                {
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            lambda row_dict: float(row_dict['long']),
                            lambda row_dict: float(row_dict['lat']),
                        ]
                    },
                    "crop": lambda row_dict: row_dict['Crop'].upper(),
                    "planting_date": lambda row_dict: row_dict['planting_date']
                }
            ]
        }
        Output eg: ->
        location_config = {
            ('fields', 0, 'geometry', 'coordinates', 0): lambda row_dict: float(row_dict['long']),
            ('fields', 0, 'geometry', 'coordinates', 1): lambda row_dict: float(row_dict['lat']),
            ('fields', 0, 'crop'): lambda row_dict: row_dict['Crop'].upper(),
            ('fields', 0, 'planting_date'): lambda row_dict: row_dict['planting_date']
        }
        """
        location_config = {}

        def _build_location_config(config_dict, location):
            for key, value in config_dict.items():
                location.append(
                    key
                )  # appending keys wherever we traverse in config_dict
                if callable(value):
                    # if we found callable object in config_dict that means at this location we
                    # have specified our transformation function that is nothing but a lambda
                    # function, we need to tag the location of this transformation function in
                    # location_config.
                    # eg: location_config = {
                    #       ('fields', 0, 'crop'): lambda row_dict: row_dict['Crop'].upper()
                    # }
                    location_tuple = tuple(location)
                    location_config[location_tuple] = copy.deepcopy(value)

                if isinstance(value, dict):
                    # if we found dictionary in nesting, then re-iterate on nested one again,
                    # to check whether we have callable function down at somewhere
                    _build_location_config(value, location)
                elif isinstance(value, list):
                    # if we found list in nesting, then iterate on this list
                    for index, obj in enumerate(value):
                        # # appending indexes wherever we traverse in list
                        location.append(index)
                        if callable(obj):
                            # if we found callable object in list that means at this location
                            # we have specified our transformation function that is nothing but a
                            # lambda function, we need to tag the location of this transformation
                            # function in location_config.
                            # eg: location_config = {
                            #       ('fields', 0, 'geometry', 'coordinates', 0): lambda row_dict:
                            #                          float(row_dict['long'])
                            # }
                            location_tuple = tuple(location)
                            location_config[location_tuple] = copy.deepcopy(obj)
                        elif isinstance(obj, dict):
                            # if we found dictionary in nesting, then re-iterate on nested one
                            # again to check whether we have callable function down at
                            # somewhere
                            _build_location_config(obj, location)
                        if location:
                            # pop from location so that we can trace the location of next
                            # transformation function that may present at another index
                            location.pop()
                if location:
                    # pop from location so that we can trace the location of next transformation
                    # function that may present at another key in config_dict
                    location.pop()

        _build_location_config(self.json_builder_config, [])
        return location_config

    @abstractmethod
    def transform(self, *args, **kwargs):
        """
        This function will call respective transformation and will provide transformed
        data in JSON
        """
        raise NotImplementedError
