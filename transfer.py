import sqlite3
import json
import os

def convert_db_to_js():
    # 1. 获取当前脚本所在的绝对路径 (即 py 文件夹的路径)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. 拼接数据库的完整路径 (确保无论在哪里运行都能找到 db)
    db_path = os.path.join(script_dir, 'fortunes.db')
    
    # 3. 设置输出路径：自动输出到上一级目录 (即 index_liuyao.html 所在的目录)
    # 这样您生成后就不用手动移动文件了
    parent_dir = os.path.dirname(script_dir)
    js_path = os.path.join(parent_dir, 'fortunes.js')

    print(f"Checking database at: {db_path}")

    if not os.path.exists(db_path):
        print(f"❌ 错误: 依然找不到数据库文件。请确认 fortunes.db 确实在 {script_dir} 目录下。")
        return

    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 查询所有数据
        cursor.execute("SELECT * FROM fortunes")
        
        # 获取列名
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        # 转换为字典列表
        results = []
        for row in rows:
            results.append(dict(zip(columns, row)))
            
        # 生成 JS 内容
        js_content = f"// 自动生成的运势数据库 (包含 {len(results)} 条数据)\nconst FORTUNES_DB = {json.dumps(results, ensure_ascii=False, indent=4)};"
        
        # 写入文件到上一级目录
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print("-" * 30)
        print(f"✅ 成功! 转换完成。")
        print(f"📂 JS文件已保存到: {js_path}")
        print(f"📊 共处理了 {len(results)} 条运势。")
        print("现在您可以直接打开 HTML 文件查看效果了！")
        print("-" * 30)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ 发生程序错误: {e}")

if __name__ == '__main__':
    convert_db_to_js()