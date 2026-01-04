import subprocess
import json
import os

def create_custom_html_template():
    """Create custom HTML template with collapsible code functionality"""
    template_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{resources['metadata']['name']}}</title>
    
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        
        .jp-Cell {
            background: white;
            margin: 15px 0;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Code cell styles */
        .jp-InputArea {
            position: relative;
            margin-bottom: 10px;
        }
        
        /* Toggle button */
        .code-toggle {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 14px;
            margin-bottom: 10px;
            transition: background 0.3s;
            font-weight: 500;
        }
        
        .code-toggle:hover {
            background: #45a049;
        }
        
        .code-toggle.collapsed {
            background: #2196F3;
        }
        
        .code-toggle.collapsed:hover {
            background: #0b7dda;
        }
        
        /* Code area */
        .jp-InputArea-editor {
            background: #f8f9fa;
            border: 1px solid #e1e4e8;
            border-radius: 4px;
            padding: 10px;
            overflow-x: auto;
        }
        
        .jp-InputPrompt {
            color: #0366d6;
            font-weight: bold;
            padding-right: 10px;
        }
        
        /* Code highlighting */
        pre {
            margin: 0;
            padding: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        code {
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 13px;
            line-height: 1.5;
        }
        
        /* Output area */
        .jp-OutputArea {
            margin-top: 10px;
        }
        
        .jp-OutputArea-output {
            background: #fff;
            border: 1px solid #e1e4e8;
            border-radius: 4px;
            padding: 10px;
            margin: 5px 0;
        }
        
        /* Markdown cells */
        .jp-MarkdownOutput {
            padding: 10px 0;
        }
        
        .jp-MarkdownOutput h1 {
            color: #1a1a1a;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
            margin-top: 30px;
        }
        
        .jp-MarkdownOutput h2 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
            margin-top: 25px;
        }
        
        .jp-MarkdownOutput h3 {
            color: #34495e;
            margin-top: 20px;
        }
        
        /* Images */
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 15px auto;
            border-radius: 4px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        /* Tables */
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        /* Global collapse/expand buttons */
        .global-controls {
            position: sticky;
            top: 0;
            background: white;
            padding: 15px;
            margin: -20px -20px 20px -20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            z-index: 1000;
            text-align: center;
            border-radius: 8px 8px 0 0;
        }
        
        .global-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 4px;
            font-size: 14px;
            margin: 0 5px;
            transition: background 0.3s;
            font-weight: 500;
        }
        
        .global-btn:hover {
            background: #45a049;
        }
        
        /* Hidden state */
        .code-hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="global-controls">
        <h2 style="margin: 0 0 15px 0; color: #2c3e50;">📊 {{resources['metadata']['name']}}</h2>
        <button class="global-btn" onclick="toggleAllCode(true)">📂 Expand All Code</button>
        <button class="global-btn" onclick="toggleAllCode(false)">📁 Collapse All Code</button>
    </div>
    
    <div id="notebook-container">
        {% for cell in nb.cells %}
            <div class="jp-Cell">
                {% if cell.cell_type == 'code' %}
                    <!-- Code cell -->
                    <button class="code-toggle" onclick="toggleCode(this)">
                        � Hide Code
                    </button>
                    <div class="jp-InputArea">
                        <div class="jp-InputPrompt">In [{{ cell.execution_count if cell.execution_count else ' ' }}]:</div>
                        <div class="jp-InputArea-editor">
                            <pre><code>{{ cell.source }}</code></pre>
                        </div>
                    </div>
                    
                    {% if cell.outputs %}
                    <div class="jp-OutputArea">
                        {% for output in cell.outputs %}
                            <div class="jp-OutputArea-output">
                                {% if output.output_type == 'stream' %}
                                    <pre>{{ output.text }}</pre>
                                {% elif output.output_type == 'execute_result' or output.output_type == 'display_data' %}
                                    {% if 'text/html' in output.data %}
                                        {{ output.data['text/html'] | safe }}
                                    {% elif 'image/png' in output.data %}
                                        <img src="data:image/png;base64,{{ output.data['image/png'] }}" />
                                    {% elif 'text/plain' in output.data %}
                                        <pre>{{ output.data['text/plain'] }}</pre>
                                    {% endif %}
                                {% elif output.output_type == 'error' %}
                                    <pre style="color: red;">{{ output.traceback | join('\n') }}</pre>
                                {% endif %}
                            </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    
                {% elif cell.cell_type == 'markdown' %}
                    <!-- Markdown cell -->
                    <div class="jp-MarkdownOutput">
                        {{ cell.source | markdown2html | safe }}
                    </div>
                {% endif %}
            </div>
        {% endfor %}
    </div>
    
    <script>
        // Toggle individual code block
        function toggleCode(button) {
            const codeArea = button.nextElementSibling.querySelector('.jp-InputArea-editor');
            const isHidden = codeArea.classList.contains('code-hidden');
            
            if (isHidden) {
                codeArea.classList.remove('code-hidden');
                button.textContent = 'Hide Code';
                button.classList.remove('collapsed');
            } else {
                codeArea.classList.add('code-hidden');
                button.textContent = 'Show Code';
                button.classList.add('collapsed');
            }
        }
        
        // Toggle all code blocks
        function toggleAllCode(show) {
            const buttons = document.querySelectorAll('.code-toggle');
            buttons.forEach(button => {
                const codeArea = button.nextElementSibling.querySelector('.jp-InputArea-editor');
                if (show) {
                    codeArea.classList.remove('code-hidden');
                    button.textContent = 'Hide Code';
                    button.classList.remove('collapsed');
                } else {
                    codeArea.classList.add('code-hidden');
                    button.textContent = 'Show Code';
                    button.classList.add('collapsed');
                }
            });
        }
        
        // Load page with all code expanded by default
        window.addEventListener('DOMContentLoaded', () => {
            toggleAllCode(true);
        });
    </script>
</body>
</html>
"""
    
    # 保存模板文件
    template_file = "collapsible_template.tpl"
    with open(template_file, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"✅ 模板文件已创建: {template_file}")
    return template_file


def notebook_to_html_simple(input_nb, output_html=None):
    """
    简单方法：直接使用nbconvert转换并添加JavaScript
    """
    if not output_html:
        output_html = input_nb.replace(".ipynb", "_collapsible.html")
    
    # 先转换为标准HTML
    command = [
        "jupyter", "nbconvert",
        "--to", "html",
        "--output", output_html,
        input_nb
    ]
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ 步骤1: 基础HTML转换完成")
        
        # 读取生成的HTML
        with open(output_html, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 添加折叠代码的JavaScript和CSS
        collapsible_script = """
<style>
    .code-toggle-btn {
        background-color: #4CAF50;
        color: white;
        padding: 8px 16px;
        border: none;
        cursor: pointer;
        border-radius: 4px;
        margin: 5px 0;
        font-size: 14px;
        transition: background-color 0.3s;
    }
    .code-toggle-btn:hover {
        background-color: #45a049;
    }
    .code-toggle-btn.collapsed {
        background-color: #2196F3;
    }
    .code-hidden {
        display: none !important;
    }
    .global-controls {
        position: sticky;
        top: 0;
        background: white;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        z-index: 1000;
        text-align: center;
        margin-bottom: 20px;
    }
    .global-btn {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
        border-radius: 4px;
        margin: 0 10px;
        font-size: 14px;
        font-weight: bold;
    }
    .global-btn:hover {
        background-color: #45a049;
    }
</style>

<script>
    function toggleCode(button) {
        const codeCell = button.parentElement.querySelector('.highlight, .jp-InputArea-editor');
        if (codeCell) {
            const isHidden = codeCell.classList.contains('code-hidden');
            if (isHidden) {
                codeCell.classList.remove('code-hidden');
                button.textContent = 'Hide Code';
                button.classList.remove('collapsed');
            } else {
                codeCell.classList.add('code-hidden');
                button.textContent = 'Show Code';
                button.classList.add('collapsed');
            }
        }
    }
    
    function toggleAllCode(show) {
        const buttons = document.querySelectorAll('.code-toggle-btn');
        buttons.forEach(button => {
            const codeCell = button.parentElement.querySelector('.highlight, .jp-InputArea-editor');
            if (codeCell) {
                if (show) {
                    codeCell.classList.remove('code-hidden');
                    button.textContent = 'Hide Code';
                    button.classList.remove('collapsed');
                } else {
                    codeCell.classList.add('code-hidden');
                    button.textContent = 'Show Code';
                    button.classList.add('collapsed');
                }
            }
        });
    }
    
    document.addEventListener('DOMContentLoaded', function() {
        // Add toggle button before each code cell
        const codeCells = document.querySelectorAll('.jp-InputArea, .input_area');
        codeCells.forEach(cell => {
            const button = document.createElement('button');
            button.className = 'code-toggle-btn';
            button.textContent = 'Hide Code';
            button.onclick = function() { toggleCode(this); };
            cell.parentNode.insertBefore(button, cell);
            
            // Code is visible by default (no code-hidden class added)
        });
        
        // Add global control buttons
        const container = document.querySelector('.container, body');
        if (container) {
            const controlDiv = document.createElement('div');
            controlDiv.className = 'global-controls';
            controlDiv.innerHTML = `
                <h2 style="margin: 0 0 15px 0;">Notebook Viewer</h2>
                <button class="global-btn" onclick="toggleAllCode(true)">Expand All Code</button>
                <button class="global-btn" onclick="toggleAllCode(false)">Collapse All Code</button>
            `;
            container.insertBefore(controlDiv, container.firstChild);
        }
    });
</script>
"""
        
        # 在</body>前插入脚本
        html_content = html_content.replace('</body>', collapsible_script + '</body>')
        
        # 写回文件
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Step 2: Collapsible functionality added")
        print(f"✅ Final HTML saved to: {output_html}")
        print(f"\n📌 Usage Instructions:")
        print(f"   1. Open {output_html} in your browser")
        print(f"   2. Click the button above each code block to expand/collapse individual code")
        print(f"   3. Use the global buttons at the top to expand/collapse all code at once")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Conversion failed: {e.stderr}")
    except Exception as e:
        print(f"❌ Processing failed: {str(e)}")


def notebook_to_html_custom(input_nb, output_html=None):
    """
    使用自定义模板转换（需要Jinja2）
    """
    try:
        import nbformat
        from jinja2 import Template
        
        if not output_html:
            output_html = input_nb.replace(".ipynb", "_custom.html")
        
        # 读取notebook
        with open(input_nb, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # 创建自定义模板
        template_file = create_custom_html_template()
        
        # 使用模板渲染
        with open(template_file, 'r', encoding='utf-8') as f:
            template = Template(f.read())
        
        html_output = template.render(nb=nb, resources={'metadata': {'name': input_nb}})
        
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(html_output)
        
        print(f"✅ 使用自定义模板转换完成: {output_html}")
        
    except ImportError:
        print("⚠️  需要安装 nbformat 和 jinja2")
        print("   运行: pip install nbformat jinja2")
    except Exception as e:
        print(f"❌ 转换失败: {str(e)}")


# 使用示例
if __name__ == "__main__":
    input_notebook = "evaluation.ipynb"
    
    print("="*60)
    print("📓 Notebook转HTML（带折叠代码功能）")
    print("="*60)
    
    # 方法1: 简单方法（推荐，不需要额外依赖）
    print("\n🔹 使用方法1: 简单转换（推荐）")
    notebook_to_html_simple(input_notebook, "evaluation_collapsible.html")
    
    # 方法2: 自定义模板（需要额外安装库）
    # print("\n🔹 使用方法2: 自定义模板")
    # notebook_to_html_custom(input_notebook, "evaluation_custom.html")