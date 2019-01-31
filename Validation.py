from pykwalify.core import Core


c = Core(source_file="document.yaml", schema_files=["schema.yaml"])
c.validate(raise_exception=True)

