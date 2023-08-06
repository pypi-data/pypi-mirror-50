from typing import *

class Aggregation:
    def reset(self):
        raise NotImplementedError()
    def account(self, element):
        raise NotImplementedError()
    def report(self):
        raise NotImplementedError()
    def get_name(self):
        raise NotImplementedError()

class Sum(Aggregation):
    def __init__(self):
        self.sum=0
        self.has_elements = False

    def reset(self):
        self.sum=0
        self.has_elements = False

    def account(self, element):
        self.sum+=element
        self.has_elements = True

    def report(self):
        if not self.has_elements:
            raise ValueError('Sequence contains no elements')
        return self.sum

    def get_name(self):
        return 'sum'


class Count(Aggregation):
    def __init__(self):
        self.cnt = 0

    def reset(self):
        self.cnt = 0

    def account(self, element):
        self.cnt+=1

    def report(self):
        return self.cnt

    def get_name(self):
        return 'count'


class Mean(Aggregation):
    def __init__(self):
        self.sum = 0
        self.cnt = 0

    def reset(self):
        self.sum=0
        self.cnt=0

    def account(self, element):
        self.sum+=element
        self.cnt += 1

    def report(self):
        if self.cnt==0:
            raise ValueError('Sequence contains no element')
        return self.sum/float(self.cnt)

    def get_name(self):
        return 'mean'

class Min(Aggregation):
    def __init__(self):
        self.min = None
        self.has_element = False

    def reset(self):
        self.min = None
        self.has_element = False

    def account(self, element):
        self.has_element = True
        if self.min is None or self.min>element:
            self.min = element

    def report(self):
        if not self.has_element:
            raise ValueError('Sequence contains no elements')
        return self.min

    def get_name(self):
        return 'min'


class Max(Aggregation):
    def __init__(self):
        self.max = None
        self.has_element = False

    def reset(self):
        self.max = None
        self.has_element = False

    def account(self, element):
        self.has_element = True
        if self.max is None or self.max<element:
            self.max = element

    def report(self):
        if not self.has_element:
            raise ValueError('Sequence contains no elements')
        return self.max

    def get_name(self):
        return 'max'

class Any(Aggregation):
    def __init__(self):
        self.any = None

    def reset(self):
        self.any = False

    def account(self, element):
        if element:
            self.any = True

    def report(self):
        return self.any

    def get_name(self):
        return 'any'


class All(Aggregation):
    def __init__(self):
        self.all = None

    def reset(self):
        self.all = True

    def account(self, element):
        if not element:
            self.all = False

    def report(self):
        return self.all

    def get_name(self):
        return 'all'



def aggregate_with(en, selector:Optional[Callable] = None, *args: Aggregation):
    if len(args) == 0:
        raise ValueError('No aggregators are provided')

    for a in args:
        a.reset()
    for e in en:
        if selector is None:
            p = e
        else:
            p = selector(e)
        for a in args:
            a.account(p)

    if len(args)==1:
        return args[0].report()
    return {z.get_name():z.report() for z in args}







