# English Reflex content

The published site has 504 authored exercises: 33 original scenario exercises,
420 record-linked contextual recall exercises, and 51 exercises split from the
long business-English note. Every original record has at least one stable
`practice-<source-page-id>` exercise. Original source cards remain separate and
are excluded from the default training selection.

`corpus.json` and `corpus-pages-complete.json` are the source snapshot, not
verified dictionary entries. Corrections live in the authored training content;
Notion originals are preserved. `conversion-audit.json` maps all 420 records.

## Rebuild

Run `bash rebuild_training.sh`. Content inputs:

- `full_examples.tsv`: 420 complete English reference sentences and recall targets
- `full_chinese.txt`: corresponding natural Chinese sentences
- `target_meanings.txt`: contextual definitions
- `target_alternatives.txt`: paraphrase directions; not universal synonyms
- `learning_content.py`: learning units for original scenario exercises
- `long_note_examples.tsv`: expressions split from the long note

The scripts add editorial corrections, preserve stable IDs and source links,
and emit `dist/data.json` and `dist/learning.json`. Examples are fictional and
must never be represented as the learner's work history.

Both routes share the same no-input interface. B defaults to casual English;
A defaults to professional English. Explicit display choices are stored per
route in browser local storage. No automatic Notion synchronization is present.

## 即时表达与音标
即时表达直接呈现 suggestion 中的完整中文句子，单击查看自然英文，不显示场景、提问、沟通思路或英文版本选择。沟通判断保留原有组织层级和版本选择。长难词在学习词条下标注美式 IPA；pronunciation.json 基于 CMU 发音词典并补充复合词，add_pronunciation.py 负责构建时合并，不需要运行时依赖。

## 精确表达
首页第三张卡为精确表达，第四张为随机一个。458 则 context-recall 训练归入 C 路线，保留稳定 ID 和练习记录。显示原 context 的中文语义提示与英文填空，直接揭示完整英文答案及学习模块；不显示中文答案、沟通判断或版本选择。随机入口均等抽取三种路线。

## 新增原创训练
2026-10-22 新增 36 则即时表达和 24 则沟通判断，分别存于 extra_instant.tsv 和 extra_judgment.tsv，由 append_extra_training.py 合并。训练 ID 使用 extra-instant/extra-judgment 前缀，重建时不重复添加。来源标注原创，不伪造 Notion 记录。当前共 564 则训练：A52、B54、C458。每题有专属释义、完整双语例句、搭配变化、替代表达、语境与直译改进。

## 学习词条与点击高亮
所有实际展示版本都须包含学习目标（允许人称和时态变化），align_learning_answers.py 修正偏离目标的近义改写，audit_answer_alignment.py 检查全部 616 个展示答案。build_learning_highlights.py 为目标词组生成具体字符区间；运行时使用文本节点及按钮渲染，不注入语料 HTML。点击背景高亮才打开学习 dialog，关闭时焦点返回表达，支持 Esc 和遮罩关闭；每题切换重置弹层。

## v3 原生词条与训练类型
原生词条代表 Notion 原始记录或原创语料；训练词条通过 nativeId 指向原生词条，同一原生词条可有多个类型和多个训练。nativeEntries 保留原始 Name、Expressions、Equivalent、Range、Tags、Extension、Pronounce 与已抓取正文。原始字段不覆盖纠正后的教学内容。
四类为 instant（即时表达）、workplace（职场沟通）、precision（精准表达）、advanced（进阶表达）。原 A/B 训练保留稳定 ID，原 C 中有词汇对照 Equivalent 的 137 项转入进阶，并配有逐条编辑的职场情境；其他保留精准训练。生活标签为原生词条增加即时训练，多个类型可共存。最新 silence 训练已补入。
三维标签：topic 细分类别（合并既有近义分类），scene 使用场景（结合原始应用范围），form 语言形式（优先原始词性；缺失时根据词条形式标注词汇、短语或句式）。点击标签默认清空类型限制，跨四类筛选；用户可再选特定类型。原生词条按钮展示其全部训练，同源类型按钮允许聚焦某一类型。
notion-snapshot.json 是本次完整属性快照，421 条，SQL 分页每次 100 条；native-coverage-audit.json 记录每条来源对应的类型与训练 ID。advanced_workplace.tsv 存储 137 个独立职场情境及必要的例句改写。运行 rebuild_training.sh 可从旧原料重建后统一迁移，不直接对迁移后的数据重复迁移。

## 2026-10-23: spoken prompts, picture prompts and audio
- Reviewed all 98 instant entries; 46 Chinese prompts rewritten for spontaneous speech.
- `instant_editorial.json` and `picture_notes.json` are applied by the final `polish_instant.py` rebuild step; stable IDs and original Notion records remain intact.
- Seven concrete objects now use `picture` prompts and reveal the vocabulary target, rather than a prewritten sentence. Photo assets live in `dist/assets/`.
- Literal-first matching fixes function-word learning targets such as “was that for me?”; the final pass also aligns updated English answers and canonical fields.
- Previous/next now follow the current filtered list with wraparound; random excludes the current entry.
- Speech controls use browser SpeechSynthesis with en-US voices at rate 0.9, cancel on navigation, and report playback failures. Controls cover English answers, learning terms/examples and English fragments in usage notes/forms/alternatives. The cloud browser did not have a working playback voice; on-device sound remains unverified.
- UI checks: 1/98 ↔ 98/98 wraparound, correct question-target highlight, picture load/reveal and learning dialog, enlarged controls at 320px.

### Generated photo asset prompts
Built-in imagegen, photorealistic vocabulary flashcards. Shared prompt: square realistic photograph, subject centered and fully in frame, soft natural light, uncluttered cream background, no words/labels/logos/watermark.
- `dist/assets/giblets.png`: chicken liver, heart, gizzard and neck on a white plate, clean food-preparation photography.
- `dist/assets/grease.png`: used frying pan with visible yellow-brown cooking grease and oily streaks.
- `dist/assets/mason_jar.png`: empty unbranded threaded glass mason jar with two-piece silver screw lid alongside.
- `dist/assets/dumpster.png`: large green commercial steel dumpster with black hinged lids in a simple service alley.
- `dist/assets/mayo.png`: bowl of mayonnaise and spoon holding a dollop, no packaging.
- `dist/assets/shiitake.png`: fresh shiitake mushrooms with brown caps and pale gills visible.
- `dist/assets/pain_au_lait.png`: small golden French milk bread rolls with diagonal cuts and fluffy interior visible.

## 2026-10-23: precision prompts and curated instant order
- `organize_precision.py` runs after the instant editorial pass. The first ten instant entries follow the user's requested order without changing IDs or practice state.
- All 321 precision entries now have individually authored scenarios in `precision_scenes.json`. Scenario, Chinese expression, English cloze and Chinese target hint are separate prompt fields.
- Precision shows both scenario and expression immediately, with one English reveal button. Workplace and advanced reveal flows remain unchanged.
- Cloze text is derived from the displayed English answer and its learning highlight, so the missing phrase reconstructs the exact answer (including inflected words).
- Incident retrospective example now uses “I troubleshot traffic anomalies at the code level.” The hypothetical PHP security example uses “It's time to harden the code against malicious activity.”
- Validated native coverage and data links, all 321 cloze/answer pairs, requested ten-entry order, one-click answer reveal and layout at 320px.

## 2026-10-23: advanced comparisons
- All 137 advanced entries now show a scenario, colloquial Chinese and a complete baseline English sentence before a single “看进阶表达” reveal.
- Baseline Equivalent wording is underlined using explicit ranges. The revealed target retains clickable learning highlights and speech controls.
- `advanced_comparisons.json` is the stable-ID editorial source for baseline phrases, Chinese prompts and individual explanations; `organize_advanced.py` runs as the final content pass.
- Original Notion Equivalent values remain available as source data. Definitions, Chinese glosses, spelling mistakes and meaning mismatches are adapted into grammatical baseline English; explanations distinguish true substitutes from specificity, register or meaning changes.
- Source pitfalls explicitly corrected include penultimate ≠ last but two, worry-related keep someone up at night ≠ exciting things, and literal detour ≠ changing the subject.
- Grammar changes accompanying replacement are explicit (look at / glimpse of; beginner at / experience in; a promising new / an up-and-coming; mission to make / goal of making).
- Validated 137 baseline ranges, canonical answer fields and source coverage; checked exact crop-up example, reveal/reset, underlining and 320px layout.

## 2026-10-23: expression sharing, export and bookmarks
- Replaced emoji speaker glyphs with inline SVG speaker icons, cream-paper fill, dark outline and hard shadow; hover/playing uses the existing lime accent.
- Card footer now has exactly three actions: 分享到微信 / 复制这个表达 / 标记这个表达.
- Copy opens an accessible modal showing the exact Markdown payload before copying, with a selectable text fallback if Clipboard API fails. Removed the old inline log/source panels and buttons.
- Share invokes Web Share directly from the click on supported devices, with a compact bilingual expression and stable #entry=<id> link. Users choose WeChat in the device's share targets. A static website cannot force WeChat as the target; unsupported environments show a copyable text/link fallback. No attempt is made to claim a message was sent.
- Hash routing restores the shared lesson and its type on load/hash change, without changing authored practice order.
- Bookmarks use `marked` and `markedAt` in the existing browser-local state. Browse mode sorts marked records first (newest first), selects the leading record on entry, and offers marked/unmarked filters. Practice mode keeps its curated order. Existing done=true marks migrate when no explicit bookmark state exists.
- Verified Markdown preview/copy, bookmark persistence after reload, browse priority/filtering, shared-link routing/counter, and the three-button row plus SVG icons at 320px. Native mobile WeChat target selection requires a real-device check; cloud desktop exercised the fallback path.
- Reference: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share (native share targets are determined by the device).

## 2026-10-23: remove contrived advanced scenes and reorder
- Removed only the five requested advanced variants: giblets, grease, dumpster, shiitake mushrooms and pain au lait. Their original Notion records and other training variants remain intact.
- Moved the existing leotard entry (stable ID preserved) from advanced to precision as picture recall. No company-family-day sentence is shown; the picture reveals `leotard` and its pronunciation/learning module.
- `trim_and_order.py` is the final rebuild pass. It applies exclusions/reclassification, the exact requested 14-entry advanced order, and refreshes native entry links/type counts.
- Current counts: 98 instant, 53 workplace, 322 precision, 131 advanced; 604 exercises, all 421 Notion natives still covered.
- Advanced starts at its first ordered record; bookmarking only changes browse ordering.
- New asset: `dist/assets/leotard.png`, built-in imagegen. Prompt: square realistic photo flashcard of one plain turquoise sleeveless gymnastics leotard, entire garment flat laid on cream background, clear one-piece form, no leggings/skirt, no person/mannequin/text/logos/watermark, soft natural light.
- Full rebuild and native coverage validation passed; checked advanced start/order and leotard picture loading, reveal and correct learning target in browser.

## 2026-10-23: workplace reference hierarchy and reduced browse controls
- Workplace Chinese is now a closed-by-default `details.layer` named 中文表达, styled exactly like 沟通思路. The English reveal action is its sibling, available independently of either accordion.
- Removed combined English display and default preference selector. Every entry starts on casual English; workplace users can switch to professional. Markdown exports use the selected workplace version.
- Removed the database header link and all source links from exported Markdown. Original source metadata remains internal and is not rendered.
- Browse now has three controls: training type, topic and bookmark status (marked/all). Removed text search, scene and form selectors; direct tag clicks still provide cross-type facet browsing.
- Entering the global browse screen defaults to marked when any current lesson is bookmarked, otherwise all. Removing the final bookmark falls back to all. Explicitly choosing all remains supported.
- Browse cards hide the previous/next edge arrows; focused practice retains them.
- Verified closed Chinese accordion, independent English reveal, casual default/professional switching, no combined option, export without source URL, browse defaults with/without bookmarks, and hidden browse edge arrows.

## 2026-10-23: precision priority order
- Applied the nine supplied sentences as positions 1–9; no tenth sentence was supplied. Remaining precision entries keep their previous relative order.
- `precision_priority.json` stores stable IDs, applied by `reorder_precision.py` after trimming. Focused precision practice now starts at its first ordered entry.
- Checked all nine exact Chinese prompts, unchanged total/source coverage and JavaScript syntax.
