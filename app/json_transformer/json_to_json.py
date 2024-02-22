from app.json_transformer.base_transformer import BaseTransformer


class JSONToJSON(BaseTransformer):
    """
    This utility class will convert json data into specified JSON format,
    nesting in JSON can be done as per the requirements
    """

    def transform(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        This function will convert json data into specified JSON format
        """
        data_dict = args[0]
        location_config = self.get_location_config()
        return self.apply_transformation(data_dict, location_config)