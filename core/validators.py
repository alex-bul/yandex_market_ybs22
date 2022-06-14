def is_all_objects_ids_unique(item_list):
    if len(item_list) == set(list(map(lambda x: x.get('id'), item_list))):
        raise ValueError("All object ids in list must be unique")