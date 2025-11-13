from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ...core.database import get_db
import asyncio

router = APIRouter()

@router.websocket("/ws/run/{run_id}")
async def ws_run_log(websocket: WebSocket, run_id: int):
    await websocket.accept()
    db = next(get_db())
    try:
        while True:
            from ...models.workflow_run import WorkflowRun
            run = db.query(WorkflowRun).filter(WorkflowRun.id == run_id).first()
            if run and run.logs:
                # send last log entry; wrap in a JSON-serializable structure
                await websocket.send_json({"log": run.logs[-1]})
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
    finally:
        try:
            db.close()
        except Exception:
            pass
