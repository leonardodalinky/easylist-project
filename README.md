# easylist-project
Homework for graduate course.

## 预备工作

目前已经将 [easylist](https://github.com/easylist/easylist) 和 [easylistchina](https://github.com/easylist/easylistchina) 都加为子模块。

easylist 以及 easylistchina 都已经**固定**到其 master 分支的一个比较新的 commit。之后的所有工作仅此 commit 之前的版本。

由于可能会涉及多版本回溯，子模块仅作为版本的 anchor，起提示作用。实际代码中可能并不会涉及到子模块中的内容，并且可能需要自行在其他版本中自行重新克隆子模块的项目。

easylist 的文件结构在[此处查阅](https://adblockplus.org/filter-cheatsheet)。

## TODO-List

- [x] 找到现成的或者自己实现一个 easylist filter 解析器
- 独立域名统计
  - [ ] 最新版本的独立域名统计，包括有多少个不同的域名，每个二级/三级域名下，又有多少个规则等
  - [ ] 对历史版本都进行统计
- filter 差分统计
  - [ ] 对各个版本中的 filters 进行差分过滤，得到每个版本中的变化情况。我们只记录 filter 的增加与删除，对于 filter 的修改，我们将其当作一次删除与一次增加。找一个格式存储，例如 json 等。
  - 根据上面所获得的各个版本的变更信息，使用**一些规则**来统计**一些信息**。这一点比较重要，待细化。
  - FP 错误该如何从这里面找出来呢？我个人认为，如果对某个域名新增了 exception rules，那基本上就是 FP 错误。因此可以从这一点入手，我们就不搞花里胡哨的论坛帖子爬取这些东西了。
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

