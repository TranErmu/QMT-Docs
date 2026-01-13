# -*- coding: utf-8 -*-
"""
QMT API 文档爬虫

功能：
1. 下载QMT API文档网页
2. 下载文档中的所有图片
3. 替换图片URL为本地路径
4. 整合为markdown文件
"""

import os
import re
import time
import hashlib
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


# ================================================================================================
# 配置
# ================================================================================================

BASE_URL = "https://dict.thinktrader.net/nativeApi/"
OUTPUT_DIR = Path("./QMT-API/QMT_Docs")
IMAGES_DIR = OUTPUT_DIR / "images"

# 需要爬取的页面列表
PAGES = [
    "start_now.html",
    "xtdata.html",
    "xttrader.html",
    "code_examples.html",
    "question_function.html",
    "download_xtquant.html",
]

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://dict.thinktrader.net/",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


# ================================================================================================
# 辅助函数
# ================================================================================================

def ensure_dirs() -> None:
    """确保输出目录存在"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ 创建目录: {OUTPUT_DIR}")
    print(f"✓ 创建目录: {IMAGES_DIR}")


def fetch_page(url: str, max_retries: int = 3) -> str | None:
    """
    获取网页内容
    
    :param url: 网页URL
    :param max_retries: 最大重试次数
    :return: 网页HTML内容
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
            else:
                print(f"  ✗ 请求失败 [{response.status_code}]: {url}")
                time.sleep(2)
        except Exception as e:
            print(f"  ✗ 请求异常: {e}")
            time.sleep(2)
    return None


def download_image(url: str, save_path: Path) -> bool:
    """
    下载图片
    
    :param url: 图片URL
    :param save_path: 保存路径
    :return: 是否成功
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"  ✗ 下载图片失败: {e}")
    return False


def get_image_filename(url: str) -> str:
    """
    根据URL生成图片文件名
    
    :param url: 图片URL
    :return: 文件名
    """
    parsed = urlparse(url)
    path = parsed.path
    
    # 获取原始文件名
    original_name = os.path.basename(path)
    
    if original_name and '.' in original_name:
        # 添加hash前缀避免重名
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        name, ext = os.path.splitext(original_name)
        return f"{url_hash}_{name}{ext}"
    else:
        # 使用hash作为文件名
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return f"{url_hash}.png"


# ================================================================================================
# 步骤2：下载所有网页
# ================================================================================================

def download_all_pages() -> list[Path]:
    """
    下载所有API文档页面
    
    :return: 已下载的文件路径列表
    """
    print("\n" + "=" * 60)
    print("步骤2: 下载所有网页")
    print("=" * 60)
    
    downloaded_files: list[Path] = []
    
    for page in PAGES:
        url = urljoin(BASE_URL, page)
        save_path = OUTPUT_DIR / page
        
        print(f"\n正在下载: {page}")
        html = fetch_page(url)
        
        if html:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"  ✓ 保存到: {save_path}")
            downloaded_files.append(save_path)
        else:
            print(f"  ✗ 下载失败: {page}")
        
        time.sleep(1)  # 避免请求过快
    
    print(f"\n共下载 {len(downloaded_files)} 个页面")
    return downloaded_files


# ================================================================================================
# 步骤3：提取并下载所有图片
# ================================================================================================

def extract_and_download_images() -> dict[str, str]:
    """
    从已下载的HTML文件中提取图片URL并下载
    
    :return: URL到本地路径的映射字典
    """
    print("\n" + "=" * 60)
    print("步骤3: 提取并下载所有图片")
    print("=" * 60)
    
    url_to_local: dict[str, str] = {}
    all_image_urls: set[str] = set()
    
    # 遍历所有HTML文件提取图片URL
    for html_file in OUTPUT_DIR.glob("*.html"):
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # 查找所有img标签
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                # 转换为绝对URL
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = 'https://dict.thinktrader.net' + src
                elif not src.startswith('http'):
                    src = urljoin(BASE_URL, src)
                all_image_urls.add(src)
    
    print(f"\n发现 {len(all_image_urls)} 个图片URL")
    
    # 下载所有图片
    for i, img_url in enumerate(all_image_urls, 1):
        filename = get_image_filename(img_url)
        save_path = IMAGES_DIR / filename
        
        print(f"[{i}/{len(all_image_urls)}] 下载: {filename}")
        
        if save_path.exists():
            print(f"  → 已存在，跳过")
            url_to_local[img_url] = f"images/{filename}"
            continue
        
        if download_image(img_url, save_path):
            print(f"  ✓ 保存成功")
            url_to_local[img_url] = f"images/{filename}"
        else:
            print(f"  ✗ 下载失败")
        
        time.sleep(0.5)
    
    print(f"\n共下载 {len(url_to_local)} 个图片")
    return url_to_local


# ================================================================================================
# 步骤4：替换图片URL为本地路径
# ================================================================================================

def replace_image_urls(url_to_local: dict[str, str]) -> None:
    """
    替换HTML文件中的图片URL为本地路径
    
    :param url_to_local: URL到本地路径的映射
    """
    print("\n" + "=" * 60)
    print("步骤4: 替换图片URL为本地路径")
    print("=" * 60)
    
    for html_file in OUTPUT_DIR.glob("*.html"):
        print(f"\n处理: {html_file.name}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        replacements = 0
        for url, local_path in url_to_local.items():
            if url in content:
                content = content.replace(url, local_path)
                replacements += 1
        
        # 同时处理相对路径格式的URL
        soup = BeautifulSoup(content, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src')
            if src and src in url_to_local:
                img['src'] = url_to_local[src]
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"  ✓ 替换了 {replacements} 处图片URL")


# ================================================================================================
# 步骤5：整合成markdown文件
# ================================================================================================

def convert_to_markdown() -> Path:
    """
    将所有HTML页面整合成一个markdown文件
    
    :return: 生成的markdown文件路径
    """
    print("\n" + "=" * 60)
    print("步骤5: 整合成markdown文件")
    print("=" * 60)
    
    markdown_content = "# QMT API 文档\n\n"
    markdown_content += "> 本文档由爬虫自动生成\n\n"
    markdown_content += "---\n\n"
    
    # 页面标题映射
    page_titles = {
        "start_now.html": "快速开始",
        "xtdata.html": "XtQuant.XtData 行情模块",
        "xttrader.html": "XtQuant.Xttrade 交易模块",
        "code_examples.html": "完整实例",
        "question_function.html": "常见问题",
        "download_xtquant.html": "xtquant版本下载",
    }
    
    # 生成目录
    markdown_content += "## 目录\n\n"
    for page in PAGES:
        title = page_titles.get(page, page)
        anchor = title.replace(" ", "-").replace(".", "")
        markdown_content += f"- [{title}](#{anchor})\n"
    markdown_content += "\n---\n\n"
    
    # 处理每个页面
    for page in PAGES:
        html_file = OUTPUT_DIR / page
        if not html_file.exists():
            continue
        
        title = page_titles.get(page, page)
        print(f"\n转换: {page} -> {title}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        markdown_content += f"## {title}\n\n"
        
        # 提取主要内容区域
        content_div = soup.find('div', class_='content') or soup.find('article') or soup.find('main')
        if content_div:
            # 简单的HTML到Markdown转换
            text = html_to_markdown(content_div)
            markdown_content += text
        else:
            # 如果找不到主内容区域，提取body
            body = soup.find('body')
            if body:
                text = html_to_markdown(body)
                markdown_content += text
        
        markdown_content += "\n\n---\n\n"
    
    # 保存markdown文件
    output_file = OUTPUT_DIR / "QMT_API_Documentation.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n✓ Markdown文档已保存: {output_file}")
    return output_file


def html_to_markdown(element, list_level=0) -> str:
    """
    递归将HTML转换为Markdown，支持嵌套列表
    
    :param element: BeautifulSoup元素
    :param list_level: 当前列表的嵌套级别 (用于缩进)
    :return: Markdown文本
    """
    from bs4 import NavigableString, Comment
    
    markdown = ""
    
    for child in element.children:
        # 跳过注释节点
        if isinstance(child, Comment):
            continue
        
        # 处理文本节点
        if isinstance(child, NavigableString):
            text = str(child).strip()
            if text:
                markdown += text + " "
            continue
        
        # 处理元素节点
        if hasattr(child, 'name') and child.name:
            tag = child.name
            
            if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(tag[1]) + 1  # 增加层级因为我们已经有了顶级标题
                markdown += f"\n{'#' * level} {child.get_text().strip()}\n\n"
            
            elif tag == 'p':
                # 段落，递归处理内部内容（可能有链接、加粗等）
                content = html_to_markdown(child, list_level)
                markdown += f"{content.strip()}\n\n"
            
            elif tag == 'pre' or tag == 'code':
                code = child.get_text()
                # 如果代码包含换行，或者是pre标签，使用代码块
                if '\n' in code or tag == 'pre':
                    markdown += f"```python\n{code}\n```\n\n"
                else:
                    markdown += f"`{code}`"
            
            elif tag in ['ul', 'ol']:
                markdown += "\n"
                is_ordered = tag == 'ol'
                
                # 确定当前列表项的缩进级别
                # 如果当前element是li，说明这个ul/ol是嵌套在li内部的，需要增加缩进
                # 否则，保持当前list_level（通常是0，表示顶级列表）
                item_indent_level = list_level + 1 if element.name == 'li' else list_level
                
                for i, li in enumerate(child.find_all('li', recursive=False), 1):
                    # 递归处理列表项的内容，并传递新的缩进级别
                    content = html_to_markdown(li, item_indent_level)
                    indent = "  " * item_indent_level
                    
                    prefix = f"{i}. " if is_ordered else "- "
                    markdown += f"{indent}{prefix}{content.lstrip()}\n"
                markdown += "\n"
            
            elif tag == 'img':
                src = child.get('src', '')
                alt = child.get('alt', '图片')
                markdown += f"![{alt}]({src})\n\n"
            
            elif tag == 'a':
                href = child.get('href', '')
                text = html_to_markdown(child, list_level).strip()
                # 如果递归处理后文本为空，但有原始文本，则使用原始文本
                if not text:
                    text = child.get_text().strip()
                markdown += f"[{text}]({href})" if href else text
            
            elif tag in ['strong', 'b']:
                markdown += f"**{html_to_markdown(child, list_level).strip()}**"
            
            elif tag in ['em', 'i']:
                markdown += f"*{html_to_markdown(child, list_level).strip()}*"
            
            elif tag == 'br':
                markdown += "\n"
            
            elif tag == 'table':
                markdown += convert_table_to_markdown(child)
            
            elif tag in ['div', 'section', 'article', 'span']:
                # 递归处理容器元素
                markdown += html_to_markdown(child, list_level)
                # 对于块级容器，添加换行
                if tag in ['div', 'section', 'article']:
                    markdown += "\n"
            
            elif tag in ['script', 'style', 'nav', 'header', 'footer', 'aside']:
                # 跳过这些标签
                continue
            
            else:
                # 对于其他未知标签，尝试递归处理其内容
                # 确保不会因为空内容而添加多余的空格或换行
                inner = html_to_markdown(child, list_level)
                if inner.strip():
                    markdown += inner
    
    return markdown


def convert_table_to_markdown(table) -> str:
    """将HTML表格转换为Markdown表格"""
    rows = table.find_all('tr')
    if not rows:
        return ""
    
    markdown = "\n"
    
    for i, row in enumerate(rows):
        cells = row.find_all(['th', 'td'])
        cell_texts = [cell.get_text().strip().replace('\n', ' ') for cell in cells]
        markdown += "| " + " | ".join(cell_texts) + " |\n"
        
        # 在第一行后添加分隔线
        if i == 0:
            markdown += "| " + " | ".join(["---"] * len(cells)) + " |\n"
    
    markdown += "\n"
    return markdown


# ================================================================================================
# 主函数
# ================================================================================================

def main():
    """主函数"""
    print("=" * 60)
    print("QMT API 文档爬虫")
    print("=" * 60)
    
    # 确保目录存在
    ensure_dirs()
    
    # 步骤2：下载所有网页
    downloaded_files = download_all_pages()
    
    if not downloaded_files:
        print("\n✗ 没有成功下载任何页面，程序退出")
        return
    
    # 步骤3：提取并下载图片
    url_to_local = extract_and_download_images()
    
    # 步骤4：替换图片URL
    if url_to_local:
        replace_image_urls(url_to_local)
    
    # 步骤5：整合成markdown
    output_file = convert_to_markdown()
    
    print("\n" + "=" * 60)
    print("✓ 爬取完成！")
    print(f"  - HTML文档: {OUTPUT_DIR}")
    print(f"  - 图片目录: {IMAGES_DIR}")
    print(f"  - Markdown: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
