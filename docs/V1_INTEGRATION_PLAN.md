# HR-clipping V1 集成计划

日期：2026-11-02。用户已明确授权创建文件、整合、验证、提交、推送专用分支；交付后停在独立审查点。

## Task Contract

- Goal：将附件中同一份 Skill 正式集成到仓库，让每期只输入主题、素材、任务类型和例外。
- Scope：仓库入口、唯一 Skill、母规范、模板、脱敏示例、轻量校验与证据。
- Out of Scope：正式剪片、素材上传、软件安装、外部付费 API、全局 Skill 安装、其他工程、main 合并和平台发布。
- Constraints：唯一标识 `hr-clipping`；风格为“小杨同学科技VLOG V1”；保护原片；公开仓库只提交脱敏文本与校验代码。
- Dependencies：用户提供的 v2 任务书、Skill ZIP、独立母规范与参考分析；Python 标准库、Git；现有代理能力。
- Acceptance：一个入口一个母规范；相对引用有效；模板区分源/成片/字幕时间轴；有实际验证证据；专用分支推送可核对；状态 READY_FOR_REVIEW。
- Verification：结构检查、负向用例、独立代理少量无/有 Skill 对照、暂存及提交敏感信息/媒体检查、远端 SHA 核对。宿主与成片不借用旧证据。

## 实施步骤

- [x] 核对附件 v2、仓库权限/默认分支/初始提交/工作区；新克隆与专用分支隔离。
- [x] 先定义行为场景及评分边界。
- [x] 无 Skill 独立样本；记录实际缺口，不强行声称所有基线失败。
- [x] 安全检查 ZIP（路径、重复、链接、体积），解压到临时目录；比较来源后导入。
- [x] 整合唯一母规范；保留来源观察但标记历史归属；简报只向用户索取四个变化项。
- [x] 补仓库 AGENTS/README/STATUS/.gitignore，记录风格例外及权限边界。
- [x] 实现标准库结构校验；负向用例先验证缺失校验器失败，再补实现。
- [x] 新独立代理实际读取并作答，对 B1–B8 评分；B3 隔离检查误触发。
- [x] 复查实际文件、引用、证据和安全；按证据更新报告，不升级 NOT_RUN。
- [x] 逐项暂存；检查 diff；Conventional Commit；推送当前功能分支；核对远端 SHA。功能提交与推送证据见[验证回执](../tests/evidence/verification-log.md)，最终交付快照由交付答复固定链接指定。

## 文件职责

| 文件 | 职责 |
|---|---|
| AGENTS.md | 视频任务路由；普通代码任务不误用 |
| .agents/skills/hr-clipping/SKILL.md | 触发条件、按需加载、制作流程入口 |
| references/production-baseline-v1.md | 唯一固定风格母规范 |
| references/reference-analysis.md | 既有观察/分析/提案/未知的来源边界 |
| templates 与 examples | 单集变化、剪辑映射、审片、未拍示例 |
| scripts/validate_skill.py | 必需文件、UTF-8、标识、相对引用与模板字段的轻量检查 |
| tests/test_validate_skill.py | 缺文件、错误命名、坏引用、编码和模板缺项的回归 |
| docs/V1_INTEGRATION_REVIEW.md | 集成差异、来源、实际验证与待审范围 |
| tests/evidence/ | 脱敏独立代理输入/答复和评估记录 |

## 重点核验

历史提取原片的声明必须归属于原包；本轮只有附件文本与截图，不能冒称重新解码或听审。结构检查不等于模型行为；手工读 Skill 不等于宿主发现。示例与脚本中的预计时间不能成为素材时间。原视频、抽帧、私有路径、密钥均不进入提交。
