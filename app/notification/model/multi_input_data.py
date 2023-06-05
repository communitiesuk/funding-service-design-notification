import uuid

from app.notification.model.notification_utils import convert_bool_value


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
        return f"{cls.indent}. {value}" if index != 1 else f". {value}"

    @classmethod
    def formatted_values(cls, value):
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

        return (
            f"{cls.indent}. {key}: {cls.formatted_values(value)}"  # noqa
            if index != 1
            else (f". {key}: {cls.formatted_values(value)}")  # noqa
        )

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

            # handles multiple nested values containing year, month formatting
            except:  # noqa
                if (
                    isinstance(value, list)
                    and len(value) > 0
                    and isinstance(value[0], dict)
                ):
                    formatted_value = []
                    for inner_items in value:

                        for k, v in inner_items.items():
                            for iso_keys in ["date", "month", "year"]:
                                try:
                                    if iso_keys in k.split("__"):

                                        formatted_value.append(
                                            f"{iso_keys}: {v}"
                                        )
                                        break

                                # handles all other nested multiple values
                                except:  # noqa

                                    formatted_value.append(
                                        ", ".join(
                                            map(
                                                lambda item: ", ".join(
                                                    [
                                                        f"{k}: {v}"
                                                        for k, v in item.items()
                                                    ]
                                                ),
                                                value,
                                            )
                                        )
                                    )
                    output.append(
                        f"{cls.indent}. {key}: {formatted_value}"
                        if index != 1
                        else f". {key}: {formatted_value}"
                    )
                # handles all other multiple values
                else:
                    output.append(
                        cls.format_keys_and_values(key, value, index)
                    )

        return output
