import datetime
import json
import os
from dataclasses import dataclass
from typing import List

GROUPS = dict(
    week1={
        "desc": "数组、链表、栈、队列、前缀和、差分、双指针扫描",
        "items": "88,21,26,283,66,206,20,155,150,641,141,227,560,25,1248,304,1109,53,1,167,15,11,84,239,42,560",
    },
    week2={
        "items": "874,49,30,146,78,77,46,111,104,226,98,50,22",
        "desc": "哈希表、集合、映射、递归、分治",
    },
    week3={
        "items": "106,210,130,94,589,429,297,105,1245,236,684,207,17,51,200,433,329",
        "desc": "树、图、深度优先搜索、广度优先搜索",
    },
    week4={"items": "23,295,355,239,704,410,162,34", "desc": "二叉堆、二叉搜索树、二分"},
    week5={
        "items": "912,1122,56,215,493,322,860,455,122,45,1665,1011,911,875,327",
        "desc": "排序、贪心",
    },
    week6={
        "items": "322,63,1143,300,53,152,121,122,123,188,714,309,198,213,72,416,518,70,120,673,279,55,45",
        "desc": "动态规划",
    },
    week7={"items": "1499,1000,312,918,300,684,200", "desc": "动态规划、Trie树、并查集"},
    week8={"items": "709,58,771,387,14,344,151,917,205,242,49,438,44,8", "desc": "图论算法、字符串处理"},
    week9={"items": "1091,1206,22,51,36,37,127,773", "desc": "高级搜索、平衡二叉树、跳跃表"},
    week10={"items": "699,307,327,191,231,190,338,50,51,37,218,1851", "desc": "树状数组、线段树"},
)

TITLE = "# Leetcode Solutions\n\n"

with open("qs.json", "r") as f:
    DB = json.load(f)


@dataclass
class Item:
    title: str
    slug: str
    tags: List[str]
    difficulty: str
    solutions_dir: str


STATISTIC = {"problems": 0, "lang": {}}


def _parse_week(nums: str) -> List[Item]:
    items = []
    for num in nums.split(","):
        qid = num.zfill(4)
        q = DB[qid]
        folder = f"solutions/{qid}-{q['title']}"
        if not os.path.isdir(folder):
            os.mkdir(folder)
        items.append(
            Item(
                title=f"{qid}-{q['title']}",
                slug=q["slug"],
                tags=q["tags"],
                difficulty=q["difficulty"],
                solutions_dir=folder,
            )
        )
    return items


def _gen_statistic() -> str:
    content = f"> Generate Time: {datetime.date.today()}\t"
    content += f"(Problems : {STATISTIC['problems']})\n"
    for lang, num in STATISTIC["lang"].items():
        content += f"> + Solutions({lang}): {num}\n"
    return content


DIFFICULTY = {
    "EASY": "🟩",
    "MEDIUM": "🟨",
    "HARD": "🟥",
}


def _gen_week(week: str, desc: str, items: List[Item]) -> str:
    ret = "***\n"
    ret += f"## {week.capitalize()}\n"
    ret += f"> {desc}\n\n"
    titles = ["No.", "题目", "难度", "Tags", "Solutions"]
    ret += f"|{'|'.join(titles)}|\n"
    ret += "|---|---|---|---|---|\n"
    for idx, item in enumerate(items, start=1):
        line = [
            str(idx),  # No.
            f"[{item.title}](https://leetcode-cn.com/problems/{item.slug})",  # Link
            f"{DIFFICULTY[item.difficulty]}",  # Difficulty
            " ".join([f"`{t}`" for t in item.tags]),  # Tags
            _gen_solutions_str(item.solutions_dir),  # Solutions
        ]
        ret += f"|{'|'.join(line)}|\n"
    ret += "\n\n"
    return ret


EXT = {
    "go": "Go",
    "py": "Python",
    "rs": "Rust",
    "js": "Javascript",
}


def _gen_solutions_str(solutions_dir: str) -> str:
    ret = []
    count = {}
    solutions = os.listdir(solutions_dir)
    STATISTIC["problems"] += 1
    for s in solutions:
        lang = EXT[s.split(".")[-1]]
        count.setdefault(lang, [])
        count[lang].append(s)

    for lang, solutions in count.items():
        STATISTIC["lang"].setdefault(lang, 0)
        STATISTIC["lang"][lang] += len(solutions)
        if len(count[lang]) == 1:
            href = f"{solutions_dir}/{solutions[0]}".replace(" ", "%20")
            ret.append(f"[{lang}]({href})")
        else:
            for idx, solution in enumerate(solutions, start=1):
                href = f"{solutions_dir}/{solution}".replace(" ", "%20")
                ret.append(f"[{lang}-{idx}]({href})")

    return " ".join(ret)


def main():
    content = ""
    for week, item in GROUPS.items():
        content += _gen_week(week, item["desc"], _parse_week(item["items"]))

    with open("README.md", "w") as readme:
        readme.write(TITLE)
        # 统计信息
        readme.write(_gen_statistic())
        readme.write(content)


if __name__ == "__main__":
    main()
