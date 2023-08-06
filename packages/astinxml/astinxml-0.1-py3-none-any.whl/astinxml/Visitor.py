import ast

class Visitor(ast.NodeVisitor):
    def __init__(self, xmlDoc, xmlNode):
        self.document = xmlDoc
        self.stack = [xmlNode]

    def createElement(self, parent, name):
        xmlNode = self.document.createElement(name)
        parent.appendChild(xmlNode)
        return xmlNode

    def generic_visit(self, node):
        nodeType = type(node).__name__
        xmlNode = self.createElement(self.stack[-1], nodeType)
        self.stack.append(xmlNode)

        for (key,value) in list(node.__dict__.items()):
            if isinstance(value, ast.AST):
                self.visit(value)
            elif isinstance(value, list):
                newNode= self.createElement(xmlNode, key)
                self.stack.append(newNode)
                for e in value:
                    if isinstance(e, ast.AST):
                        self.visit(e)
                    else:
                        newNode.setAttribute(key,str(value))
                self.stack.pop()
            else:
                xmlNode.setAttribute(key, str(value))
        self.lastNode=self.stack.pop()
        return xmlNode