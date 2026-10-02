from fastapi import APIRouter

from app.common.http.api_response import success

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.get("/machines/{machine_id}")
async def get_machine(machine_id: str) -> dict:
  return success(
    {
      "id": machine_id,
      "name": f"Machine {machine_id}",
      "line": "L-01",
      "status": "running",
    }
  )


@router.post("/step/ack")
async def ack_step(body: dict) -> dict:
  return success({"acknowledged": True, "step_id": body.get("step_id")})


@router.post("/alarms/{alarm_id}/ack")
async def ack_alarm(alarm_id: int) -> dict:
  return success({"alarm_id": alarm_id, "acknowledged": True})
