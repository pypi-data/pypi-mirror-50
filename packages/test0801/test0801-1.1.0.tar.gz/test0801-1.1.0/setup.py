from distutils.core import setup
#从python发布工具导入setup函数
setup(
		name          = 'test0801',
		version       ='1.1.0',
		py_modules    =['test0801'],                  #模块元数据与setup函数参数关联
		author        ='hfpython',                    #该行以下，元数据可不同
		author_email  ='hfpython@headfirstlabs.com',
		url           ='http://www.headfirstlabs.com',
		description   ='A simple printer of nested lists',
	   #函数参数名
	)
	