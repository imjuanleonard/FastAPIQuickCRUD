from copy import deepcopy


def filter_none(request_or_response_object):
    received_request = deepcopy(request_or_response_object.__dict__)
    if 'insert' in received_request:
        insert_item_without_null = []
        for received_insert in received_request['insert']:
            received_insert_ = deepcopy(received_insert)
            for received_insert_item, received_insert_value in received_insert_.__dict__.items():
                if hasattr(received_insert_value, '__module__'):
                    if received_insert_value.__module__ == 'fastapi.params' or received_insert_value is None:
                        delattr(received_insert, received_insert_item)
                elif received_insert_value is None:
                    delattr(received_insert, received_insert_item)

            insert_item_without_null.append(received_insert)
        setattr(request_or_response_object, 'insert', insert_item_without_null)
    else:
        for name, value in received_request.items():
            if hasattr(value, '__module__'):
                if value.__module__ == 'fastapi.params' or value is None:
                    delattr(request_or_response_object, name)
            elif value is None:
                delattr(request_or_response_object, name)


def value_of_list_to_str(cls, columns):
    if isinstance(columns, str):
        columns = [columns]
    request_or_response_object = cls
    received_request = deepcopy(request_or_response_object.__dict__)
    if 'insert' in request_or_response_object.__dict__:
        insert_str_list = []
        for insert_item in request_or_response_object.__dict__['insert']:
            for column in columns:
                for insert_item_column, _ in insert_item.__dict__.items():
                    if column in insert_item_column:
                        value_ = insert_item.__dict__[insert_item_column]
                        if value_ is not None:
                            if isinstance(value_, list):
                                str_value_ = [str(i) for i in value_]
                            else:
                                str_value_ = str(value_)
                            setattr(insert_item, insert_item_column, str_value_)
            insert_str_list.append(insert_item)
        setattr(request_or_response_object, 'insert', insert_str_list)
    else:
        for column in columns:
            for received_column_name, _ in received_request.items():
                if column in received_column_name:
                    value_ = received_request[received_column_name]
                    if value_ is not None:
                        if isinstance(value_, list):
                            str_value_ = [str(i) for i in value_]
                        else:
                            str_value_ = str(value_)
                        setattr(request_or_response_object, received_column_name, str_value_)