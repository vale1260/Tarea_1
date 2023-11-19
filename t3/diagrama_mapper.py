import graphviz

def crear_diagrama():
    grafo = graphviz.Digraph('diagrama', format='png', engine='dot', strict=True)

    grafo.node('Inicio')
    grafo.node('postgresql_connect')
    grafo.node('process_input')
    grafo.node('insert_paginas')

    grafo.edge('Inicio', 'postgresql_connect')
    grafo.edge('postgresql_connect', 'process_input')
    grafo.edge('process_input', 'insert_paginas')
    grafo.edge('process_input', 'process_input', label='bucle')
    grafo.edge('insert_paginas', 'process_input')

    return grafo

def principal():
    grafo = crear_diagrama()
    grafo.render(filename='diagrama_mapper', cleanup=True, format='png', engine='dot')

if __name__ == '__main__':
    principal()
