import operator
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END

from workers.legal_worker import legal_worker_node
from workers.news_worker import news_worker_node
from workers.general_worker import general_worker_node
from supervisor import supervisor_node

# Định nghĩa State
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

# Khởi tạo Graph
workflow = StateGraph(AgentState)

# Thêm Nodes
workflow.add_node("Supervisor", supervisor_node)
workflow.add_node("LegalWorker", legal_worker_node)
workflow.add_node("NewsWorker", news_worker_node)
workflow.add_node("GeneralWorker", general_worker_node)

# Định tuyến từ Supervisor
workflow.add_conditional_edges(
    "Supervisor",
    lambda state: state["next"],
    {
        "LegalWorker": "LegalWorker",
        "NewsWorker": "NewsWorker",
        "GeneralWorker": "GeneralWorker",
        "FINISH": END
    }
)

# Sau khi Worker xử lý xong, chuyển về Supervisor để đánh giá xem đã xong chưa
workflow.add_edge("LegalWorker", "Supervisor")
workflow.add_edge("NewsWorker", "Supervisor")
workflow.add_edge("GeneralWorker", "Supervisor")

# Điểm bắt đầu
workflow.add_edge(START, "Supervisor")

# Compile graph
app_graph = workflow.compile()
