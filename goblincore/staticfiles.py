from django.contrib.staticfiles.apps import StaticFilesConfig as BaseStaticFilesConfig


class StaticFilesConfig(BaseStaticFilesConfig):
    ignore_patterns = [
        *BaseStaticFilesConfig.ignore_patterns,
        "css/globals.css",
        "js/*.ts",
        "js/tests/*",
    ]
