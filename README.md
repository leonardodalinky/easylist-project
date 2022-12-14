# easylist-project
Homework for graduate course.

## 预备工作

目前已经将 [easylist](https://github.com/easylist/easylist) 和 [easylistchina](https://github.com/easylist/easylistchina) 都加为子模块。

easylist 以及 easylistchina 都需要**固定**到其 master 分支的一个比较新的 commit。之后的所有工作仅此 commit 之前的版本:
* easylist: bb058be
* easylistchina: 23537fb

由于可能会涉及多版本回溯，子模块仅作为版本的 anchor，起提示作用。实际代码中可能并不会涉及到子模块中的内容，并且可能需要自行在其他版本中自行重新克隆子模块的项目。

easylist 的文件结构在[此处查阅](https://adblockplus.org/filter-cheatsheet)。

## TODO-List

- [x] 找到现成的或者自己实现一个 easylist filter 解析器
- 独立域名统计
  - [ ] 最新版本的独立域名统计，包括有多少个不同的域名，每个二级/三级域名下，又有多少个规则等
  - [ ] 对历史版本都进行统计
- filter 差分统计
  - [ ] 对各个版本中的 filters 进行差分过滤，得到每个版本中的变化情况。我们只记录 filter 的增加与删除，对于 filter 的修改，我们将其当作一次删除与一次增加。使用 JSON 形式记录。
  - 根据上面所获得的各个版本的变更信息，并分析一些信息:
    - 新增和删去的规则中，其数量多少，normal rule 和 html rule 各有多少
    - 平均每个 commit 之间的时间差
    - 所认为的新增的 Exception rule 的数量
    - 单独的 EX rule 的添加时间，与其 base rule 的添加时间的时间差
- easylist 失效的情景
  - [ ] 找一些 easylist 失效的场景，这里可以使用一些现成的广告拦截插件（例如 AdBlock）来寻找
  - [ ] 总结多方面的失败原因
- To be continued.

## 域名过滤的规则

由于 easylistchina 中存在着太多不完整的域名，以及存在着许许多多的通配域名，例如：
```
*.ad.baidu.com
adyss.
```

对于这种域名，我们采取以下策略：
- 不完整域名：直接丢弃，当做没看见
- 通配域名：尽可能保留域名最后面不带通配域名的部分

## Rule parser 用法

`Rule` 和 `Rules` 的定义参考 `filter_parser` 模块。

主要通过 `repo_utils` 模块中的函数来读取 `easylistchina` 中所包含的各个历史版本的 filter 数据。

Examples:
```python
import repo_utils

repo = repo_utils.get_git_repo("/tmp/easylistchina")
# 读取当前 repo 的规则
rules = repo_utils.get_rules_rel_from_repo(repo, "easylistchina.txt")
# 读取当前 repo 下所有历史版本的规则数据
rules_list = list(repo_utils.iter_all_rules_from_repo(repo, "easylistchina.txt"))
```

`Rule` 对象下面最重要的是 `domain`，里面会可能有不完整或者通配域名等怪异状况，急需一个过滤手段。

如果已有 `extract_easylists.py` 预处理好的 easylist 大全，那么可以手动加载 `Rules`:
```python
from datetime import datetime
from filter_parser import Rules

rules = Rules.from_file("/tmp/easylistchina.txt", time=datetime.utcnow(), commit_hash="1H34SD8A0")
```

## Scripts 用法

### `scripts/extract_easylists.py`

这个脚本用来提取所有的历史 easylistchina 中的 `easylistchina.txt` 文件，并存储在指定目录下。

Usage:
```bash
# 提取 easylistchina 中的 easylistchina.txt 文件
python scripts/extract_easylists.py -r /tmp/easylistchina -f easylistchina.txt -o /tmp/all_easylists
```

### `scripts/diff.py`

这个脚本用来执行不同版本的 `easylistchina.txt` 的差分操作，必须用于 `extract_easylists.py` 所生成的目录。

```bash
python scripts/diff.py -d /tmp/all_easylists -o /tmp/easylists_diff
```

## easylistchina 失效的情景

1. 有一些域名未被列入 easylist 中，而是委托给一些小广告商，然后他们经常改变域名，使得难以被追踪
2. 有一些网站加载了 anti-adblock 的脚本，这些脚本会检测广告是否正常加载，如果没有加载，那么就会显示一些提示，或者直接阻止网页的正常加载
3. To be continued.
