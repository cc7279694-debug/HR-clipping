# 本轮验证收据

日期：2026-11-02。工作目录为仓库根；不在公开记录中保存绝对本地路径。记录退出码与实际输出，不复制原包 PASS 作为本轮结果。

## 测试先行

导入/修改 Skill 前已定义 B1–B8；无 Skill 组先完成。校验器实现前运行：

```text
python -X utf8 -m unittest discover -s tests -p 'test_*.py' -v
exit 1
test_validator_exists ... FAIL
validator not implemented
FAILED (failures=1, skipped=1)
```

第一次搭建测试时曾把缺校验器报成 setUpClass ERROR，已改成明确断言失败；没有删除测试绕过结果。

## 结构及负向回归

```text
python -X utf8 scripts/validate_skill.py
exit 0
PASS: 23 required files; UTF-8, identity, local file targets, template fields
Scope: limited scalar-field checks; link targets only, not anchors; no host/behavior/media validation

python -X utf8 -m unittest discover -s tests -p 'test_*.py' -v
exit 0
Ran 11 tests
OK
```

包含缺文件、错误标识、空描述、失效相对链接、逃逸链接、坏 UTF-8、缺时间字段、重复 Skill、旧调用名，以及有效仓库和校验器存在性检查。

有效仓库副本先后发现历史收据和报告引用的行为证据未被复制；实际仓库中存在这些目标，但副本缺失。已将历史收据及六份行为/验证证据全部纳入必需文件，重新运行 11 项全部通过。

## 作者工具检查

常用 Python 3.12 缺少 PyYAML，首次 quick_validate 因导入依赖退出 1；未安装依赖。Python 启动器中另一个注册项无效，已改用本机现有 Anaconda Python（已有 PyYAML 5.4.1）执行相同原始工具，退出 0：

```text
<existing-python> -X utf8 <skill-creator>/scripts/quick_validate.py .agents/skills/hr-clipping
Skill is valid!
```

上面两个安装路径在公开记录中已脱敏；未修改或替代作者工具。这个成功仅覆盖其 frontmatter/命名/占位符检查，不代表宿主发现。

## 保留未执行状态

宿主菜单发现及真实调用自动注入：NOT_RUN。样片剪辑、完整播放、完整试听、工程重开：NOT_RUN。未新增依赖、付费 API 或剪辑软件。

## 提交前全仓库复查

另一个全新上下文的 Codex 代理只读检查了全部 25 份交付文本，复跑结构检查、11 项回归及 diff 空白检查，核对来源哈希和历史收据原文。没有未解决 Critical/Important；README 跨工作区说明的 Minor 已补充证据链接依赖。该复查是执行流程内质量检查，不等同独立 ChatGPT 审查或用户验收。

执行方对全部 25 份文本做 UTF-8/JSON、媒体类型及敏感内容检查，未发现私人绝对路径、邮箱、凭据或原始媒体；8 份用户原附件 SHA-256 均未变化。`.gitignore` 的原片、输出、参考图、环境文件和本地简报路径均命中忽略规则。提交时仍需对实际暂存内容及生成提交再检查。

实际暂存后的空白检查发现原包带来的五处 Markdown 双空格换行；已改为段落换行，保持内容含义，重新检查暂存 diff。
