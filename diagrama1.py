from graphviz import Digraph

dot = Digraph(comment='The Code Flow')

dot.node('A', 'Inicio')
dot.node('B', 'Lectura de entrada estándar')
dot.node('C', 'Para cada línea en la entrada:')
dot.node('D', '- Limpiar la línea')
dot.node('E', '- Dividir la línea por el tabulador')
dot.node('F', '- Si result[0] está en las claves de doc_count:')
dot.node('G', '   - Si result[1] está en las claves de doc_count[result[0]]:')
dot.node('H', '      - Incrementar el contador')
# ... Agrega más nodos según sea necesario

dot.edges(['AB', 'BC', 'CD', 'DE', 'EF', 'FG', 'GH'])
# ... Agrega más bordes según sea necesario

dot.render('code_flow', format='png', cleanup=True)
