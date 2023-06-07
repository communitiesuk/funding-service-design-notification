import json
import uuid

from app.notification.model.notification_utils import convert_bool_value
from flask import current_app


class MultiInput:
    indent = " " * 5

    @classmethod
    def format_values(cls, value, index):
        """
        Format the given value based on the specified conditions.
        Args:
            value: The value to be formatted.
            index: The index of the value in the processing sequence.
        Returns:
            str: The formatted string representation of the value.
        """
        return f"{cls.indent}- {value}" if index != 1 else f"- {value}"

    @classmethod
    def format_keys_and_values(cls, key, value, index):

        """
        Format the given key-value pair based on specified conditions.
        Args:
            key: The key of the key-value pair.
            value: The value associated with the key.
            index: The index of the key-value pair in the processing sequence.
        Returns:
            str: The formatted string representation of the key-value pair.
        """

        def formatted_values(value):
            return (
                ", ".join(
                    map(
                        str,
                        convert_bool_value([value])
                        if len(value) > 1
                        else convert_bool_value(value),
                    )
                )
                if isinstance(value, list)
                else convert_bool_value(value)
            )

        return (
            f"{cls.indent}- {key}: {formatted_values(value)}"  # noqa
            if index != 1
            else (f"- {key}: {formatted_values(value)}")  # noqa
        )

    @classmethod
    def format_nested_data(cls, value):

        formatted_nested_values = []
        for inner_items in value:

            for k, v in inner_items.items():
                for iso_keys in ["date", "month", "year"]:
                    try:
                        if iso_keys in k.split("__"):
                            formatted_nested_values.append(f"{iso_keys}: {v}")
                            break

                    # handles all other nested multiple values
                    except:  # noqa
                        formatted_nested_values.append(
                            ", ".join(
                                map(
                                    lambda item: ", ".join(
                                        [f"{k}: {v}" for k, v in item.items()]
                                    ),
                                    value,
                                )
                            )
                        )
        return formatted_nested_values

    @classmethod
    def process_data(cls, data):
        """
        Process the data dictionary and generate a formatted output list.
        Args:
            data (dict): The dictionary to be processed.
        Returns:
            list: The formatted output list generated from the data.
        """
        output = []

        for index, (key, value) in enumerate(data.items(), start=1):

            # handles single value/answer containing uuid and excludes uuid key
            # & display the value only.
            try:
                if isinstance(key, str) and uuid.UUID(key, version=4):
                    output.append(cls.format_values(value, index))

            # handles multiple nested values containing year, month formatting and others
            except:  # noqa
                if (
                    isinstance(value, list)
                    and len(value) > 0
                    and isinstance(value[0], dict)
                ):
                    formatted_nested_values = cls.format_nested_data(value)
                    output.append(
                        f"{cls.indent}- {key}: {formatted_nested_values}"
                        if index != 1
                        else f"- {key}: {formatted_nested_values}"
                    )
                # handles all other multiple values
                else:
                    output.append(
                        cls.format_keys_and_values(key, value, index)
                    )

        return output

    @classmethod
    def map_multi_input_data(cls, multi_input_data):
        """
        Map the multi-input data to a sorted dictionary and process it.

        Args:
            multi_input_data (list): The list of dictionaries representing the multi-input data.

        Returns:
            str: The processed output as a formatted string.
        """
        try:

            key = None
            value = None
            sorted_data = {}
            for item in multi_input_data:
                if len(item) < 2:
                    for value in item.values():
                        key = str(uuid.uuid4())
                        sorted_data[key] = value
                else:
                    try:
                        key, *values = item.values()
                        sorted_data[key] = values
                    except TypeError:
                        value = tuple(item.values())
                        if isinstance(value[0], dict) and isinstance(
                            value[1], str
                        ):
                            *values, key = item.values()
                            sorted_data[key] = values
                    except:  # noqa
                        current_app.logger.error(
                            "Could not format the data correctly for"
                            f" {multi_input_data}"
                        )
                        key, *values = item.values()
                        sorted_data[json.dumps(key)] = values
            output = cls.process_data(sorted_data)
            return "\n".join(output)
        except Exception as e:
            current_app.logger.error(
                f"Error occurred while processing the multi input data: {e}"
            )
            current_app.logger.error(
                f"Couldn't map the multi input data for: {multi_input_data}"
            )
