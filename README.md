# surge-rules

## TAG Profile Lite

[TAG Profile Lite](https://raw.githubusercontent.com/zhiyue/surge-rules/release/Modules/tag-profile-lite.sgmodule) 是从 TAG 上游生成的 Surge 模块。它删除 `A = A` 自映射，以减少 `[Host]` 条目；保留真正改变节点入口解析的 `A = B` 别名及原顺序。

[发布流程](.github/workflows/merge_openai_rule.yml) 每天用[精简脚本](scripts/trim-tag-hosts.py)检查上游。只有精简后的产物变化才会因此触发发布；原模块只增删自映射时，Lite 的内容保持不变。上游获取或校验失败时保留上次发布的版本。

Mac 和 iPhone 可从同一地址安装。启用 Lite 后停用原 `TAG Profile`；如果同时使用 `DNS Split`，让它的优先级高于 Lite。已安装的模块在 [Surge 中手动更新](https://manual.nssurge.com/tools/cli.html#module-details)。
