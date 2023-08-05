# test

Supervisor for Windows wrote by Weber Juche.
2016.7.19

## 设计目的

在Windows下启动并控制其它命令行程序(cmdProgram)运行。
类似于Linux系统下的 Supervisor 工具。

## 打包上传PyPi方法
相关命令如下

````
$ python setup.py sdist  # 编译包
$ python setup.py sdist upload # 上传包
$ pip install --upgrade --no-cache-dir weberWinSV
````

## 20190731
pip install twine
````
(py27) c:\WeiYF\git\bitbucket\wyfpythoneggs\weberWinSV>python setup.py sdist

(py27) c:\WeiYF\git\bitbucket\wyfpythoneggs\weberWinSV>twine check dist/*
Checking distribution dist\weberWinSV-0.0.19.tar.gz: Passed
(py27) c:\WeiYF\git\bitbucket\wyfpythoneggs\weberWinSV>twine upload --repository-url https://test.pypi.org/legacy/ dist/*
Enter your username: Weber.JC
Enter your password:
Uploading distributions to https://test.pypi.org/legacy/
Uploading weberWinSV-0.0.19.tar.gz
 45%|█████████████████████████████████████████████████
100%|█████████████████████████████████████████████████████████████████████████
███████████████████████████████████| 17.6k/17.6k [00:07<00:00, 2.48kB/s]

(py27) c:\WeiYF\git\bitbucket\wyfpythoneggs\weberWinSV>twine upload dist/* --repository-url https://upload.pypi.org/legacy/
Enter your username: Weber.JC
Enter your password:
Uploading distributions to https://upload.pypi.org/legacy/
Uploading weberWinSV-0.0.19.tar.gz
 45%|█████████████████████████████████████████████████
100%|█████████████████████████████████████████████████████████████████████████
███████████████████████████████████| 17.6k/17.6k [00:05<00:00, 3.31kB/s]
````
