#!/usr/lib/env python
# -*- encoding:utf-8 -*-

import re
import os
import argparse


# 生成启动文件
os.system("echo '#!/usr/lib/env python' > app.py")
os.system("echo '# -*- encoding:utf-8 -*-' >> app.py")
os.system("echo '' >> app.py")
os.system("echo 'from lixingtie.web import Application' >> app.py")
os.system("echo '' >> app.py")
os.system("echo '' >> app.py")
os.system("""echo 'if __name__ == "__main__":' >> app.py""")
os.system("echo '    Application.start(port=8085)' >> app.py")

# 生成静态目录
os.system("rm -rf static")
os.system("mkdir static")
os.system("cp ../favicon.ico static/")
os.system("cp -r ../img/ static/img/")
os.system("cp -r ../css/ static/css/")
os.system("cp -r ../js/ static/js/")
os.system("cp -r ../lib/ static/lib/")
os.system("cp -r ../templates/ static/templates/")

# 生成模板目录
os.system("rm -rf views")
os.system("mkdir views")
# 生成主页文件
with open("../index.html", "r") as index_src:
    with open("views/index.html", "w") as index_dest:
        c = index_src.read()
        c = c.replace("{{", "{{!")

        pattern = "href=[\"']([^\"']+)[\"']"
        c = re.sub(pattern, "href=\"{{ static_url(\"\\1\") }}\"", c)

        pattern = "src=[\"']([^\"']+)[\"']"
        c = re.sub(pattern, "src=\"{{ static_url(\"\\1\") }}\"", c)

        index_dest.write(c)
