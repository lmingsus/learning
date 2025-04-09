'''
https://langchain-ai.github.io/langgraph/reference/graphs/?h=stream_mode#langgraph.graph.graph.CompiledGraph.stream
'''

import operator
from typing_extensions import Annotated, TypedDict
from langgraph.graph import StateGraph, START

class State(TypedDict):
    aaalist: Annotated[list, operator.add]
    bbblist: Annotated[list, operator.add]

builder = StateGraph(State)
builder.add_node("a", lambda _state: {"bbblist": ['こんにちは']})
builder.add_node("b", lambda _state: {"aaalist": ["there"]})
builder.add_node("c", lambda _state: {"bbblist": ['안녕하세요']})
builder.add_edge("a", "b")
builder.add_edge("b", "c")
builder.add_edge(START, "a")
graph = builder.compile()

#  stream_mode="values" ------------------------------------------
for event in graph.stream({"aaalist": ['你好']}, stream_mode="values"):
    print(event)

for event in graph.stream({"aaalist": ['你好']}, stream_mode="values"):
    # message = event["messages"][-1]
    message = event
    if isinstance(message, tuple):
        print(message)
    else:
        # message.pretty_print()
        print(message)

{'aaalist': ['你好'], 'bbblist': []}
{'aaalist': ['你好'], 'bbblist': ['こんにちは']}
{'aaalist': ['你好', 'there'], 'bbblist': ['こんにちは']}
{'aaalist': ['你好', 'there'], 'bbblist': ['こんにちは', '안녕하세요']}



#  stream_mode="updates" ------------------------------------------
for event in graph.stream({"aaalist": ['你好']}, stream_mode="updates"):
    print(event)

{'a': {'bbblist': ['こんにちは']}}
{'b': {'aaalist': ['there']}}
{'c': {'bbblist': ['안녕하세요']}}


#  stream_mode="debug"  ------------------------------------------
import json
for event in graph.stream({"aaalist": ['你好']}, stream_mode="debug"):
    print(json.dumps(event, indent=4, ensure_ascii=False))

'''
{
    "type": "task",
    "timestamp": "2025-04-02T17:25:30.191540+00:00",
    "step": 1,
    "payload": {
        "id": "62a137c8-6a7f-bc20-1745-e673ed7a3712",
        "name": "a",
        "input": {
            "aaalist": [
                "你好"
            ],
            "bbblist": []
        },
        "triggers": [
            "start:a"
        ]
    }
}
{
    "type": "task_result",
    "timestamp": "2025-04-02T17:25:30.194525+00:00",
    "step": 1,
    "payload": {
        "id": "62a137c8-6a7f-bc20-1745-e673ed7a3712",
        "name": "a",
        "error": null,
        "result": [
            [
                "bbblist",
                [
                    "こんにちは"
                ]
            ]
        ],
        "interrupts": []
    }
}
{
    "type": "task",
    "timestamp": "2025-04-02T17:25:30.196538+00:00",
    "step": 2,
    "payload": {
        "id": "9545db88-a143-6e09-a6a6-85a9f8633056",
        "name": "b",
        "input": {
            "aaalist": [
                "你好"
            ],
            "bbblist": [
                "こんにちは"
            ]
        },
        "triggers": [
            "a"
        ]
    }
}
{
    "type": "task_result",
    "timestamp": "2025-04-02T17:25:30.205529+00:00",
    "step": 2,
    "payload": {
        "id": "9545db88-a143-6e09-a6a6-85a9f8633056",
        "name": "b",
        "error": null,
        "result": [
            [
                "aaalist",
                [
                    "there"
                ]
            ]
        ],
        "interrupts": []
    }
}
{
    "type": "task",
    "timestamp": "2025-04-02T17:25:30.206533+00:00",
    "step": 3,
    "payload": {
        "id": "bf797866-0dd5-06f1-6c14-238322ffb82b",
        "name": "c",
        "input": {
            "aaalist": [
                "你好",
                "there"
            ],
            "bbblist": [
                "こんにちは"
            ]
        },
        "triggers": [
            "b"
        ]
    }
}
{
    "type": "task_result",
    "timestamp": "2025-04-02T17:25:30.208532+00:00",
    "step": 3,
    "payload": {
        "id": "bf797866-0dd5-06f1-6c14-238322ffb82b",
        "name": "c",
        "error": null,
        "result": [
            [
                "bbblist",
                [
                    "안녕하세요"
                ]
            ]
        ],
        "interrupts": []
    }
}
'''

#  stream_mode="custom" ------------------------------------------

from langgraph.types import StreamWriter

def node_a(state: State, writer: StreamWriter):
     writer({"custom_data": "哈哈哈"})
     return {"alist": ["hi"]}

builder = StateGraph(State)
builder.add_node("a", node_a)
builder.add_edge(START, "a")
graph = builder.compile()

for event in graph.stream({"aaalist": ['這是 custom 例子']}, stream_mode="custom"):
     print(event)