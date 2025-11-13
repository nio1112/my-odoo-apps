{
    "name": "Demo Module",
    "summary": "一个简单的演示模块，包含 demo.record 的列表与表单视图。",
    "version": "1.0.0",
    "category": "Tools",
    "author": "YourName",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/demo_record_views.xml",
    ],
    "application": True,
    "installable": True,
}