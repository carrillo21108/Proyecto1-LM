from ply.lex import lex
from ply.yacc import yacc
from graphviz import Digraph

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def plot_tree(root, graph=None):
    if graph is None:
        graph = Digraph()
        graph.node(name=str(id(root)), label=root.value)
    if root.left:  # si el nodo izquierdo existe, se agrega al gráfico y se conecta con la raíz
        graph.node(name=str(id(root.left)), label=root.left.value)
        graph.edge(str(id(root)), str(id(root.left)))
        plot_tree(root.left, graph)
    if root.right:  # si el nodo derecho existe, se agrega al gráfico y se conecta con la raíz
        graph.node(name=str(id(root.right)), label=root.right.value)
        graph.edge(str(id(root)), str(id(root.right)))
        plot_tree(root.right, graph)
    return graph

# Tokenizer
# Tokens
tokens = ('NEGATION',
          'CONJUNCTION',
          'DISJUNCTION',
          'IMPLICATION',
          'BICONDITIONAL',
          'LPAREN',
          'RPAREN',
          'VARIABLE',
          'CONSTANT')

# Definicion de Tokens
t_ignore = ' \t'
t_NEGATION = r'\~'
t_CONJUNCTION = r'\^'
t_DISJUNCTION = r'o'
t_IMPLICATION = r'→'
t_BICONDITIONAL = r'↔'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_VARIABLE = r'[pqrstuvwxyz]'
t_CONSTANT = r'[01]'

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

precedence = (
    ('left', 'IMPLICATION', 'BICONDITIONAL'),
    ('left', 'DISJUNCTION'),
    ('left', 'CONJUNCTION'),
    ('left', 'NEGATION')
)

lexer = lex()


# Parser
def p_expression_value(p):
    '''
    expression : VARIABLE
                | CONSTANT
    '''
    p[0] = Node(p[1])

def p_expression_negation(p):
    '''
    expression : NEGATION expression
    '''
    node = Node(p[1])
    node.right = p[2]
    p[0] = node

def p_factor_grouped(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_expression(p):
    '''
    expression : expression CONJUNCTION expression
               | expression DISJUNCTION expression
               | expression IMPLICATION expression
               | expression BICONDITIONAL expression
    '''
    node = Node(p[2])
    node.left = p[1]
    node.right = p[3]
    p[0] = node

def p_error(p):
    print(f'Syntax error at {p.value!r}')

# Construccion del Parser
parser = yacc()

# Reconocimiento de expresion
ast = parser.parse('((p→q)^p)')

# Grafo dirigido
tree_graph = plot_tree(ast)
nombre_archivo_pdf = 'AST'
tree_graph.view(filename=nombre_archivo_pdf)

