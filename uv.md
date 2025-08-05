# uv

https://docs.astral.sh/uv/getting-started/installation/#installation-methods

https://docs.astral.sh/uv/getting-started/installation/#pypi



# 1. 初步使用

1. 安装

   ```
   pip install uv
   ```

   或者

   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   

2. 查看版本信息

   ```
   uv --version
   ```

   

3. 初步设想

   - 开发阶段

     - uv 负责管理依赖（`pyproject.toml`）

   - 部署阶段

     - 使用 pip




4. uv初始化

   https://docs.astral.sh/uv/guides/projects/#working-on-projects

   ```
   uv init 
   ```

   新增文件

   ```
   .
   ├── .git
   ├── .gitignore
   ├── main.py
   ├── pyproject.toml
   ├── .python-version
   ├── README.md
   ```

   

5. 创建虚拟环境

   ```
   uv venv -p 3.13.5
   ```

   - 查看当前支持的python版本  `uv python list`

   

6. 激活环境

   ```
   source .venv/bin/activate
   ```

   



# 2. 依赖管理

1. uv 安装依赖

   ```
   uv add fastapi
   ```

   **可以看到uv自动调整`pyproject.toml`中的`dependencies`**

   ```toml
   [project]
   name = "learn"
   version = "0.1.0"
   description = "Add your description here"
   readme = "README.md"
   requires-python = ">=3.13.5"
   dependencies = [
       "fastapi>=0.116.1",
   ]
   ```
   



2. 指定版本安装

   ```
   uv add pydantic==2.10.0
   uv add pydantic>=2.10.0
   uv add "pydantic<=2.10.0"        # 注意添加引号
   ```
   
   
   
3. 打印依赖树

   ```
   uv tree
   ```

   ```
   Resolved 22 packages in 7ms
   learn v0.1.0
   ├── fastapi v0.116.1
   │   ├── pydantic v2.11.7
   │   │   ├── annotated-types v0.7.0
   │   │   ├── pydantic-core v2.33.2
   │   │   │   └── typing-extensions v4.14.1
   │   │   ├── typing-extensions v4.14.1
   │   │   └── typing-inspection v0.4.1
   │   │       └── typing-extensions v4.14.1
   │   ├── starlette v0.47.2
   │   │   └── anyio v4.9.0
   │   │       ├── idna v3.10
   │   │       └── sniffio v1.3.1
   │   └── typing-extensions v4.14.1
   ├── numpy v2.3.2
   ├── openai v1.98.0
   │   ├── anyio v4.9.0 (*)
   │   ├── distro v1.9.0
   │   ├── httpx v0.28.1
   │   │   ├── anyio v4.9.0 (*)
   │   │   ├── certifi v2025.8.3
   │   │   ├── httpcore v1.0.9
   │   │   │   ├── certifi v2025.8.3
   │   │   │   └── h11 v0.16.0
   │   │   └── idna v3.10
   │   ├── jiter v0.10.0
   │   ├── pydantic v2.11.7 (*)
   │   ├── sniffio v1.3.1
   │   ├── tqdm v4.67.1
   │   └── typing-extensions v4.14.1
   └── unicorn v2.1.3
   (*) Package tree already displayed
   ```



4. 卸载

   ```
   uv remove numpy
   ```

   

5. 注意：`uv add` / `uv remove` 只是针对一级依赖

   我的项目依赖fastapi，而fastapi依赖pydantic。此时，fastapi就是一级依赖，pydantic就是二级依赖。

   `pyproject.toml`中的`dependencies`列出的都是一级依赖

   - 在安装fastapi后，仍然执行`uv add pydantic`。最终`pydantic`会被添加到`pyproject.toml`中。
   - 然后执行`uv remove pydantic`，删除的只是`pyproject.toml`中列出的一级依赖。因为fastapi仍然需要pydantic，所以在环境中，没有删除pydantic



6. 当一个包**既是一级依赖又是二级依赖**时，其最终版本由**依赖解析器**根据以下规则确定：

   1. **一级依赖优先**
      - 如果**一级依赖明确指定了版本**（如 `pydantic>=2.0.0`），解析器会优先满足该版本要求，即使二级依赖的版本与之冲突。
      - 如果冲突无法解决（如二级依赖强制要求 `pydantic<2.0.0`），解析器会报错（`ResolutionImpossible`）。
   3. **冲突时的行为**
      - 如果一级和二级依赖的版本范围**完全不兼容**（如一级要求 `pydantic>=2.0.0`，二级要求 `pydantic<2.0.0`），解析器会失败并提示版本冲突，需要手动解决。



# 3. 打包和同步

1. 打包

   - 调整`pyproject.toml`，添加相关工具

     ```
     [build-system]
     requires = ["setuptools>=65.0.0", "wheel"]  
     build-backend = "setuptools.build_meta"
     ```

   - 目录要调整至python官方的方式

   - 执行

     ```
     uv build
     ```

     （相当于`python -m build`）

     可以看到`dist`文件夹下的whl文件

   

2. 可以使用`uv pip`（ 是 `uv`的一个子命令）

    ```
    uv pip install -e .
    ```
    
    

    注意：使用 `uv pip install pydantic` **不会自动修改 `pyproject.toml`**，它的行为与传统 `pip install` 一致

    - 仅将包安装到当前 Python 环境中，而不会更新项目的依赖声明文件



3. 环境同步

   ```
   uv sync
   ```

   - 自动读取 `pyproject.toml` 中的 `[project.dependencies]`

   - 安装所有依赖，并移除环境中未列出的包

     

# 4. pypi源和缓存

1. 使用清华源

    - https://docs.astral.sh/uv/concepts/configuration-files/

    - https://mirrors.tuna.tsinghua.edu.cn/help/pypi/

      

    在 `~/.config/uv/uv.toml` 或者 `/etc/uv/uv.toml` 填写下面的内容：

    ```
    [[index]]
    url = "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/"
    default = true
    ```



2. 缓存相关

    - 查看`uv add`导致的缓存位置

      ```
      uv cache dir
      ```

    - 清理缓存

      ```
      uv cache clean
      ```

      
