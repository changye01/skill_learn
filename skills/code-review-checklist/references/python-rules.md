# Python 专项审查规则

以下规则仅在审查 Python 代码时使用，作为通用规则的补充。

---

## 1. PEP 8 规范

检查要点：
- 缩进是否使用 4 个空格
- 行长度是否不超过 88 字符（black 默认）或 79 字符（PEP 8 默认）
- import 顺序是否正确（标准库 → 第三方 → 本地）
- 类和顶层函数之间是否有两个空行

---

## 2. 类型提示

检查要点：
- 公开函数是否有参数和返回值类型提示
- 复杂数据结构是否使用 TypeAlias 或 TypedDict
- 是否避免了 `Any` 类型（除非确实需要）
- Optional 参数是否标注为 `X | None`

---

## 3. 异常处理

检查要点：
- 是否避免了裸 `except:`（应捕获具体异常）
- 是否避免了 `except Exception:`（太宽泛）
- 是否使用了 `raise ... from e` 保留异常链
- 资源清理是否使用了 `with` 语句或 `finally`

---

## 4. Pythonic 写法

检查要点：
- 是否使用列表推导代替简单的 for+append
- 是否使用 `enumerate()` 代替手动计数器
- 是否使用 `pathlib.Path` 代替字符串拼接路径
- 是否使用 f-string 代替 `%` 或 `.format()`
