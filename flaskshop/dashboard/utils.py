import functools

from flask import current_app


def get_unique_path(path):
    parent = path.parent
    if path.exists():
        name = path.stem
        ext = path.suffix
        i = 1
        while True:
            new_path = parent / f"{name}({i}){ext}"
            if not new_path.exists():
                return new_path
            i += 1
    else:
        return path


def save_img_file(image):
    upload_path = current_app.config["UPLOAD_DIR"] / image.filename
    upload_path = get_unique_path(upload_path)
    upload_path.write_bytes(image.read())
    background_img_url = upload_path.relative_to(
        current_app.config["STATIC_DIR"]
    ).as_posix()
    return background_img_url


def wrap_partial(fn, *args, **kwargs):
    partial_func = functools.partial(fn, *args, **kwargs)
    functools.update_wrapper(partial_func, args[0])
    return partial_func


def item_del(cls, id):
    try:
        item = cls.get_by_id(id)
        item.delete()
    except Exception as e:
        return {"code": 1, "msg": str(e)}
    return {"code": 0}
