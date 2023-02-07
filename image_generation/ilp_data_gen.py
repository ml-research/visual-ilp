import itertools
import random

from dilpst.src.ilp_problem import ILPProblem
from scene import CLEVRObject, CLEVRSize, CLEVRColor, CLEVRShape, CLEVRMaterial


def ilp_problem2scenes(ilp_problem):
    # an example is a list of clevr objects
    pos_scenes = [objects2scene(x) for x in ilp_problem.pos_examples]
    neg_scenes = [objects2scene(x) for x in ilp_problem.neg_examples]
    bk_scenes = [objects2scene(x) for x in ilp_problem.backgrounds]


def objects2scene(x):
    pass


"""
full attributes
colors = ["cyan","blue","yellow","purple","red","green","gray","brown"]
shapes = ["sphere","cube","cylinder"]
sizes = ["large","small"]
materials = ["rubber","metal"]
"""

colors = ["red", "gray", "cyan", "yellow"]
# shapes = ["sphere"]
sizes = ["large"]
# materials = ["metal"]
shapes = ["sphere", "cube", "cylinder"]
materials = ["rubber", "metal"]


def gen_all_properties():
    xs = itertools.product(colors, shapes, sizes, materials)
    ys = []
    for x in xs:
        color = CLEVRColor(x[0])
        shape = CLEVRShape(x[1])
        size = CLEVRSize(x[2])
        material = CLEVRMaterial(x[3])
        obj = CLEVRObject(color=color, shape=shape, size=size, material=material)
        ys.append(obj)
    return ys


def random_choices(ls, k):
    if k == 0:
        return []
    else:
        return [random.choice(ls) for i in range(k)]


def sample_wo_color_duplication(n, clevr_objects):
    flag = True
    while flag:
        objs = random.sample(clevr_objects, k=n)
        colors = [x.color.name for x in objs]
        if len(colors) == len(list(set(colors))):
            flag = False
    return objs


def get_sublist(ls):
    if len(ls) == 1:
        return [ls] + [[]]
    else:
        return [ls] + get_sublist(ls[1:])


def get_ilp_problem(name, n):
    if name == "member":
        return MemberProblem(n)
    elif name == "delete":
        return DeleteProblem(n)
    elif name == "append":
        return AppendProblem(n)
    elif name == "sort":
        return SortProblem(n)
    elif name == "reverse":
        return ReverseProblem(n)


class MemberProblem(ILPProblem):
    def __init__(self, n=30, noise_rate=0.0, max_len=3, min_len=3):
        self.name = "member"
        self.pos_examples = []
        self.neg_examples = []
        self.backgrounds = []
        self.init_clauses = []
        # p_ = Predicate('.', 1)
        # false = Atom(p_, [Const('__F__')])
        # true = Atom(p_, [Const('__T__')])
        # self.facts = [false, true]
        self.lang = None
        self.noise_rate = noise_rate
        self.n = n
        self.max_len = max_len
        self.min_len = min_len
        # self.symbols = list('abc')
        self.symbols = gen_all_properties()

        # init dataset
        self.get_pos_examples()
        self.get_neg_examples()

    def get_pos_examples(self):
        i = 0
        while len(self.pos_examples) < self.n:
            n = random.randint(self.min_len, self.max_len)
            x = random.choice(self.symbols)
            # ls = random.sample(self.symbols, k=n)
            ls = sample_wo_color_duplication(n=n, clevr_objects=self.symbols)
            if x in ls:
                self.pos_examples.append(([x], ls))
                # term1 = Const(x)
                # term2 = list_to_term(ls, self.funcs[0])
                # atom = Atom(self.preds[0], [term1, term2])
                # self.pos_examples.append(atom)

    def get_neg_examples(self):
        i = 0
        while i < self.n:
            n = random.randint(1, self.max_len)
            # 長さnで満たすもの出すまで繰り返し
            flag = True
            while flag:
                x = random.choice(self.symbols)
                ls = random.sample(self.symbols, n)
                if not x in ls:
                    self.neg_examples.append(([x], ls))
                    # atom = Atom(self.preds[0], [
                    #            Const(x), list_to_term(ls, self.funcs[0])])
                    # self.neg_examples.append(atom)
                    i += 1
                    flag = False


def delete(a, ls):
    result = []
    count = 0
    for x in ls:
        if a == x and count == 0:
            count += 1
            next
        else:
            result.append(x)
    return result


class AppendProblem(ILPProblem):
    def __init__(self, n=50, noise_rate=0.0, max_len=3, min_len=3):
        self.name = "append"
        self.pos_examples = []
        self.neg_examples = []
        self.backgrounds = []
        self.init_clauses = []
        self.lang = None
        self.noise_rate = noise_rate
        self.n = n
        self.max_len = max_len
        self.min_len = min_len
        # self.symbols = list('abc')
        self.symbols = gen_all_properties()

        # init dataset
        self.get_pos_examples()
        self.get_neg_examples()

    def get_pos_examples(self):
        i = 0
        while len(self.pos_examples) < self.n:
            a1 = random.choice(self.symbols)

            n2 = random.randint(self.min_len - 1, int(self.max_len) - 1)
            # ls2 = random.sample(self.symbols, k=n2)
            ls2 = sample_wo_color_duplication(n=n2, clevr_objects=self.symbols)

            # flip 50% of examples (1,2) or (2,1)A
            if random.random() < 0.5:
                self.pos_examples.append(([a1], ls2, [a1] + ls2))
            else:
                self.pos_examples.append((ls2, [a1], ls2 + [a1]))

            i += 1

    def get_neg_examples(self):
        i = 0
        while i < self.n:
            a1 = random.choice(self.symbols)

            n2 = random.randint(self.min_len - 1, int(self.max_len) - 1)
            # ls2 = random.sample(self.symbols, k=n2)
            ls2 = sample_wo_color_duplication(n=n2, clevr_objects=self.symbols)
            n3 = random.randint(self.min_len, int(self.max_len))
            # ls3 = random.sample(self.symbols, k=n2)
            ls3 = sample_wo_color_duplication(n=n2, clevr_objects=self.symbols)

            if random.random() < 0.5:
                if [a1] + ls2 != ls3:
                    self.neg_examples.append(([a1], ls2, ls3))
                    i += 1
            else:
                if ls2 + [a1] != ls3:
                    self.neg_examples.append((ls2, [a1], ls3))
                    i += 1


class DeleteProblem(ILPProblem):
    def __init__(self, n=50, noise_rate=0.0, max_len=3, min_len=3):
        self.name = "delete"
        self.pos_examples = []
        self.neg_examples = []
        self.backgrounds = []
        self.init_clauses = []
        self.lang = None
        self.noise_rate = noise_rate
        self.n = n
        self.max_len = max_len
        self.min_len = min_len
        # self.symbols = list('abc')
        self.symbols = gen_all_properties()

        # init dataset
        self.get_pos_examples()
        self.get_neg_examples()

    def get_pos_examples(self):
        i = 0
        while len(self.pos_examples) < self.n:
            a1 = random.choice(self.symbols)

            n2 = random.randint(self.min_len, int(self.max_len))
            # ls2 = random.sample(self.symbols, k=n2)
            ls2 = sample_wo_color_duplication(n=n2, clevr_objects=self.symbols)
            if a1 in ls2:
                self.pos_examples.append(([a1], ls2, delete(a1, ls2)))
                i += 1

    def get_neg_examples(self):
        i = 0
        while i < self.n:
            a1 = random.choice(self.symbols)

            n2 = random.randint(self.min_len, int(self.max_len))
            # ls2 = random.sample(self.symbols, k=n2)
            ls2 = sample_wo_color_duplication(n=n2, clevr_objects=self.symbols)
            n3 = random.randint(self.min_len - 1, int(self.max_len) - 1)
            # ls3 = random.sample(self.symbols, k=n2)
            ls3 = sample_wo_color_duplication(n=n2, clevr_objects=self.symbols)
            if a1 in ls2 and delete(a1, ls2) != ls3:
                self.neg_examples.append(([a1], ls2, ls3))
                i += 1


class SortProblem(ILPProblem):
    def __init__(self, n=50, noise_rate=0.0, max_len=3, min_len=3):
        self.name = "sort"
        self.pos_examples = []
        self.neg_examples = []
        self.backgrounds = []
        self.init_clauses = []
        self.lang = None
        self.noise_rate = noise_rate
        self.n = n
        self.max_len = max_len
        self.min_len = min_len
        # self.symbols = list('abc')
        self.symbols = gen_all_properties()

        # init dataset
        self.get_pos_examples()
        self.get_neg_examples()

    def get_pos_examples(self):
        i = 0
        while len(self.pos_examples) < self.n:
            a1 = random.choice(self.symbols)

            n1 = random.randint(self.min_len, self.max_len)
            # ls = random.sample(self.symbols, k=n1)
            ls = sample_wo_color_duplication(n=n1, clevr_objects=self.symbols)
            ls_sorted = sorted(ls, key=lambda x: x.color.name)

            self.pos_examples.append((ls, ls_sorted))
            i += 1

    def get_neg_examples(self):
        i = 0
        while i < self.n:
            n1 = random.randint(self.min_len, self.max_len)
            # ls1 = random.sample(self.symbols, k=n1)
            ls1 = sample_wo_color_duplication(n=n1, clevr_objects=self.symbols)
            # ls2 = random.sample(self.symbols, k=n1)
            # ls2 = sample_wo_color_duplication(n=n1, clevr_objects=self.symbols)
            ls2 = ls1.copy()
            if random.random() > 0.3:
                random.shuffle(ls2)
            ls1_sorted = sorted(ls1, key=lambda x: x.color.name)
            ls1_sorted_colors = [x.color.name for x in ls1_sorted]
            ls2_colors = [x.color.name for x in ls2]
            if ls1_sorted_colors != ls2_colors:
                self.neg_examples.append((ls1, ls2))
                i += 1


class ReverseProblem(ILPProblem):
    def __init__(self, n=50, noise_rate=0.0, max_len=3, min_len=3):
        self.name = "sort"
        self.pos_examples = []
        self.neg_examples = []
        self.backgrounds = []
        self.init_clauses = []
        self.lang = None
        self.noise_rate = noise_rate
        self.n = n
        self.max_len = max_len
        self.min_len = min_len
        # self.symbols = list('abc')
        self.symbols = gen_all_properties()

        # init dataset
        self.get_pos_examples()
        self.get_neg_examples()

    def get_pos_examples(self):
        i = 0
        while len(self.pos_examples) < self.n:
            a1 = random.choice(self.symbols)

            n1 = random.randint(self.min_len, self.max_len)
            # ls = random.sample(self.symbols, k=n1)
            ls = sample_wo_color_duplication(n=n1, clevr_objects=self.symbols)
            ls_reversed = list(reversed(ls))  # , key=lambda x:A x.color.name)

            self.pos_examples.append((ls, ls_reversed))
            i += 1

    def get_neg_examples(self):
        i = 0
        while i < self.n:
            n1 = random.randint(self.min_len, self.max_len)
            # ls1 = random.sample(self.symbols, k=n1)
            ls1 = sample_wo_color_duplication(n=n1, clevr_objects=self.symbols)
            # ls2 = random.sample(self.symbols, k=n1)
            # ls2 = sample_wo_color_duplication(n=n1, clevr_objects=self.symbols)
            ls2 = ls1.copy()
            if random.random() > 0.3:
                random.shuffle(ls2)
            ls1_reversed = list(reversed(ls1))  # , key=lambda x: x.color.name)
            ls1_reversed_colors = [x.color.name for x in ls1_reversed]
            ls2_colors = [x.color.name for x in ls2]
            if ls1_reversed_colors != ls2_colors:
                self.neg_examples.append((ls1, ls2))
                i += 1
