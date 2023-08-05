# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   Author :       Zhang Fan
   date：         2019/8/1
   Description :
-------------------------------------------------
"""
from types import FunctionType


class InterfaceError(Exception):
    pass


def decorator_must_overload(cls, func):
    def decorator(*args, **kwargs):
        raise InterfaceError('方法 {}.{} 必须重载后才能使用'.format(cls.__name__, func.__name__))

    return decorator


class Must_Overload():
    def __init__(self, cls):
        old_func_mapp = dict()
        for mro in cls.mro():
            if cls == object:
                continue
            mo = getattr(mro, '__must_overload__', None)
            if not mo:
                continue
            for name, value in mo.overload_func_mapp.items():
                # if name in old_func_mapp:
                #     raise InterfaceError('方法 {}.{} 被定义多次'.format(cls.__name__, name))
                old_func_mapp[name] = value

        func_mapp = dict()
        for name, value in cls.__dict__.items():
            if isinstance(value, FunctionType) and name[0] != '_':
                func_mapp[name] = value

        for name, value in func_mapp.items():
            decorator_func = decorator_must_overload(cls, value)
            func_mapp[name] = decorator_func
            setattr(cls, name, decorator_func)

        func_mapp.update(old_func_mapp)
        self.overload_func_mapp = func_mapp
        setattr(cls, '__must_overload__', self)

    def add_func(self, mapp, cls, func):
        pass

    def check(self):
        pass


def InterfaceBase(cls):
    Must_Overload(cls)
    return cls


def InterfaceCheck(cls):
    mo = getattr(cls, '__must_overload__', None)  # type: Must_Overload
    assert mo, '对象 {} 没有继承使用了接口类型的父类'.format(cls.__name__)
    for name, decorator_func in mo.overload_func_mapp.items():
        now_func = getattr(cls, name)
        if now_func == decorator_func:
            raise InterfaceError('方法 {}.{} 未被重载'.format(cls.__name__, name))

    return cls
