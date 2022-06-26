import ast

class MyNodeVisitor(ast.NodeVisitor):
  def visit_ClassDef(self, node: ast.ClassDef):

    print("-----")
    print(node.name)
    if node.bases[0].id == "Enum" :
      print("Enum | パターン")
      for enum_member in node.body:
        for target in enum_member.targets:
          if(target.id != "__order__"):
            print(target.id + ":" + enum_member.value.s)
    
    if node.bases[0].id == "Variable":
      print("Variable | 変数")
      for variable_member in node.body:
        if type(variable_member) == ast.Assign:
          for index, assing_target in enumerate(variable_member.targets):
            if assing_target.id == "label":
              print("タイトル：" + variable_member.value.s)
        
        if type(variable_member) == ast.FunctionDef:
          print("この値は計算に基づき処理されます")

              

    self.generic_visit(node)

with open("openfisca/openfisca_yuisekin/variables/障害/身体障害者手帳.py", mode="r", encoding="utf-8") as f:
  source = f.read()
  tree = ast.parse(source=source)
  MyNodeVisitor().visit(node=tree)