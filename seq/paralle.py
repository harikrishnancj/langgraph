from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class Batsmanstate(TypedDict):
    balls:int
    runs:int
    six:int
    four:int

    SR:float
    boundaryperc:float
    ballperbound:float
    summary:str

def Strike_rate(state:Batsmanstate) :
    sr=(state['runs']/state['balls'])*100

    return{'SR':sr}

def bpb(state:Batsmanstate):
    bpb=(state['balls']/(state['four']+state['six']))

    return{"ballperbound":bpb}

def bperc(state:Batsmanstate):
    boundary_percent = (((state['four'] * 4) + (state['six'] * 6))/state['runs'])*100

    return {'boundaryperc': boundary_percent}

def summary(state: Batsmanstate):

    summary = f"""
Strike Rate - {state['SR']} \t
Balls per boundary - {state['ballperbound']} \t
Boundary percent - {state['boundaryperc']}
"""
    
    return {'summary': summary}

Graph=StateGraph(Batsmanstate)

Graph.add_node('Strike Rate',Strike_rate)
Graph.add_node("bounderyperball",bpb)
Graph.add_node('boundaryperc',bperc)
Graph.add_node('summary',summary)

Graph.add_edge(START,"Strike Rate")
Graph.add_edge(START,"bounderyperball")
Graph.add_edge(START,"boundaryperc")
Graph.add_edge("Strike Rate",'summary')
Graph.add_edge("bounderyperball",'summary')
Graph.add_edge("boundaryperc",'summary')
Graph.add_edge('summary',END)

workflow = Graph.compile()

print(workflow)



intial_state = {
    'runs': 100,
    'balls': 50,
    'four': 6,
    'six': 4
}

s=workflow.invoke(intial_state)
print(s)
"*********************************************************************************************************"
"""START → Strike Rate
START → bounderyperball
START → boundaryperc
Strike Rate → summary
bounderyperball → summary
boundaryperc → summary
summary → END
"""